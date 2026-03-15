# -*- coding: utf-8 -*-

import gc
import threading
from typing import Any


class GCMonitor:
    """Tool for monitoring gc performance.

    Maybe it will be added to the library itself.
    """

    def __init__(
        self,
        interval: int = 60,
    ) -> None:
        """Init.

        Args:
            interval (int): Monitoring interval
        """
        self.interval = interval
        self._prev = gc.get_stats()
        self.__stop = threading.Event()

    def send_metric(self, metric: Any) -> None:
        """Method for sending metrics.

        Can be overridden, for example, to work with Prometheus.
        """
        print(metric)

    def start(self) -> None:
        """Start monitoring."""
        threading.Thread(target=self.__run, daemon=True).start()

    def __run(self):
        while not self.__stop.wait(self.interval):
            curr = gc.get_stats()
            print(f"GC (last: {self.interval}s): ")
            for i in range(len(curr)):
                c = curr[i]["collections"] - self._prev[i]["collections"]
                self.send_metric(f"Gen{i}: {c} runs")
            self._prev = curr
