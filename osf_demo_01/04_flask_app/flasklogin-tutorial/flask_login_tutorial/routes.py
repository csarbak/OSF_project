"""Logged-in page routes."""
from flask import Blueprint, redirect, render_template, url_for
from flask import request,jsonify
from flask_login import current_user, login_required, logout_user
import mysql.connector
from mysql.connector import Error
from sqlalchemy.engine import make_url, URL
from .forms import SymbolForm, MyForm
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
basedirLst= basedir.split("/")
del basedirLst[-1]
basedir = "/".join(basedirLst)
load_dotenv(path.join(basedir, ".env"))

url = make_url(environ.get("SQLALCHEMY_DATABASE_URI"))




# Blueprint Configuration
main_bp = Blueprint(
    "main_bp", __name__, template_folder="templates", static_folder="static"
)


@main_bp.route("/", methods=["GET"])
@login_required
def dashboard():
    """Logged-in User Dashboard."""
    return render_template(
        "dashboard.jinja2",
        title="Flask-Login Tutorial",
        template="dashboard-template",
        current_user=current_user,
        body="You are now logged in!",
    )


@main_bp.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for("auth_bp.login"))


@main_bp.route("/symbol",methods=["GET", "POST"])
@login_required
def symbol():
    """
    User sign-up page.

    GET requests serve sign-up page.
    POST requests validate form & user creation.
    """
    connection = create_db_connection(url.host, url.username, url.password, url.database)
    bxQuery = """
SELECT Symbol
FROM BX;
"""
    nasdaqQuery = """
SELECT Symbol
FROM nasdaq;
"""
    phlxQuery = """
SELECT Symbol
FROM PHLX;
"""

    bxresults = read_query(connection, bxQuery)
    nasdaqresults =read_query(connection,nasdaqQuery )
    phlxresults = read_query(connection,phlxQuery )

    symbol_choices = {
        'BX': [(symbol,symbol) for symbol in bxresults
        ],
        'nasdaq': [
            (symbol,symbol) for symbol in nasdaqresults
        ],
        'PHLX': [
            (symbol,symbol) for symbol in phlxresults
        ]
    }
    form = SymbolForm()
    if form.validate_on_submit():
        print("valid on submit")
        exchange_name = form.exchange_name.data
        symbol = form.symbol.data
        q1 = f"""
SELECT *
FROM {exchange_name}
WHERE Symbol = '{symbol}'
LIMIT 1;
"""
        #connection = create_db_connection(url.host, url.username, url.password, url.database)
        results = read_query(connection, q1)
        for result in results:
            print(result)
        if not results :
            results = ["No data"]
        return render_template(
        "symbol.jinja2",
        title="Put in symbol",
        form=form,
        template="symbol-page",
        body="Put in symbol",
    symbol_choices=symbol_choices,
    results=results
    )

    
    return render_template(
        "symbol.jinja2",
        title="Put in symbol",
        form=form,
        template="symbol-page",
        body="Put in symbol",
    symbol_choices=symbol_choices,
    results=["your data"]
    )






def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name, user=user_name, passwd=user_password, database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def read_query(connection, query):  # For reading info
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")