from abc import ABC, abstractmethod
from typing import Any

from flask import flash, redirect, render_template, request, url_for

from app.forms.customer_forms import PurchaseForm
from app.helpers import format_currency
from app.models.customer_models import Customers
from app.models.inventory_models import Inventory, Purchase


class PurchaseInterface(ABC):
    @abstractmethod
    def purchase(self) -> None:
        pass

    @abstractmethod
    def search_product(self) -> Any:
        pass


class PurchaseManager(PurchaseInterface):
    def purchase(self) -> Any:
        products = Inventory().get_products()
        customers = Customers().get_customers()
        form = PurchaseForm()

        if customers is None:
            customers = []

        current_customers = []
        for customer in customers:
            current_customers.append(customer["customer_name"])

        form.customer_name.choices = current_customers

        if request.method == "GET":
            return render_template(
                "main/purchase.html",
                title="Purchase",
                products=products,
                format_currency=format_currency,
                form=form,
            )

        if form.validate_on_submit():
            product_ids = request.form.getlist("product_id")
            quantities = request.form.getlist("quantity")
            product = Purchase()

            item_bought = False

            for product_id, quantity in zip(product_ids, quantities):
                if int(quantity) <= 0:
                    continue
                item_bought = product.buy(product_id, quantity)

            if item_bought:
                flash(
                    f"Purchase successful for {form.customer_name.data}",
                    "success-purchase",
                )
            else:
                flash("Purchase failed", "danger-purchase")

        return redirect(url_for("main.purchase"))

    def search_product(self) -> Any:
        query = request.args.get("q", "")
        user_inventory = Inventory()
        products = user_inventory.search_product(query)

        return render_template(
            "partials/purchase_rows.html",
            products=products,
            format_currency=format_currency,
        )
