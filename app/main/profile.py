from abc import ABC, abstractmethod
from typing import Any

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user

from app.user_forms import EditProfile, EditStore
from app.user_models import User


class ProfileInterface(ABC):
    @abstractmethod
    def profile(self, username) -> Any:
        pass

    @abstractmethod
    def edit_profile(self, username) -> Any:
        pass

    @abstractmethod
    def store_name(self, username) -> Any:
        pass


class ProfileManager(ProfileInterface):
    def profile(self, username) -> Any:
        if username != current_user.username:
            abort(401)

        user = User(username=username).get_user()
        if user is None:
            return redirect(url_for("main.index"))

        return render_template("main/profile.html", user=user, title=user.username)

    def edit_profile(self, username) -> Any:
        if username != current_user.username:
            abort(401)

        user = User(username=username).get_user()
        if user is None:
            return redirect(url_for("main.index"))

        form = EditProfile()
        if form.validate_on_submit():
            user.set_password(form.new_password.data)

            if not user.update_user(new_password=user.password_hash):
                return redirect(url_for("main.edit_profile", username=username))

            return redirect(url_for("main.profile", username=username))

        return render_template(
            "main/edit_profile.html",
            user=user,
            form=form,
            title=user.username,
        )

    def store_name(self, username) -> Any:
        user = User(username=username).get_user()
        if username != current_user.username:
            abort(401)

        if user is None:
            return redirect(url_for("main.index"))

        form = EditStore()
        if form.validate_on_submit():
            user.store_name = form.store_name.data

            if not user.update_user():
                return redirect(url_for("main.profile", username=username))

            flash("Store name updated successfully", "success")
            return redirect(url_for("main.profile", username=username))

        return render_template(
            "main/store_name.html",
            user=user,
            form=form,
            title=user.username,
        )
