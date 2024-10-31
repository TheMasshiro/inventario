from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.errors import return_404
from app.forms import EditProfile, EditStore
from app.main import main_bp as main
from app.models import User


@main.route("/")
def index():
    if not current_user.is_authenticated:
        return render_template("index.html", title="Welcome to Inventario")
    return redirect(url_for("main.inventory"))


@main.route("/inventory", methods=["GET", "POST"])
@login_required
def inventory():
    if request.method == "GET":
        return render_template("main/inventory.html", title="Inventory")
    return render_template("main/inventory.html", title="Inventory")


@main.route("/analytics", methods=["GET", "POST"])
@login_required
def analytics():
    if request.method == "GET":
        return render_template("main/analytics.html", title="Analytics")
    return render_template("main/analytics.html", title="Analytics")


@main.route("/sales", methods=["GET", "POST"])
@login_required
def sales():
    if request.method == "GET":
        return render_template("main/sales.html", title="Sales")
    return render_template("main/sales.html", title="Sales")


@main.route("/<username>", methods=["GET", "POST"])
@login_required
def profile(username):
    # TODO: Doing it right now display the profile here
    user = User(username=username).get_user()
    if user is None:
        return redirect(url_for("main.index"))
    if user.username != username:
        return_404()
    return render_template("main/profile.html", user=user, title=user.username)


@main.route("/about", methods=["GET", "POST"])
@login_required
def about():
    # TODO:
    if request.method == "GET":
        return render_template("main/about.html", title="About")
    return render_template("main/about.html", title="About")


@main.route("/<username>/edit", methods=["GET", "POST"])
@login_required
def edit_profile(username):
    # TODO: now? do something here to change password of the user
    user = User(username=username).get_user()
    if user is None:
        return redirect(url_for("main.index"))
    if user.username != username:
        return_404()

    form = EditProfile()
    if form.validate_on_submit():
        pass
        print(form.old_password.data)
        print(form.new_password.data)
        print(form.confirm_password.data)
    return render_template(
        "main/edit_profile.html",
        user=user,
        form=form,
        title=user.username,
    )


@main.route("/<username>/store_name", methods=["GET", "POST"])
@login_required
def store_name(username):
    user = User(username=username).get_user()
    if user is None:
        return redirect(url_for("main.index"))
    if user.username != username:
        return_404()

    form = EditStore()
    if form.validate_on_submit():
        store_name = User(
            username=username, store_name=form.store_name.data
        ).update_user()

        if not store_name:
            flash("An error has occurred", "danger")
            return redirect(url_for("main.profile", username=username))

        return redirect(url_for("main.profile", username=username))

    return render_template(
        "main/store_name.html",
        user=user,
        form=form,
        title=user.username,
    )
