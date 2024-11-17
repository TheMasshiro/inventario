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
            product = user_inventory.get_item_by_name(form.product_name.data)

            product_name = form.product_name.data
            price = form.price.data
            stock = form.stock.data
            supplier_name = form.supplier_name.data

            if product_name is None:
                flash(
                    f"{form.product_name.data} does not exist in the inventory",
                    "danger-inventory",
                )
                return redirect(url_for("main.inventory"))

            if (
                supplier_name.strip().lower() == product[5].strip().lower()
                and product_name.strip().lower() == product[1].strip().lower()
            ):
                flash(
                    f"{form.product_name.data} already exists in the inventory",
                    "danger-inventory",
                )
                return redirect(url_for("main.inventory"))

            add_item = user_inventory.add_item(
                product_name, price, stock, current_date, supplier_name
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

        product_by_id = user_inventory.get_item(product_id)
        if product_by_id is None:
            flash("Product not found", "danger-inventory")
            return redirect(url_for("main.inventory"))

        companies = [
            company["company_name"]
            for company in user_inventory.get_supplier_companies()
        ]
        form.supplier_name.choices = companies

        if form.validate_on_submit():
            current_date = date.today().strftime("%d-%m-%Y")

            new_product_name = form.product_name.data
            new_price = form.price.data
            new_stock = form.stock.data
            new_supplier_name = form.supplier_name.data

            if not new_product_name:
                flash("Product name cannot be empty", "danger-inventory")
                return redirect(url_for("main.inventory"))

            existing_product = user_inventory.get_item_by_name_and_supplier(
                new_product_name, new_supplier_name
            )

            if existing_product and existing_product[0] != product_id:
                flash(
                    f"{new_product_name} already exists for the supplier {new_supplier_name}",
                    "danger-inventory",
                )
                return redirect(url_for("main.inventory"))

            edit_item = user_inventory.edit_item(
                product_id,
                new_product_name,
                new_price,
                new_stock,
                current_date,
                new_supplier_name,
            )

            if edit_item:
                flash(
                    f"Successfully updated '{new_product_name}'",
                    "success-inventory",
                )
            else:
                flash(
                    f"Failed to update '{new_product_name}'. {form.errors}.",
                    "danger-inventory",
                )
        else:
            flash(
                f"Failed to update '{form.product_name.data}'. {form.errors}.",
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
