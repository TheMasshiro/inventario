from abc import ABC, abstractmethod
from typing import Any

from flask import render_template, request


class AnalyticsInterface(ABC):
    @abstractmethod
    def analytics(self) -> Any:
        pass


class AnalyticsManager(AnalyticsInterface):
    def analytics(self) -> Any:
        if request.method == "GET":
            return render_template("main/analytics.html", title="Analytics")
        return render_template("main/analytics.html", title="Analytics")
