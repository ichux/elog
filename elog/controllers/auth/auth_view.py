from flask import redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user  # type: ignore

from elog.controllers.auth import auth
from elog.forms.error_login import ErrorLoginUserForm
from elog.models.profile import User


# noinspection PyUnresolvedReferences
@auth.route("/", methods=["GET", "POST"])
def login():
    form = ErrorLoginUserForm()  # form = UserLoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, remember=True)
            return redirect(request.args.get("next") or url_for("frontend.index"))

        form.username.errors.append("Invalid username or password")
    return render_template("auth/index.html", form=form)


@auth.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
