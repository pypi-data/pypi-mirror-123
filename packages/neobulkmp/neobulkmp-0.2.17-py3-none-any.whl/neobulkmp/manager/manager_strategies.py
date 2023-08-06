import operator
import os
import psutil
import graphio
import math
import humanfriendly
import time
import multiprocessing
import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .manager import Manager

log = logging.getLogger(__name__)


class StrategyBase:
    max_processes_count: int = multiprocessing.cpu_count()
    cache_storage_warning_limit: int = 80
    cache_storage_clogged_limit: int = 90
    _max_graphobjects_count_in_cache: int = 10000000
    min_graphobjects_count_in_cache: int = None
    target_graphobjects_count_in_cache: int = None
    graphio_batchsize: int = 50000
    parsing_worker_spawn_min_wait_time_sec = 60

    cache_storage_total = None

    _last_amount_sourcing_cores = 1

    # On large server with huge core counts, the sourcing workers can fly the cache quickly into the ceilling. thats why we create a default max amount of sourcing workers
    max_sourcing_workers = None

    def __init__(self, manager: "Manager"):
        self.manager = manager
        self._cache_untouched = True
        self._cache_first_hit_time = 0
        if self.cache_storage_total is None:
            self.cache_storage_total = getattr(psutil.virtual_memory(), "total") * 0.80
        else:
            self.cache_storage_total = humanfriendly.parse_size(
                self.cache_storage_total
            )
        self._calc_max_min_graphobjects_count_in_cache()

    def _calc_max_min_graphobjects_count_in_cache(self):
        if not self.target_graphobjects_count_in_cache:
            self.target_graphobjects_count_in_cache = round(
                self._max_graphobjects_count_in_cache * 0.5
            )

        self.min_graphobjects_count_in_cache = round(
            self._max_graphobjects_count_in_cache * 0.3
        )
        if self.min_graphobjects_count_in_cache > self.max_graphobjects_count_in_cache:
            raise ValueError(
                f"'Manager.strategy.min_graphobjects_count_in_cache'->{self.min_graphobjects_count_in_cache} is larger as 'Manager.strategy.max_graphobjects_count_in_cache'->{self.max_graphobjects_count_in_cache}. please adapt your config."
            )

    @property
    def max_graphobjects_count_in_cache(self):
        return self._max_graphobjects_count_in_cache

    @max_graphobjects_count_in_cache.setter
    def max_graphobjects_count_in_cache(self, val: int):
        self._max_graphobjects_count_in_cache = val
        self._calc_max_min_graphobjects_count_in_cache()

    def amount_loading_cores(self) -> int:
        if (
            self.manager.statistics.is_sourcing_phase_done()
            or self.manager.statistics.get_cache_storage_used()
            >= self.manager.cache_size
            or self.manager.statistics.get_cache_storage_level() in ["ORANGE", "RED"]
        ):
            return self.max_processes_count
        c = round(self.max_processes_count - self.amount_sourcing_cores())
        if c == 0:
            c = 1
        # We can take more cores as available because loading processes are waiting a lot for the db and wont use any cpu time during that
        return math.ceil(c * 1.5)

    def amount_loading_nodes_cores(self) -> int:
        c = round(self.amount_loading_cores() * 0.9)
        if c == 0:
            c = 1
        # We can take more cores as available because loading processes are waiting a lot for the db and wont use any cpu time during that
        return math.ceil(c * 1.5)

    def amount_loading_rels_cores(self) -> int:
        # if we ended the sourcing phase (all sourcing workers finished) we first load all nodesets and after that all relsets can load without draining)
        if (
            self.manager.statistics.get_count_left_sourcing_workers() == 0
            and len(self.manager.cache.list_SetsMeta(graphio.NodeSet)) > 0
        ):
            return 0
        # if we are low on nodeSets in the cache we can start more RelSet loaders
        nodesets_cores_needed: int = len(
            self.manager.cache.list_SetsMeta(graphio.NodeSet)
            + self.manager.manager_loading._get_workers(
                status=("initial", "running"),
                tag=self.manager.manager_loading.worker_tag_nodesets,
            )
        )
        if nodesets_cores_needed < self.amount_loading_nodes_cores():
            return self.amount_loading_cores() - nodesets_cores_needed
            # else
        # By default we apply 50% of available loading cores to RelSets (or at least one Core)
        c = round(self.amount_loading_cores() * 0.5)
        if c == 0:
            c = 1
        return math.ceil(c)

    def amount_sourcing_cores(self) -> int:
        if self.manager.manager_sourcing.is_done():
            # we are finished with sourcing. nothing to do here
            return 0
        c = self._last_amount_sourcing_cores
        current_sourcing_workers_running_count = len(
            self.manager.manager_sourcing._get_workers(status=("running"))
        )
        last_open_store_duration = (
            self.manager.statistics.get_last_cache_open_duration_in_sec()
        )

        if not self.manager.cache.store_is_available():
            # cache was full and we are in empty mode. we are waiting until parsers can store new data into the cache
            c = self._last_amount_sourcing_cores
        elif self._cache_untouched:
            # when nothing is in cache yet we only let one parser work.
            # we want to measure how long the first parser need to load data into the cache
            # this way we can carefully increase parser workers without clogging the cache
            if self.manager.statistics.get_cached_graphobjects_total_count() > 0:
                # first objects arrive in cache.
                # from here on we can increase the amount of parsing workers
                self._cache_untouched = False
                self._cache_first_hit_time = (
                    self.manager.statistics.start_time - time.time()
                )
                if (
                    self._cache_first_hit_time
                    < self.parsing_worker_spawn_min_wait_time_sec
                ):
                    # we want at least a cooldown time of <self.parsing_worker_spawn_min_wait_time_sec> seconds for spawning new parsers
                    # otherwise we take the time the first parser needed to fill first data into the cache (+10 secs)
                    self._cache_first_hit_time = (
                        self.parsing_worker_spawn_min_wait_time_sec
                    )
                self._sourcing_cool_down_target_time = (
                    time.time() + self._cache_first_hit_time + 10
                )
            c = self._last_amount_sourcing_cores
        elif current_sourcing_workers_running_count == self._last_amount_sourcing_cores:
            # We now adapt the amount of parser workers to the input perfomance of the neo4j (aka empty rate of the cache)
            # we only change the amount of parser workers if the last change has already happend
            # thats because we need to turn up the amout of parsers very careful. A running parsers runs and fills the cache no matter what. if memory is full we will all die
            # with the current architecture we only can stop all parsers at once, which is a makeshift brake atm
            if self.manager.statistics.get_cache_storage_level() == "RED":
                # if memory is full, dont start any new parsers. we wait until the situation is better
                return 0
            if self._sourcing_cool_down_target_time < time.time():
                # we only start new parser when a cooldown time has passed. this helps us to not spawn a bunch of parsers and then realize they just needed to run warm and now spam our chache
                # Reset timer
                self._sourcing_cool_down_target_time = (
                    time.time() + self._cache_first_hit_time
                )

                # gather some statistics to help us make decisions
                cache_level_mean = (
                    self.manager.statistics.get_mean_count_graph_objects_in_cache()
                )
                cache_level_current = (
                    self.manager.statistics.get_cached_graphobjects_total_count()
                    - self.manager.statistics.get_loaded_graphobjects_total_count()
                )

                cache_level_trend = (
                    self.manager.statistics.get_cached_graphobjects_total_count_trend()
                )
                # Lets make a decision on the amount of parser workers

                if (
                    cache_level_current < self.min_graphobjects_count_in_cache
                    or cache_level_mean < self.min_graphobjects_count_in_cache
                ):
                    # oh boy, we still scrape the bottom of the cache. That could distort our trend analyses and is not where we want to be anyway.
                    # turn up the volume
                    c = self._last_amount_sourcing_cores + 1
                elif (
                    cache_level_mean > self.target_graphobjects_count_in_cache * 0.8
                    and cache_level_mean < self.target_graphobjects_count_in_cache * 1.4
                ):
                    # we are in the sweetspot of cache level.
                    # Here, we can keep feeding the loaders but wont eat too much memory
                    # Enjoy the balance and ❤️ lets keep beeing here happy forever ❤️
                    c = self._last_amount_sourcing_cores
                elif (
                    cache_level_mean > self.max_graphobjects_count_in_cache * 0.95
                    or cache_level_current > self.max_graphobjects_count_in_cache
                ):
                    # we scrap at the ceiling of the cache or we shot over it. we turn the parser amount down
                    c = self._last_amount_sourcing_cores - 1
                    log.info(
                        f"Turn down parser worker slots from {self._last_amount_sourcing_cores} to {c}. Reason: MeanCacheAlmostFull: {cache_level_mean > self.max_graphobjects_count_in_cache * 0.95}, CurrenCacheLvlToHigh: {cache_level_current > self.max_graphobjects_count_in_cache}"
                    )
                elif last_open_store_duration and (
                    last_open_store_duration
                    < self.parsing_worker_spawn_min_wait_time_sec
                ):
                    # we have enough worker to fill the cache pretty quick to the limit lets stop here
                    c = self._last_amount_sourcing_cores
                # Cache filling is in the flow then lets have a look at the trend of the cache. it is filling or drying? Based on that we give more or less cores for parsers
                elif cache_level_trend < 5:
                    c = self._last_amount_sourcing_cores + 1
                elif cache_level_trend > 30:
                    c = self._last_amount_sourcing_cores - 1
                    log.info(
                        f"Turn down parser worker slots from {self._last_amount_sourcing_cores} to {c}. Reason: CacheTrendToSteep: {cache_level_trend > 30}"
                    )
                else:
                    # no trend identifiable.
                    # lets appreciate the balance and do nothing and wait for the next tick
                    c = self._last_amount_sourcing_cores
            else:
                c = self._last_amount_sourcing_cores
        else:
            c = self._last_amount_sourcing_cores
        # max we can want to provide 60% of all cores for parsing
        max_c = math.ceil(self.max_processes_count * 0.6)
        left_needed = self.manager.statistics.get_count_left_sourcing_workers()
        if max_c > left_needed:
            max_c = left_needed
        if c > max_c:
            log.info(
                f"Turn down parser worker slots from {self._last_amount_sourcing_cores} to {max_c}. Reason: MaxSlotsReached: {c > max_c}, NotEnoughParserWorkersLeft: {math.ceil(self.max_processes_count * 0.6) > self.manager.statistics.get_count_left_sourcing_workers()}. self.manager.statistics.get_count_left_sourcing_workers()={self.manager.statistics.get_count_left_sourcing_workers()}"
            )
            c = max_c

        if c < 1:
            c = 1
        self._last_amount_sourcing_cores = c
        return c
