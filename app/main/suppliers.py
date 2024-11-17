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
            company_name = form.company_name.data
            supplier_name = form.supplier_name.data
            email = form.email.data
            phone = form.phone.data
            status = form.status.data

            existing_supplier_name = user_supplier.get_supplier_by_name(
                company_name, supplier_name
            )
            if supplier_name is None:
                flash(
                    "Supplier name is required",
                    "danger-supplier",
                )
                return redirect(url_for("main.suppliers"))

            if (
                existing_supplier_name
                and existing_supplier_name[2].strip().lower()
                == supplier_name.strip().lower()
            ):
                flash(
                    f"{form.supplier_name.data} from {form.company_name.data} already exists in Suppliers",
                    "danger-supplier",
                )
                return redirect(url_for("main.suppliers"))

            existing_supplier_email = user_supplier.get_supplier_by_email(
                company_name, email
            )
            if email is None:
                flash(
                    "Email is required",
                    "danger-supplier",
                )
                return redirect(url_for("main.suppliers"))

            if (
                existing_supplier_email
                and existing_supplier_email[3].strip().lower() == email.strip().lower()
            ):
                flash(
                    f"{form.email.data} already exists in Suppliers",
                    "danger-supplier",
                )
                return redirect(url_for("main.suppliers"))

            existing_supplier_phone = user_supplier.get_supplier_by_phone(
                company_name, phone
            )
            if existing_supplier_phone:
                flash(
                    f"{form.phone.data} already exists in Suppliers",
                    "danger-supplier",
                )
                return redirect(url_for("main.suppliers"))

            add_supplier = user_supplier.add_supplier(
                company_name, supplier_name, email, phone, status
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
            new_company_name = form.company_name.data
            new_supplier_name = form.supplier_name.data
            new_email = form.email.data
            new_phone = form.phone.data
            new_status = form.status.data

            existing_supplier = user_supplier.get_supplier_by_name(
                new_company_name, new_supplier_name
            )
            if existing_supplier and existing_supplier[0] != supplier_id:
                flash(
                    f"{form.supplier_name.data} from {form.company_name.data} already exists in Suppliers",
                    "danger-supplier",
                )
                return redirect(url_for("main.suppliers"))

            existing_supplier_email = user_supplier.get_supplier_by_email(
                new_company_name, new_email
            )
            if existing_supplier_email and existing_supplier_email[0] != supplier_id:
                flash(
                    f"{form.email.data} already exists in Suppliers",
                    "danger-supplier",
                )
                return redirect(url_for("main.suppliers"))

            existing_supplier_phone = user_supplier.get_supplier_by_phone(
                new_company_name, new_phone
            )
            if existing_supplier_phone and existing_supplier_phone[0] != supplier_id:
                flash(
                    f"{form.phone.data} already exists in Suppliers",
                    "danger-supplier",
                )
                return redirect(url_for("main.suppliers"))

            edit_supplier = user_supplier.edit_supplier(
                supplier_id,
                new_company_name,
                new_supplier_name,
                new_email,
                new_phone,
                new_status,
            )

            if edit_supplier:
                flash(
                    f"Successfully edited {form.company_name.data}",
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

        print(supplier_id)

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
