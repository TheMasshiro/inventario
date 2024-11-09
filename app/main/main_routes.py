from flask import redirect, render_template, url_for
from flask_login import current_user, login_required

from app.main import main_bp as main
from app.main.inventory import InventoryManager
from app.main.profile import ProfileManager


@main.route("/")
def index():
    if not current_user.is_authenticated:
        return render_template("index.html", title="Welcome to Inventario")
    return redirect(url_for("main.inventory"))


@main.route("/purchase", methods=["GET", "POST"])
@login_required
def purchase():
    return InventoryManager().purchase()


@main.route("/inventory", methods=["GET", "POST"])
@login_required
def inventory():
    return InventoryManager().inventory()


@main.route("/inventory/edit/<int:product_id>", methods=["POST"])
def edit_product(product_id):
    return InventoryManager().edit_product(product_id)


@main.route("/inventory/delete/<int:product_id>", methods=["POST"])
def remove_product(product_id):
    return InventoryManager().remove_product(product_id)


@main.route("/analytics", methods=["GET", "POST"])
@login_required
def analytics():
    return InventoryManager().analytics()


@main.route("/suppliers", methods=["GET", "POST"])
@login_required
def suppliers():
    return InventoryManager().suppliers()


@main.route("/about", methods=["GET", "POST"])
@login_required
def about():
    return InventoryManager().about()


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
