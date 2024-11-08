import logging
from abc import abstractmethod
from typing import Any

from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user

from app.user_forms import LoginForm, RegisterForm
from app.user_models import User


class AuthInterface:
    @abstractmethod
    def login_user(self) -> Any:
        pass

    @abstractmethod
    def register_user(self) -> Any:
        pass

    @abstractmethod
    def logout_user(self) -> Any:
        pass


class AuthManager(AuthInterface):
    def login_user(self) -> Any:
        """
        Log in user
        """
        if current_user.is_authenticated:
            return redirect(url_for("main.inventory"))

        form = LoginForm()
        if form.validate_on_submit():
            user = User(username=form.username.data).get_user()

            if user is None or not user.check_password(form.password.data):
                return redirect(url_for("auth.login"))

            try:
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for("main.inventory"))
            except Exception as e:
                logging.error(f"Login failed: {str(e)}")

        return render_template("auth/login.html", title="Log in", form=form)

    def register_user(self) -> Any:
        """
        Register user
        """
        if current_user.is_authenticated:
            return redirect(url_for("main.inventory"))

        form = RegisterForm()
        if form.validate_on_submit():
            user = User(username=form.username.data)
            user.set_password(form.password.data)
            is_created = user.create_user()

            if not is_created:
                flash("An error has occurred", "danger")
                return redirect(url_for("auth.register"))

            try:
                login_user(user.get_user(), remember=form.remember_me.data)
                return redirect(url_for("main.inventory"))
            except Exception as e:
                logging.error(f"Login failed: {str(e)}")

        return render_template("auth/register.html", title="Register", form=form)

    def logout_user(self) -> Any:
        """Logout User"""
        logout_user()
        return redirect(url_for("auth.login"))
