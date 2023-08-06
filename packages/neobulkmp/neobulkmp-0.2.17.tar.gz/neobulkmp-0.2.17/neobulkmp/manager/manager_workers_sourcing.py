import logging
import graphio
from typing import List, Dict, Type, Set, TYPE_CHECKING
from ..worker_base import WorkerBase, Progress
from .manager_workers_base import ManagerWorkersBase


if TYPE_CHECKING:
    from .manager import Manager

log = logging.getLogger(__name__)


class ManagerWorkersSourcing(ManagerWorkersBase):
    def __init__(self, manager: "Manager", worker_class: Type[WorkerBase]):
        super(type(self), self).__init__(manager, worker_class)
        # create workers distribute task parameters per worker
        log.debug(f"self.parent.worker_parameters: {self.parent.worker_parameters}")
        self._init_workers(parameters=self.parent.worker_parameters)
        self.worker_count_total = len(self.workers)
        self.cache_untouched = True

    def is_done(self):
        # Mom, Are We There Yet?
        if self.worker_count_total == len(self.finished_workers + self.failed_workers):

            return True
        else:
            return False

    def manage(self):

        available_cores = self.parent.strategy.amount_sourcing_cores()

        # Collect all running sourcing workers
        waiting_workers = self._get_workers(progress=Progress.QUEUED)
        # Start next worker
        if (
            len(self._get_workers(progress=Progress.LOADING)) < available_cores
            and len(waiting_workers) > 0
        ):
            next_worker = waiting_workers.pop(0)
            log.debug(f"CALL START ON SOURCING {next_worker} - {next_worker.params}")
            next_worker.progress = Progress.LOADING
            next_worker.start()
            next_worker.timer.__enter__()

        self._finish_workers()
