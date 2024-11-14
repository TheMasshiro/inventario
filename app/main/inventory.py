from abc import ABC, abstractmethod
from datetime import date
from typing import Any

from flask import flash, redirect, render_template, request, url_for

from app.forms.inventory_forms import ProductForm
from app.helpers import format_currency, paginate_inventory
from app.models.inventory_models import Inventory


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
        form = ProductForm()

        pagination = paginate_inventory(page, user_inventory)
        companies = []
        for company in user_inventory.get_supplier_companies():
            companies.append(company["company_name"])

        form.supplier_name.choices = companies

        if request.method == "GET":
            return render_template(
                "main/inventory.html",
                title="Inventory",
                products=pagination[0],
                format_currency=format_currency,
                page=page,
                start_page=pagination[1],
                end_page=pagination[2],
                total_pages=pagination[3],
                form=form,
            )

        if form.validate_on_submit():
            current_date = date.today().strftime("%d-%m-%Y")

            add_item = user_inventory.add_item(
                form.product_name.data,
                form.price.data,
                form.stock.data,
                current_date,
                form.supplier_name.data,
            )

            if add_item:
                flash(
                    f"{form.product_name.data} added to inventory",
                    "success-inventory",
                )
            else:
                flash(
                    f"Failed to add {form.product_name.data} to the inventory. {form.errors}.",
                    "danger-inventory",
                )
        else:
            flash(
                f"Failed to add {form.product_name.data} to the inventory. {form.errors}.",
                "danger-inventory",
            )

        return redirect(url_for("main.inventory"))

    def edit_product(self, product_id: int | None = None) -> Any:
        user_inventory = Inventory()
        form = ProductForm()
        product = user_inventory.get_item(product_id)

        if product is None:
            return redirect(url_for("main.inventory"))

        companies = []
        for company in user_inventory.get_supplier_companies():
            companies.append(company["company_name"])

        form.supplier_name.choices = companies

        if form.validate_on_submit():
            current_date = date.today().strftime("%d-%m-%Y")

            edit_item = user_inventory.edit_item(
                product_id,
                form.product_name.data,
                form.price.data,
                form.stock.data,
                current_date,
                form.supplier_name.data,
            )

            if edit_item:
                flash(
                    f"{product[1]} updated to {form.product_name.data}",
                    "success-inventory",
                )
            else:
                flash(
                    f"Failed to update {form.product_name.data}. {form.errors}.",
                    "danger-inventory",
                )
        else:
            flash(
                f"Failed to update {form.product_name.data}. {form.errors}.",
                "danger-inventory",
            )

        return redirect(url_for("main.inventory"))

    def remove_product(self, product_id) -> Any:
        user_inventory = Inventory()
        product = user_inventory.get_item(product_id)

        if product is None:
            return redirect(url_for("main.inventory"))

        if user_inventory.remove_item(product_id):
            flash(f"{product[1]} removed from inventory", "success-inventory")
        else:
            flash(f"Failed to remove {product[1]} from inventory", "danger-inventory")

        return redirect(url_for("main.inventory"))

    def analytics(self) -> Any:
        if request.method == "GET":
            return render_template("main/analytics.html", title="Analytics")
        return render_template("main/analytics.html", title="Analytics")

    def about(self) -> Any:
        if request.method == "GET":
            return render_template("main/about.html", title="About")
        return render_template("main/about.html", title="About")
