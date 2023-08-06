import os
import psutil
import graphio
import humanfriendly
from collections import OrderedDict
import time
import graphio
import statistics
import numpy
import math
from typing import TYPE_CHECKING, Type, Union, Dict
from ..worker_base import Progress
from ..worker_loading import WorkerLoading

if TYPE_CHECKING:
    from .manager import Manager


class Statistics:
    NodeSets_done_timeline: OrderedDict = None
    RelSets_done_timeline: OrderedDict = None
    graph_objects_loaded_counts_per_type_timeline: OrderedDict = None
    graph_objects_cached_counts_per_type_timeline: OrderedDict = None
    graph_objects_count_in_cache: OrderedDict = None
    graph_objects_mean_count_in_cache: OrderedDict = None
    management_ticks_timeline: OrderedDict = None

    def __init__(self, manager):
        self.manager: "Manager" = manager
        self.last_tick_sourcing_workers_done = []
        self.start_time = time.time()

        self.NodeSets_done_timeline = OrderedDict()
        self.RelSets_done_timeline = OrderedDict()
        self.graph_objects_loaded_counts_per_type_timeline = OrderedDict()
        self.graph_objects_cached_counts_per_type_timeline = OrderedDict()
        self.graph_objects_count_in_cache = OrderedDict()
        self.graph_objects_mean_count_in_cache = OrderedDict()
        self.management_ticks_timeline = OrderedDict()
        self.cache_store_status_timeline = OrderedDict()

    def update_statistics(
        self, finished_sourcing_workers: list, finished_loading_workers: list
    ):
        current_time = time.time()
        # Save NodeSets/RelSets Workers timeline
        self.NodeSets_done_timeline[current_time] = [
            w for w in finished_loading_workers if w.set_meta.type == graphio.NodeSet
        ]

        self.RelSets_done_timeline[current_time] = [
            w
            for w in finished_loading_workers
            if w.set_meta.type == graphio.RelationshipSet
        ]

        # Save Labels/Rels amount loaded
        self.graph_objects_loaded_counts_per_type_timeline[
            current_time
        ] = self.manager.cache.get_report_graphsets_loaded()

        # Save Labels/Rels amount loaded
        self.graph_objects_cached_counts_per_type_timeline[
            current_time
        ] = self.manager.cache.get_report_graphsets_cached()

        self.graph_objects_count_in_cache[current_time] = (
            self.get_cached_graphobjects_total_count()
            - self.get_loaded_graphobjects_total_count()
        )

        self.graph_objects_mean_count_in_cache[
            current_time
        ] = self.get_mean_count_graph_objects_in_cache()

        # save store status timings
        self.cache_store_status_timeline[
            current_time
        ] = self.manager.cache.store_is_available()

        # Save amount of management ticks
        self.management_ticks_timeline[current_time] = self.manager.management_ticks

    def get_management_ticks_per_n_sec(
        self, n: int = 1, timeframe: int = 120, object_type=None
    ) -> int:
        current_time = time.time()
        running_time = current_time - self.start_time

        if timeframe is None or running_time < timeframe:
            timeframe_start = self.start_time
        else:
            timeframe_start = current_time - timeframe

        relevant_data = OrderedDict()
        for timestamp, tick_count in self.management_ticks_timeline.items():
            if timestamp > timeframe_start:
                relevant_data[timestamp] = tick_count
        relevnt_tick_counts = list(relevant_data.values())
        if len(relevnt_tick_counts) < 2:
            tick_count = 0
        else:
            tick_count = (
                relevnt_tick_counts[len(relevant_data) - 1] - relevnt_tick_counts[0]
            )
        return (tick_count / (current_time - timeframe_start)) * n

    def get_graphobjects_count_loaded_per_n_sec(
        self, n: int = 1, timeframe: int = 120, object_type: str = None
    ) -> int:
        """[summary]

        Args:
            n (int, optional): Timeresolution in sec. Defaults to 1.
            timeframe (int, optional): Take last n seconds into account to calculate median value. Defaults to 20.
            object_type (str, optional): "Nodes" to only count Nodes per second, "Relations" to only count rels per second or None to count both. Defaults to None.

        Returns:
            int: Integer as objects per n seconds loaded
        """
        return self._get_graphobjects_count_per_n_sec(
            n=n, timeframe=timeframe, object_type=object_type, target="Loaded"
        )

    def get_graphobjects_count_cached_per_n_sec(
        self, n: int = 1, timeframe: int = 120, object_type: str = None
    ) -> int:
        """[summary]

        Args:
            n (int, optional): Timeresolution in sec. Defaults to 1.
            timeframe (int, optional): Take last n seconds into account to calculate median value. Defaults to 20.
            object_type (str, optional): "Nodes" to only count Nodes per second, "Relations" to only count rels per second or None to count both. Defaults to None.

        Returns:
            int: Integer as objects per n seconds loaded
        """
        return self._get_graphobjects_count_per_n_sec(
            n=n, timeframe=timeframe, object_type=object_type, target="Cached"
        )

    def _get_graphobjects_count_per_n_sec(
        self,
        n: int = 1,
        timeframe: int = 120,
        object_type: str = None,
        target: str = "Loaded",
    ) -> int:
        """[summary]

        Args:
            n (int, optional): Timeresolution in sec. Defaults to 1.
            timeframe (int, optional): Take last n seconds into account to calculate median value. Defaults to 20.
            object_type (str, optional): "Nodes" to only count Nodes per second, "Relations" to only count rels per second or None to count both. Defaults to None.
            target (str, optional): Do you want to count graphsets loaded into the neo4j DB use "Loaded" or do you want to count cached graphobjects into the cache backend (e.g. redis) use "Cached". Defaults to "Loaded"
        Returns:
            int: Integer as objects per n seconds loaded
        """
        current_time = time.time()
        running_time = current_time - self.start_time
        if timeframe is None or running_time < timeframe:
            timeframe_start = self.start_time
        else:
            timeframe_start = current_time - timeframe
        relevant_data = OrderedDict()

        for timestamp, data in (
            self.graph_objects_loaded_counts_per_type_timeline.items()
            if target == "Loaded"
            else self.graph_objects_cached_counts_per_type_timeline.items()
        ):
            if timestamp > timeframe_start:
                relevant_data[timestamp] = data
        count_before_and_after = [0, 0]
        if len(relevant_data) == 0:
            return 0
        for index, data_position in enumerate([0, len(relevant_data) - 1]):
            count_all = 0
            report = list(relevant_data.values())[data_position]
            if object_type in [None, "Nodes"]:
                for graphobject_name, count in report["Nodes"].items():
                    count_all += count
            if object_type in [None, "Relations"]:
                for graphobject_name, count in report["Relations"].items():
                    count_all += count
            count_before_and_after[index] = count_all
        if len(relevant_data) < 2:
            count_before_and_after[0] = 0
        return ((count_before_and_after[1] - count_before_and_after[0]) / timeframe) * n

    def get_count_graphsets_loaded_per_n_sec(
        self,
        n: int = 1,
        timeframe: int = 120,
        graphset_type: Type[Union[graphio.NodeSet, graphio.RelationshipSet]] = None,
    ):
        current_time = time.time()
        running_time = current_time - self.start_time
        if timeframe is None or running_time < timeframe:
            timeframe_start = self.start_time
        else:
            timeframe_start = current_time - timeframe

        workers = []
        for timestamp, workers_in_slot in self.NodeSets_done_timeline.items():
            if timestamp > timeframe_start:
                if graphset_type is None or graphset_type == graphio.NodeSet:
                    workers.extend(workers_in_slot)
                if graphset_type is None or graphset_type == graphio.RelationshipSet:
                    # this is a little bit hacky but we know for sure that the keys in self.RelSets_done_timeline and self.NodeSets_done_timeline are always in sync
                    workers.extend(self.RelSets_done_timeline[timestamp])
        return (len(workers) / (current_time - timeframe_start)) * n

    def get_mean_count_graph_objects_in_cache(
        self,
        timeframe: int = 120,
        graphset_type: Type[Union[graphio.NodeSet, graphio.RelationshipSet]] = None,
    ) -> int:
        current_time = time.time()
        running_time = current_time - self.start_time

        if timeframe is None or running_time < timeframe:
            timeframe_start = self.start_time
        else:
            timeframe_start = current_time - timeframe

        relevant_data = []
        for (
            timestamp,
            graph_objects_count,
        ) in self.graph_objects_count_in_cache.items():
            if timestamp > timeframe_start:
                relevant_data.append(graph_objects_count)
        return round(statistics.mean(relevant_data))

    def get_count_queued_and_running_sourcing_workers(self) -> int:
        return len(
            self.manager.manager_sourcing._get_workers(status=("initial", "running"))
        )

    def get_count_left_sourcing_workers(self) -> int:
        return len(self.manager.manager_sourcing.workers)

    def get_memory_consumed_by_loaders(self):
        mem_total_bytes = 0
        for worker in self.manager.manager_loading._get_workers(status="running"):
            process = psutil.Process(worker.pid)
            mem_total_bytes += process.memory_info()[0]
        return mem_total_bytes

    def get_memory_consumed_by_sourcing_workers(self):
        mem_total_bytes = 0
        for worker in self.manager.manager_sourcing._get_workers(status="running"):
            process = psutil.Process(worker.pid)
            mem_total_bytes += process.memory_info()[0]
        return mem_total_bytes

    def get_memory_consumed_by_manager(self):
        process = psutil.Process(os.getpid())
        return process.memory_info()[0]

    def is_sourcing_phase_done(self):
        return self.manager.manager_sourcing.is_done()

    def get_memory_available(self):
        return getattr(psutil.virtual_memory(), "available")

    def get_memory_total(self):
        return getattr(psutil.virtual_memory(), "total")

    def get_memory_used(self):
        return getattr(psutil.virtual_memory(), "used")

    def get_cache_storage_total(self) -> int:
        return self.manager.strategy.cache_storage_total

    def get_cache_storage_available(self) -> int:
        return self.get_cache_storage_total() - self.get_cache_storage_used()

    def get_cache_storage_used(self) -> int:
        return self.manager.cache.storage_used()

    def get_cached_graphobjects_total_count(self, object_type: str = None) -> int:
        if not self.graph_objects_cached_counts_per_type_timeline:
            return 0
        last_count_stats = self.graph_objects_cached_counts_per_type_timeline[
            next(reversed(self.graph_objects_cached_counts_per_type_timeline))
        ]
        total_count = 0
        if object_type in [None, "Relations"]:
            for label, count in last_count_stats["Relations"].items():
                total_count += count
        if object_type in [None, "Nodes"]:
            for label, count in last_count_stats["Nodes"].items():
                total_count += count
        return total_count

    def get_loaded_graphobjects_total_count(self, object_type: str = None) -> int:
        if not self.graph_objects_loaded_counts_per_type_timeline:
            return 0
        last_count_stats = self.graph_objects_loaded_counts_per_type_timeline[
            next(reversed(self.graph_objects_loaded_counts_per_type_timeline))
        ]
        total_count = 0
        if object_type in [None, "Relations"]:
            for label, count in last_count_stats["Relations"].items():
                total_count += count
        if object_type in [None, "Nodes"]:
            for label, count in last_count_stats["Nodes"].items():
                total_count += count
        return total_count

    def get_cached_graphobjects_total_count_trend(
        self,
        timeframe: int = 60,
    ) -> int:
        current_time = time.time()
        running_time = current_time - self.start_time

        if timeframe is None or running_time < timeframe:
            timeframe_start = self.start_time
        else:
            timeframe_start = current_time - timeframe

        relevant_data = []
        for (
            timestamp,
            graph_objects_count,
        ) in self.graph_objects_mean_count_in_cache.items():
            if timestamp > timeframe_start:
                relevant_data.append(graph_objects_count)
        return self._trend(relevant_data)

    def get_cached_graphobjects_current(self) -> int:
        return (
            self.get_cached_graphobjects_total_count()
            - self.get_loaded_graphobjects_total_count()
        )

    def get_cache_storage_level(self) -> str:
        mem_full_perc = (
            self.get_cache_storage_used() * 100
        ) / self.get_cache_storage_total()
        if self.manager.strategy.cache_storage_clogged_limit <= mem_full_perc:
            return "RED"
        elif self.manager.strategy.cache_storage_warning_limit <= mem_full_perc:
            return "ORANGE"
        else:
            return "GREEN"

    def get_cache_storage_used_by_relSets(self):
        size = 0
        for rel_meta in self.manager.cache.list_SetsMeta(
            set_type=graphio.RelationshipSet
        ):
            size += rel_meta.total_size_bytes
        return size

    def get_cache_storage_used_by_nodeSets(self):
        size = 0
        for rel_meta in self.manager.cache.list_SetsMeta(set_type=graphio.NodeSet):
            size += rel_meta.total_size_bytes
        return size

    def get_node_types_by_insert_time(self, top_n_only=None) -> OrderedDict:
        worker_timings = OrderedDict()
        workers: list[WorkerLoading] = self.manager.manager_loading.finished_workers
        for worker in workers:
            if worker.set_meta.type == graphio.NodeSet:
                node_labels = ":".join(worker.set_meta.labels)
                if node_labels in worker_timings:
                    worker_timings[node_labels] += worker.timer.took
                else:
                    worker_timings[node_labels] = worker.timer.took
        rel_times = OrderedDict(
            reversed(sorted(worker_timings.items(), key=lambda item: item[1]))
        )
        if top_n_only:
            return OrderedDict(list(rel_times.items())[:top_n_only])
        return rel_times

    def get_relation_types_by_insert_time(self, top_n_only=None) -> OrderedDict:
        worker_timings = OrderedDict()
        workers: list[WorkerLoading] = self.manager.manager_loading.finished_workers
        for worker in workers:
            if worker.set_meta.type == graphio.RelationshipSet:
                if worker.set_meta.rel_type in worker_timings:
                    worker_timings[worker.set_meta.rel_type] += worker.timer.took
                else:
                    worker_timings[worker.set_meta.rel_type] = worker.timer.took
        rel_times = OrderedDict(
            reversed(sorted(worker_timings.items(), key=lambda item: item[1]))
        )
        if top_n_only:
            return OrderedDict(list(rel_times.items())[:top_n_only])
        return rel_times

    def get_last_cache_open_duration_in_sec(self) -> float:
        found_end_of_last_closing = False
        beginning_time_of_last_closing = None
        beginning_time_of_last_opening = None
        for timestamp, cache_open_status in reversed(
            self.cache_store_status_timeline.items()
        ):
            if not cache_open_status and not found_end_of_last_closing:
                found_end_of_last_closing = True
            elif (
                cache_open_status
                and found_end_of_last_closing
                and not beginning_time_of_last_closing
            ):
                # we found the beginning of last closing
                beginning_time_of_last_closing = timestamp
            elif (
                beginning_time_of_last_closing
                and not beginning_time_of_last_opening
                and not cache_open_status
            ):
                # we found the beginning of last opening
                beginning_time_of_last_opening = timestamp
                break
        if not beginning_time_of_last_closing or not beginning_time_of_last_opening:
            # there was no cache store closing until now. we dont havy measurements
            return None
        return beginning_time_of_last_closing - beginning_time_of_last_opening

    def get_report(self):
        report = {}

        report["General"] = {}

        gen_rep = report["General"]

        gen_rep["running_time_sec"] = {
            "val": time.time() - self.start_time,
            "desc": "Running time",
            "humanfriendly_transformer": humanfriendly.format_timespan,
        }

        gen_rep["max_processes_count"] = {
            "val": self.manager.strategy.max_processes_count,
            "desc": "Max processes count",
        }

        gen_rep["management_tick_per_sec"] = {
            "val": self.get_management_ticks_per_n_sec(),
            "desc": "Management ticks per second",
            "humanfriendly_transformer": "{:.2f}/s".format,
        }

        report["Sourcing"] = {}

        src_rep = report["Sourcing"]

        src_rep["cores_avail_no"] = {
            "val": self.manager.strategy.amount_sourcing_cores(),
            "desc": "Sourcing Workers amount of cores allocated",
        }
        src_rep["workers_total_no"] = {
            "val": self.manager.manager_sourcing.worker_count_total,
            "desc": "Sourcing Workers amount total",
        }

        src_rep["workers_fin_no"] = {
            "val": len(self.manager.manager_sourcing.finished_workers),
            "desc": "Sourcing Workers amount finished",
        }

        src_rep["workers_running_no"] = {
            "val": len(self.manager.manager_sourcing._get_workers(status="running")),
            "desc": "Sourcing Workers amount running",
        }

        report["Cache"] = {}

        cache_rep = report["Cache"]

        cache_rep["relSet_no"] = {
            "val": len(self.manager.cache.list_SetsMeta(graphio.RelationshipSet)),
            "desc": "RelationSets count in cache",
        }
        cache_rep["relSet_size"] = {
            "val": self.get_cache_storage_used_by_relSets(),
            "desc": "RelationSets size in cache",
            "humanfriendly_transformer": humanfriendly.format_size,
        }

        cache_rep["rels_per_sec"] = {
            "val": self.get_graphobjects_count_cached_per_n_sec(
                object_type="Relations"
            ),
            "desc": "Relations cached per sec",
            "humanfriendly_transformer": "{:.2f}/s".format,
        }

        cache_rep["nodeSet_no"] = {
            "val": len(self.manager.cache.list_SetsMeta(graphio.NodeSet)),
            "desc": "NodeSets count in cache",
        }
        cache_rep["nodeSet_size"] = {
            "val": self.get_cache_storage_used_by_nodeSets(),
            "desc": "NodeSets size in cache",
            "humanfriendly_transformer": humanfriendly.format_size,
        }

        cache_rep["nodes_per_sec"] = {
            "val": self.get_graphobjects_count_cached_per_n_sec(object_type="Nodes"),
            "desc": "Nodes cached per sec",
            "humanfriendly_transformer": "{:.2f}/s".format,
        }
        #

        cache_rep["cache_storage_status"] = {
            "val": self.get_cache_storage_level(),
            "desc": "Cache storage health status",
        }

        cache_storage_level_details = f"{int(100 - ((self.get_cache_storage_used() * 100) / self.get_cache_storage_total()))}% Free ({humanfriendly.format_size(self.get_cache_storage_used())} used of {humanfriendly.format_size(self.get_cache_storage_total())})"

        cache_rep["cache_storage_status_details"] = {
            "val": cache_storage_level_details,
            "desc": "Cache storage status details",
        }

        report["Loading"] = {}

        load_rep = report["Loading"]

        load_rep["cores_avail_no"] = {
            "val": self.manager.strategy.amount_loading_cores(),
            "desc": "Loading Workers amount of cores allocated",
        }
        load_rep["workers_running_no"] = {
            "val": len(self.manager.manager_loading._get_workers(status="running")),
            "desc": "Loading Workers amount running",
        }
        load_rep["workers_fin_no"] = {
            "val": len(self.manager.manager_loading.finished_workers),
            "desc": "Loading Workers amount finished",
        }

        load_rep["workers_relsets_run_no"] = {
            "val": len(
                self.manager.manager_loading._get_workers(
                    status=("running"),
                    tag=self.manager.manager_loading.worker_tag_relsets,
                )
            ),
            "desc": "Loading RelSets Workers amount running",
        }

        load_rep["workers_relsets_fin_no"] = {
            "val": len(
                self.manager.manager_loading._get_workers(
                    progress=Progress.COMPLETE,
                    tag=self.manager.manager_loading.worker_tag_relsets,
                )
            ),
            "desc": "Loading RelSets Workers amount finished",
        }

        load_rep["workers_relsets_wait_no"] = {
            "val": len(
                self.manager.manager_loading._get_workers(
                    progress=Progress.DRAIN_ORDERED,
                    tag=self.manager.manager_loading.worker_tag_relsets,
                )
            ),
            "desc": "RelSets Workers waiting for NodeSet drain",
        }

        load_rep["labels_blocked_for_rels"] = {
            "val": len(self.manager._get_blocked_labels()),
            "desc": "Amount of labels blocked for relation loading",
        }

        load_rep["relSet_per_sec"] = {
            "val": self.get_count_graphsets_loaded_per_n_sec(
                graphset_type=graphio.RelationshipSet
            ),
            "desc": "RelationSets loaded per sec",
            "humanfriendly_transformer": "{:.2f}/s".format,
        }

        load_rep["rels_per_sec"] = {
            "val": self.get_graphobjects_count_loaded_per_n_sec(
                object_type="Relations"
            ),
            "desc": "Relations loaded per sec",
            "humanfriendly_transformer": "{:.2f}/s".format,
        }

        load_rep["workers_relsets_run_no"] = {
            "val": len(
                self.manager.manager_loading._get_workers(
                    status=("running"),
                    tag=self.manager.manager_loading.worker_tag_relsets,
                )
            ),
            "desc": "Loading RelSets Workers amount running",
        }

        load_rep["workers_NodeSets_run_no"] = {
            "val": len(
                self.manager.manager_loading._get_workers(
                    progress=(Progress.QUEUED, Progress.LOADING),
                    tag=self.manager.manager_loading.worker_tag_nodesets,
                )
            ),
            "desc": "Loading NodeSets Workers running or queded",
        }

        load_rep["workers_NodeSets_fin_no"] = {
            "val": len(
                self.manager.manager_loading._get_workers(
                    progress=Progress.COMPLETE,
                    tag=self.manager.manager_loading.worker_tag_nodesets,
                )
            ),
            "desc": "Loading NodeSets Workers amount finished",
        }

        load_rep["nodeSet_per_sec"] = {
            "val": self.get_count_graphsets_loaded_per_n_sec(
                graphset_type=graphio.NodeSet
            ),
            "desc": "NodeSets loaded per sec",
            "humanfriendly_transformer": "{:.2f}/s".format,
        }

        load_rep["nodes_per_sec"] = {
            "val": self.get_graphobjects_count_loaded_per_n_sec(object_type="Nodes"),
            "desc": "Nodes loaded per sec",
            "humanfriendly_transformer": "{:.2f}/s".format,
        }

        load_rep["nodes_types_insert_timings"] = {
            "val": self.get_node_types_by_insert_time(5),
            "desc": "Top5 insertion times by node type",
            "humanfriendly_transformer": lambda val: self._dict_report_style(
                val, val_formater="{:.2f} sec".format
            ),
        }

        load_rep["reltypes_insert_timings"] = {
            "val": self.get_relation_types_by_insert_time(5),
            "desc": "Top5 insertion times by rel type",
            "humanfriendly_transformer": lambda val: self._dict_report_style(
                val, val_formater="{:.2f} sec".format
            ),
        }

        report["SyncControl"] = {}
        sync_rep = report["SyncControl"]

        sync_rep["sourcing_paused"] = {
            "val": str(not self.manager.cache.store_is_available()),
            "desc": "Sourcing is paused to let loading catch up",
        }

        sync_rep["last_sourcing_open_duration"] = {
            "val": self.manager.statistics.get_last_cache_open_duration_in_sec(),
            "desc": "Duration between last 2 pauses",
            "humanfriendly_transformer": lambda val: "{:.2f} sec".format(val)
            if val is not None
            else "n/a",
        }

        sync_rep["cached_total"] = {
            "val": self.get_cached_graphobjects_total_count(),
            "desc": "Count of Graphobjects inserted into cache",
            "humanfriendly_transformer": humanfriendly.format_number,
        }

        sync_rep["loaded_total"] = {
            "val": self.get_loaded_graphobjects_total_count(),
            "desc": "Count of Graphobjects loaded into Neo4j",
            "humanfriendly_transformer": humanfriendly.format_number,
        }

        sync_rep["cache_to_load_advantage_count_current"] = {
            "val": sync_rep["cached_total"]["val"] - sync_rep["loaded_total"]["val"],
            "desc": "Current cached graphobjects",
            "humanfriendly_transformer": humanfriendly.format_number,
        }

        sync_rep["cached_graphobjects_count"] = {
            "val": self.get_mean_count_graph_objects_in_cache(),
            "desc": "Mean cached graphobjects count",
            "humanfriendly_transformer": humanfriendly.format_number,
        }

        sync_rep["max_cached_graphobjects_count"] = {
            "val": self.manager.strategy.max_graphobjects_count_in_cache,
            "desc": "Max graphobjects cache count before pausing sourcing workers",
            "humanfriendly_transformer": humanfriendly.format_number,
        }

        sync_rep["min_cached_graphobjects_count"] = {
            "val": self.manager.strategy.min_graphobjects_count_in_cache,
            "desc": "Min graphobjects cache count",
            "humanfriendly_transformer": humanfriendly.format_number,
        }
        sync_rep["cache_to_load_advantage"] = {
            "val": (
                (
                    (sync_rep["cached_total"]["val"] / sync_rep["loaded_total"]["val"])
                    * 100
                )
                - 100
            )
            if sync_rep["loaded_total"]["val"] not in [None, 0]
            else 0,
            "desc": "Percental advantage of cached to loaded graphobjects",
            "humanfriendly_transformer": "{:.2f} %".format,
        }

        sync_rep["cache_level_trend"] = {
            "val": self.get_cached_graphobjects_total_count_trend(),
            "desc": "Trend of cache level (+=filling,-=drying)",
            "humanfriendly_transformer": "{:.2f}°".format,
        }

        report["Memory"] = {}
        mem_rep = report["Memory"]

        mem_rep = report["Memory"]

        memory_status = f"{humanfriendly.format_size(self.get_memory_available())} available - {humanfriendly.format_size(self.get_memory_used())} used of {humanfriendly.format_size(self.get_memory_total())}"

        mem_rep["memory_status_details"] = {
            "val": memory_status,
            "desc": "Memory status for Manager and Workers processes",
        }

        mem_rep["memory_used_by_manager"] = {
            "val": self.get_memory_consumed_by_manager(),
            "desc": "Memory used by the manager process",
            "humanfriendly_transformer": humanfriendly.format_size,
        }

        mem_rep["memory_used_by_sourcing_workers"] = {
            "val": self.get_memory_consumed_by_sourcing_workers(),
            "desc": "Memory used by the sourcing processes",
            "humanfriendly_transformer": humanfriendly.format_size,
        }

        mem_rep["memory_used_by_loading_workers"] = {
            "val": self.get_memory_consumed_by_loaders(),
            "desc": "Memory used by the loading processes",
            "humanfriendly_transformer": humanfriendly.format_size,
        }

        return report

    def get_human_readable_report(self):

        report = self.get_report()

        report_str = "\n"
        for title, chapters in report.items():
            report_str += f"## {title}\n"
            longest_chapter_desc_length: int = max(
                [len(chapter["desc"]) for chapter in chapters.values()]
            )
            for key, chapter in chapters.items():
                if "humanfriendly_transformer" in chapter:
                    val = chapter["humanfriendly_transformer"](chapter["val"])
                else:
                    val = chapter["val"]
                if isinstance(val, str) and "\n" in val:
                    multiline_val = ""
                    for index, line_val in enumerate(val.split("\n")):
                        if index > 0:
                            line = "\t{:" + str(longest_chapter_desc_length) + "}  {}"
                            line = line.format(" ", line_val)
                        else:
                            line = line_val

                        multiline_val += line + "\n"
                    val = multiline_val.strip("\n")
                row = "\t{:" + str(longest_chapter_desc_length) + "}: {}\n"
                report_str += row.format(chapter["desc"], val)

        return report_str

    @classmethod
    def _trend(cls, data: dict) -> float:
        """Return the trend of a number list in degree.
        0 = no trend
        postive number (max 90) = numbers go upwarts
        negative number (min -90) = numbers trending downwards

        Args:
            data (list): e.g. [1,34,564,1,23]

        Returns:
            int: trend as a degree number between -90 to 90
        """
        if len(data) > 1 and max(data) > 0:
            # generate x-axis data based on the max value to get relative trends compared to the amount of data
            maximum = max(data)
            x_axis = list(numpy.arange(0, maximum, maximum / len(data)))
            # dirty fix to avoid rounding errors
            if len(x_axis) > len(data):
                print("DATA TOO SHOORT")
                data.insert(data[0], 0)
            elif len(x_axis) < len(data):
                print("DATA TOO LOONG")
                data.pop(0)
            coeffs = numpy.polynomial.polynomial.Polynomial.fit(
                x_axis,
                list(data),
                1,
            )
            coeffs_convert = coeffs.convert().coef
            try:
                slope = list(coeffs_convert)[1]
            except:
                slope = 0
            angle_rad = math.atan(slope)
            angle_deg = math.degrees(angle_rad)
            return float(angle_deg)
        else:
            return 0

    @classmethod
    def _dict_report_style(cls, dic, val_formater=None) -> str:
        s = ""
        for key, val in dic.items():
            if val_formater:
                value = val_formater(val)
            else:
                value = val
            s += f"{key}: {value}\n"
        return s
