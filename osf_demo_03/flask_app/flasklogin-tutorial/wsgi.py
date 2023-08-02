"""Application entry point."""
from flask_login_tutorial import create_app
import sys
sys.path.append("../../scripts")
# change to your path
import download_equity_stock_data as download_equity_stock_data

download_equity_stock_data.main(False)

app = create_app()

if __name__ == "__main__":

    app.run(host="0.0.0.0")
