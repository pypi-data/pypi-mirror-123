import multiprocessing
import logging


import time
from typing import List, Dict, Type, Set, Union
from ..worker_sourcing import WorkerSourcing
from ..worker_loading import WorkerLoading
from ..cache_backend import (
    CacheInterface,
    NodeSetMeta,
    RedisCache,
    SetsMetaBase,
)
from .manager_workers_loading import ManagerWorkersLoading
from .manager_workers_sourcing import ManagerWorkersSourcing
from .manager_strategies import StrategyBase
from .manager_statistics import Statistics
from ..cache_logger import LogRecordStreamHandler
import humanfriendly


log = logging.getLogger(__name__)


class Manager:
    # Redis - Default cache backend

    strategy_type: Type[StrategyBase] = StrategyBase

    def __init__(
        self,
        worker_sourcing_class: Type[WorkerSourcing],
        worker_parameters: List[Dict],
        cache_backend: Type[CacheInterface] = RedisCache,
        cache_backend_params: Dict = None,
        cache_size: str = "2000MB",
        debug: bool = False,
    ):
        """[summary]

        Args:
            worker_sourcing_class (Type[WorkerSourcing]): [description]
            worker_parameters (List[Dict]): [description]
            cache_backend (Type[CacheInterface], optional): [description]. Defaults to RedisCache.
            cache_backend_params (Dict, optional): [description]. Defaults to None.
            cache_size (str, optional): Max size of cache that should be available in humanfriendly ( https://pypi.org/project/humanfriendly/ ) size format . Defaults to "2000MB".
        """
        self.debug = debug

        self.worker_sourcing_class = worker_sourcing_class
        self.worker_parameters = worker_parameters
        self.worker_loading_class = WorkerLoading
        self.graph_params = {}
        self.cache_backend = cache_backend
        self.cache_backend_params = cache_backend_params
        self.cache: CacheInterface = self.cache_backend(
            self.cache_backend_params, debug=self.debug
        )
        self.statistics = Statistics(self)
        self.strategy: StrategyBase = self.strategy_type(self)
        self.insert_action: str = "create"
        self.create_indexes = True
        self.create_unique_constraints = False
        self.worker_logging_reciever = LogRecordStreamHandler(self.cache)
        self.cache_size = humanfriendly.parse_size(cache_size)

        self.blocked_labels: Dict[str, Set[SetsMetaBase]] = {}
        self.update_statistics_per_sec = 4
        self.status_log_every_n_sec = 8
        self.manage_store_every_n_sec = 8

        self.report_statistics_print_func = None

    def test_cache_backend_ready(self):
        if self.cache.test_connection():
            return True
        else:
            return False

    def is_cache_log_flushed(self):
        if len(self.cache.get_logs()) == 0:
            return True
        else:
            return False

    def merge(self, graph_params: Dict = {}):
        self.graph_params = graph_params
        self.insert_action = "merge"
        self._start()

    def create(self, graph_params: Dict = {}):
        self.graph_params = graph_params
        self.insert_action = "create"
        self._start()

    def _start(self):
        if not self.test_cache_backend_ready():
            raise Exception(
                f"Cache backend {type(self.cache_backend)} {self.cache_backend_params} not available!"
            )
        if self.report_statistics_print_func is None:
            self.report_statistics_print_func = log.info
        self.cache.clear_cache()
        self.manager_sourcing = ManagerWorkersSourcing(self, self.worker_sourcing_class)
        self.manager_loading = ManagerWorkersLoading(self, self.worker_loading_class)
        self.management_ticks = 0
        finished = False
        self.worker_logging_reciever.handle()
        log.info("##Management start##")
        last_status_log_time = time.time()
        last_statistics_update = time.time()
        last_store_management_time = time.time()
        while not finished:
            self.management_ticks += 1

            if time.time() - last_store_management_time > self.manage_store_every_n_sec:
                self._manage_store()
                last_store_management_time = time.time()
            if time.time() - last_statistics_update > self.update_statistics_per_sec:
                self.statistics.update_statistics(
                    self.manager_sourcing.just_finished_workers,
                    self.manager_loading.just_finished_workers,
                )
                self.manager_loading.just_finished_workers = []
                self.manager_sourcing.just_finished_workers = []
                last_statistics_update = time.time()
            if time.time() - last_status_log_time > self.status_log_every_n_sec:
                self.log_status()
                last_status_log_time = time.time()

            log.debug(f"blocked_labels: {self.blocked_labels}")
            self.manager_sourcing.manage()
            self.manager_loading.manage()

            finished = (
                self.manager_sourcing.is_done() and self.manager_loading.is_done()
            )
        log.debug("##Management finish##")
        # Wait for all log records to be processed
        while not self.is_cache_log_flushed():
            time.sleep(0.1)
        self.statistics.update_statistics([], [])
        self.log_status()

    def log_status(self):
        self.report_statistics_print_func(self.statistics.get_human_readable_report())

    def _block_loading_label(self, block_id: str, labels: Set[str]):
        log.debug(f"BLOCK {labels}")
        if block_id in self.blocked_labels:
            self.blocked_labels[block_id].update(labels)
        else:
            self.blocked_labels[block_id] = set(labels)

    def _release_loading_block_label(self, block_id: str):
        self.blocked_labels.pop(block_id, None)

    def _is_nodeset_loading_blocked(
        self, nodeset_meta: Union[SetsMetaBase, NodeSetMeta]
    ) -> bool:
        if isinstance(nodeset_meta, SetsMetaBase):
            nodeset_meta: NodeSetMeta = self.cache.get_NodeSetMeta(nodeset_meta)
        for label in nodeset_meta.labels:
            if label in self._get_blocked_labels():
                return True

    def _get_blocked_labels(self) -> tuple:
        # flatten all values in a list and remove duplicates
        return {
            label for label_list in self.blocked_labels.values() for label in label_list
        }

    def _manage_store(self):
        store_is_available = self.cache.store_is_available()
        if self.statistics.get_cache_storage_level() == "RED" or (
            self.statistics.get_cached_graphobjects_total_count()
            - self.statistics.get_loaded_graphobjects_total_count()
            > self.strategy.max_graphobjects_count_in_cache
        ):
            if store_is_available:
                self.cache.close_store()
                if self.statistics.get_cache_storage_level() == "RED":
                    log.warning(
                        "Cache backend is blocked for storing new NodeSets and RelationshipSets due to low memory. \n This will impact the overall perfomance dramaticly, but prevents the process from crashing. \n Try to work with a lower core count or get more memory."
                    )
                else:
                    log.debug(
                        "Cache backend is blocked for storing new NodeSets and RelationshipSets due to slow Neo4j database inserting rate. \n This can impact the sourcing perfomance dramaticly, but prevents the processes filling up memory. \n Try to improve Neo4j insert perfomance if this gets in your way"
                    )
        elif not store_is_available and (
            self.statistics.get_cached_graphobjects_current()
            < self.strategy.target_graphobjects_count_in_cache * 0.8
        ):
            # open the store when we are back under the cache target size
            self.cache.open_store()
            log.debug(
                "Cache backend is open for storing NodeSets and RelationshipSets again"
            )
