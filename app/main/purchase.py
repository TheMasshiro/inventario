from abc import ABC, abstractmethod
from typing import Any

from flask import render_template, request


class PurchaseInterface(ABC):
    @abstractmethod
    def purchase(self) -> None:
        pass


class PurchaseManager(PurchaseInterface):
    def purchase(self) -> Any:
        if request.method == "GET":
            return render_template("main/purchase.html", title="Purchase")
        return render_template("main/purchase.html", title="Purchase")
