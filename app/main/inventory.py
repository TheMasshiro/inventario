from abc import ABC, abstractmethod
from typing import Any

from flask import render_template, request

from app.inventory_models import Inventory


class InventoryInterface(ABC):
    @abstractmethod
    def inventory(self) -> Any:
        pass

    @abstractmethod
    def analytics(self) -> Any:
        pass

    @abstractmethod
    def about(self) -> Any:
        pass


class InventoryManager(InventoryInterface):
    def inventory(self) -> Any:
        user_inventory = Inventory()

        if request.method == "GET":
            user_inventory.get_item()
            return render_template("main/inventory.html", title="Inventory")

        page = request.args.get("page", 1, type=int)

        return render_template("main/inventory.html", title="Inventory")

    def analytics(self) -> Any:
        if request.method == "GET":
            return render_template("main/analytics.html", title="Analytics")
        return render_template("main/analytics.html", title="Analytics")

    def about(self) -> Any:
        if request.method == "GET":
            return render_template("main/about.html", title="About")
        return render_template("main/about.html", title="About")
