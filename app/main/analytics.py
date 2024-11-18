from abc import ABC, abstractmethod
from typing import Any

from flask import flash, redirect, render_template, request, url_for

from app.forms.customer_forms import CustomerForm
from app.models.customer_models import Customers


class AnalyticsInterface(ABC):
    @abstractmethod
    def analytics(self) -> Any:
        pass

    @abstractmethod
    def customers(self) -> Any:
        pass

    @abstractmethod
    def edit_customer(self, customer_id) -> Any:
        pass

    @abstractmethod
    def remove_customer(self, customer_id) -> Any:
        pass

    @abstractmethod
    def search_customer(self) -> Any:
        pass


class AnalyticsManager(AnalyticsInterface):
    def analytics(self) -> Any:
        if request.method == "GET":
            return render_template("main/analytics.html", title="Analytics")
        return render_template("main/analytics.html", title="Analytics")

    def customers(self) -> Any:
        user_customer = Customers()
        form = CustomerForm()

        customers = user_customer.get_customers()

        if request.method == "GET":
            return render_template(
                "main/customers.html",
                title="Customers",
                customers=customers,
                form=form,
            )

        if form.validate_on_submit():
            customer_name = form.customer_name.data

            if not customer_name:
                flash("Invalid customer name", "danger-customer")
                return redirect(url_for("main.customers"))

            existing_customer = user_customer.get_customer_by_name(customer_name)
            if (
                existing_customer
                and existing_customer["customer_name"].strip().lower()
                == customer_name.strip().lower()
            ):
                flash("Customer already exists", "danger-customer")
                return redirect(url_for("main.customers"))

            add_customer = user_customer.add_customer(
                customer_name,
            )

            if add_customer:
                flash(f"{customer_name} added successfully", "success-customer")
            else:
                flash("Customer already exists", "danger-customer")

        else:
            flash("Invalid customer name", "danger-customer")

        return redirect(url_for("main.customers"))

    def edit_customer(self, customer_id) -> Any:
        user_customer = Customers()
        form = CustomerForm()

        customer = user_customer.get_customer(customer_id)
        if customer is None:
            flash("Customer does not exist", "danger-customer")
            return redirect(url_for("main.customers"))

        if form.validate_on_submit():
            new_customer_name = form.customer_name.data
            if not new_customer_name:
                flash("Customer name cannot be empty", "danger-customer")
                return redirect(url_for("main.customers"))

            existing_customer = user_customer.get_customer_by_name(new_customer_name)
            if (
                existing_customer
                and existing_customer["customer_name"].strip().lower()
                == new_customer_name.strip().lower()
            ):
                flash("Customer already exists", "danger-customer")
                return redirect(url_for("main.customers"))

            if user_customer.edit_customer(customer_id, new_customer_name):
                flash(f"{customer[2]} updated successfully", "success-customer")
            else:
                flash("Failed to update customer", "danger-customer")
        else:
            flash("Invalid customer name", "danger-customer")

        return redirect(url_for("main.customers"))

    def remove_customer(self, customer_id) -> Any:
        user_customer = Customers()
        customer = user_customer.get_customer(customer_id)

        if customer is None:
            flash("Customer does not exist", "danger-customer")
            return redirect(url_for("main.customers"))

        if user_customer.remove_customer(customer_id):
            flash(f"{customer[2]} removed successfully", "success-customer")
        else:
            flash("Customer does not exist", "danger-customer")

        return redirect(url_for("main.customers"))

    def search_customer(self) -> Any:
        query = request.args.get("q", "")
        user_customer = Customers()
        customers = user_customer.search_customer(query)

        return render_template(
            "partials/customer_rows.html",
            customers=customers,
        )
