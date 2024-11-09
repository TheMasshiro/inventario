from abc import ABC, abstractmethod
from datetime import date
from typing import Any

from flask import flash, redirect, render_template, request, url_for

from app.helpers import format_currency
from app.inventory_forms import ProductForm
from app.inventory_models import Inventory


class InventoryInterface(ABC):
    @abstractmethod
    def purchase(self) -> Any:
        pass

    @abstractmethod
    def inventory(self) -> Any:
        pass

    @abstractmethod
    def edit_product(self, product_id) -> Any:
        pass

    @abstractmethod
    def remove_product(self, product_id) -> Any:
        pass

    @abstractmethod
    def analytics(self) -> Any:
        pass

    @abstractmethod
    def suppliers(self) -> Any:
        pass

    @abstractmethod
    def about(self) -> Any:
        pass


class InventoryManager(InventoryInterface):
    def purchase(self) -> Any:
        if request.method == "GET":
            return render_template("main/purchase.html", title="Purchase")
        return render_template("main/purchase.html", title="Purchase")

    def inventory(self) -> Any:
        user_inventory = Inventory()
        page = request.args.get("page", 1, type=int)
        ITEMS_PER_PAGE = 10

        add_form = ProductForm()

        if request.method == "GET":
            total_items = user_inventory.get_total_items()
            total_pages = max(1, (total_items + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE)
            page = max(1, min(page, total_pages))

            if total_pages <= 5:
                start_page = 1
                end_page = total_pages
            else:
                start_page = max(1, page - 2)
                end_page = min(total_pages, page + 2)

                if start_page == 1:
                    end_page = 5
                elif end_page == total_pages:
                    start_page = total_pages - 4

            offset = (page - 1) * ITEMS_PER_PAGE
            products = user_inventory.get_all_paginated_items(offset, ITEMS_PER_PAGE)

            return render_template(
                "main/inventory.html",
                title="Inventory",
                products=products,
                format_currency=format_currency,
                page=page,
                total_pages=total_pages,
                start_page=start_page,
                end_page=end_page,
                form=add_form,
            )

        if add_form.validate_on_submit():
            current_date = date.today().strftime("%d-%m-%Y")

            add_item = user_inventory.add_item(
                add_form.product_name.data,
                add_form.price.data,
                add_form.quantity.data,
                add_form.supplier_name.data,
                current_date,
            )

            if add_item:
                flash(f"{add_form.product_name.data} Added to Inventory", "success")

        return redirect(url_for("main.inventory"))

    def edit_product(self, product_id: int | None = None) -> Any:
        user_inventory = Inventory()
        form = ProductForm()
        product = user_inventory.get_item(product_id)

        if product is None:
            return redirect(url_for("main.inventory"))

        if form.validate_on_submit():
            current_date = date.today().strftime("%d-%m-%Y")

            edit_item = user_inventory.edit_item(
                product_id,
                form.product_name.data,
                form.price.data,
                form.quantity.data,
                form.supplier_name.data,
                current_date,
            )

            if edit_item:
                flash(f"{form.product_name.data} updated successfully", "success")

        return redirect(url_for("main.inventory"))

    def remove_product(self, product_id) -> Any:
        user_inventory = Inventory()
        product = user_inventory.get_item(product_id)

        if product is None:
            return redirect(url_for("main.inventory"))

        if user_inventory.remove_item(product_id):
            flash("Product removed successfully", "success")

        return redirect(url_for("main.inventory"))

    def analytics(self) -> Any:
        if request.method == "GET":
            return render_template("main/analytics.html", title="Analytics")
        return render_template("main/analytics.html", title="Analytics")

    def suppliers(self) -> Any:
        if request.method == "GET":
            return render_template("main/suppliers.html", title="Suppliers")
        return render_template("main/suppliers.html", title="Suppliers")

    def about(self) -> Any:
        if request.method == "GET":
            return render_template("main/about.html", title="About")
        return render_template("main/about.html", title="About")
