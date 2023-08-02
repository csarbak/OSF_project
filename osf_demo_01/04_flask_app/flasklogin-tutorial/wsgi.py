"""Application entry point."""
from flask_login_tutorial import create_app
import sys
sys.path.append("/Users/conradscomputer/Desktop/Fintech/osfutils_dev/osf_demo_01/01_load_dbs/daily_downloads")
# change to your path
import dailyScript as dailyScrip

dailyScrip.main()

app = create_app()

if __name__ == "__main__":

    app.run(host="0.0.0.0")
