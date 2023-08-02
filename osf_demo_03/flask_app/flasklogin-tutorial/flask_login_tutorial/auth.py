"""Routes for user authentication."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user

from . import login_manager
from .forms import LoginForm, SignupForm, SymbolForm
from .models import User, db

# Blueprint Configuration
auth_bp = Blueprint(
    "auth_bp", __name__, template_folder="templates", static_folder="static"
)


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    """
    User sign-up page.

    GET requests serve sign-up page.
    POST requests validate form & user creation.
    """
    form = SignupForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            user = User(
                name=form.name.data, email=form.email.data, website=form.website.data
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()  # Create new user
            login_user(user)  # Log in as newly created user
            return redirect(url_for("main_bp.dashboard"))
        flash("A user already exists with that email address.")
    return render_template(
        "signup.jinja2",
        title="Create an Account.",
        form=form,
        template="signup-page",
        body="Sign up for a user account.",
    )

# @auth_bp.route("/symbol", methods=["GET", "POST"])
# def symbol():
#     """
#     User sign-up page.

#     GET requests serve sign-up page.
#     POST requests validate form & user creation.
#     """
#     form = SymbolForm()
#     if form.validate_on_submit():
#         exchange_name = form.exchange_name.data
#         symbol = form.symbol.data
#         q1 = f"""
# SELECT *
# FROM {exchange_name}
# WHERE Symbol = '{symbol}'
# LIMIT 1;
# """
#         # connection = create_db_connection(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_EXISTING_DATABASE_NAME)
#         connection = create_db_connection("localhost", "root", "MyNewPass", "test")
#         results = read_query(connection, q1)
#         for result in results:
#             print(result)
#         if not results :
#             results = ["No data"]
#         return render_template(
#         "symbol_dashboard.jinja2",
#         title="Flask-Login Tutorial",
#         template="dashboard-template",
#         results=results,
#         body="Your Answer!",
#     )
#         # existing_user = User.query.filter_by(email=form.email.data).first()
#         # if existing_user is None:
#         #     user = User(
#         #         name=form.name.data, email=form.email.data, website=form.website.data
#         #     )
#         #     user.set_password(form.password.data)
#         #     db.session.add(user)
#         #     db.session.commit()  # Create new user
#         #     login_user(user)  # Log in as newly created user
#         #     return redirect(url_for("main_bp.dashboard"))
#         # flash("A user already exists with that email address.")
#     return render_template(
#         "symbol.jinja2",
#         title="Put in symbol",
#         form=form,
#         template="symbol-page",
#         body="Put in symbol",
#     )


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Log-in page for registered users.

    GET requests serve Log-in page.
    POST requests validate and redirect user to dashboard.
    """
    # Bypass if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for("main_bp.dashboard"))

    form = LoginForm()
    # Validate login attempt
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(password=form.password.data):
            login_user(user)
            next_page = request.args.get("next")
            return redirect(next_page or url_for("main_bp.dashboard"))
        flash("Invalid username/password combination")
        return redirect(url_for("auth_bp.login"))
    return render_template(
        "login.jinja2",
        form=form,
        title="Log in.",
        template="login-page",
        body="Log in with your User account.",
    )


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in upon page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash("You must be logged in to view that page.")
    return redirect(url_for("auth_bp.login"))

