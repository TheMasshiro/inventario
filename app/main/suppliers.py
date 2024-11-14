from abc import ABC, abstractmethod
from typing import Any

from flask import flash, redirect, render_template, request, url_for

from app.forms.supplier_forms import SupplierForm
from app.helpers import error_messages, paginate_suppliers
from app.models.supplier_models import Suppliers


class SuppliersInterface(ABC):
    @abstractmethod
    def suppliers(self) -> Any:
        pass

    @abstractmethod
    def edit_suppliers(self, supplier_id) -> Any:
        pass

    @abstractmethod
    def remove_suppliers(self, supplier_id) -> Any:
        pass


class SuppliersManager(SuppliersInterface):
    def suppliers(self) -> Any:
        user_supplier = Suppliers()
        page = request.args.get("page", 1, type=int)
        form = SupplierForm()

        pagination = paginate_suppliers(page, user_supplier)

        if request.method == "GET":
            return render_template(
                "main/suppliers.html",
                title="Suppliers",
                suppliers=pagination[0],
                page=page,
                start_page=pagination[1],
                end_page=pagination[2],
                total_pages=pagination[3],
                form=form,
            )

        if form.validate_on_submit():
            add_supplier = user_supplier.add_supplier(
                form.company_name.data,
                form.supplier_name.data,
                form.email.data,
                form.phone.data,
                form.status.data,
            )

            if add_supplier:
                flash(
                    f"{form.supplier_name.data} from {form.company_name.data} added to Suppliers",
                    "success-supplier",
                )
            else:
                flash(
                    f"Failed to add {form.company_name.data} to the suppliers list. {error_messages(form)}.",
                    "danger-supplier",
                )
        else:
            flash(
                f"Failed to add {form.company_name.data} to the suppliers list. {error_messages(form)}.",
                "danger-supplier",
            )

        return redirect(url_for("main.suppliers"))

    def edit_suppliers(self, supplier_id) -> Any:
        user_supplier = Suppliers()
        form = SupplierForm()
        supplier = user_supplier.get_supplier(supplier_id)

        if supplier is None:
            return redirect(url_for("main.suppliers"))

        if form.validate_on_submit():
            edit_supplier = user_supplier.edit_supplier(
                supplier_id,
                form.company_name.data,
                form.supplier_name.data,
                form.email.data,
                form.phone.data,
                form.status.data,
            )

            if edit_supplier:
                flash(
                    f"{form.supplier_name.data} from {form.company_name.data} edited.",
                    "success-supplier",
                )
            else:
                flash(
                    f"Failed to edit {form.supplier_name.data} from {form.company_name.data}. {error_messages(form)}.",
                    "danger-supplier",
                )
        else:
            flash(
                f"Failed to edit {form.supplier_name.data} from {form.company_name.data}. {error_messages(form)}.",
                "danger-supplier",
            )

            return redirect(url_for("main.suppliers"))

    def remove_suppliers(self, supplier_id) -> Any:
        user_supplier = Suppliers()
        supplier = user_supplier.get_supplier(supplier_id)

        if supplier is None:
            return redirect(url_for("main.suppliers"))

        if user_supplier.remove_supplier(supplier_id):
            flash(
                f"{supplier[2]} from {supplier[1]} removed from suppliers.",
                "success-supplier",
            )
        else:
            flash(
                f"Failed to remove {supplier[2]} from {supplier[1]} from suppliers.",
                "danger-supplier",
            )

        return redirect(url_for("main.suppliers"))
