from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.main import main_bp as main
from app.main.analytics import AnalyticsManager
from app.main.inventory import InventoryManager
from app.main.profile import ProfileManager
from app.main.purchase import PurchaseManager
from app.main.suppliers import SuppliersManager


@main.route("/")
def index():
    if not current_user.is_authenticated:
        return render_template("index.html", title="Welcome to Inventario")
    return redirect(url_for("main.inventory"))


@main.route("/product/search")
@login_required
def search_product():
    return InventoryManager().search_product()


@main.route("/supplier/search")
@login_required
def search_supplier():
    return SuppliersManager().search_supplier()


@main.route("/customer/search")
@login_required
def search_customer():
    return AnalyticsManager().search_customer()


@main.route("/purchase/search")
@login_required
def search_purchase():
    return PurchaseManager().search_product()


@main.route("/purchase", methods=["GET", "POST"])
@login_required
def purchase():
    return PurchaseManager().purchase()


@main.route("/inventory", methods=["GET", "POST"])
@login_required
def inventory():
    return InventoryManager().inventory()


@main.route("/inventory/edit/<int:product_id>", methods=["POST"])
@login_required
def edit_product(product_id):
    return InventoryManager().edit_product(product_id)


@main.route("/inventory/delete/<int:product_id>", methods=["POST"])
@login_required
def remove_product(product_id):
    return InventoryManager().remove_product(product_id)


@main.route("/analytics", methods=["GET", "POST"])
@login_required
def analytics():
    return AnalyticsManager().analytics()


@main.route("/customers", methods=["GET", "POST"])
@login_required
def customers():
    return AnalyticsManager().customers()


@main.route("/customer/edit/<int:customer_id>", methods=["POST"])
@login_required
def edit_customer(customer_id):
    return AnalyticsManager().edit_customer(customer_id)


@main.route("/customer/delete/<int:customer_id>", methods=["POST"])
@login_required
def remove_customer(customer_id):
    return AnalyticsManager().remove_customer(customer_id)


@main.route("/suppliers", methods=["GET", "POST"])
@login_required
def suppliers():
    return SuppliersManager().suppliers()


@main.route("/suppliers/edit/<int:supplier_id>", methods=["POST"])
@login_required
def edit_supplier(supplier_id):
    return SuppliersManager().edit_suppliers(supplier_id)


@main.route("/suppliers/delete/<int:supplier_id>", methods=["POST"])
@login_required
def remove_supplier(supplier_id):
    return SuppliersManager().remove_suppliers(supplier_id)


@main.route("/user/<username>", methods=["GET", "POST"])
@login_required
def profile(username):
    return ProfileManager().profile(username)


@main.route("/user/<username>/edit", methods=["GET", "POST"])
@login_required
def edit_profile(username):
    return ProfileManager().edit_profile(username)


@main.route("/user/<username>/store_name", methods=["GET", "POST"])
@login_required
def store_name(username):
    return ProfileManager().store_name(username)
