import atexit

import waitress
from flask import Flask

from models import close_db, init_db
from server import AdsViews, UserViews

init_db()
atexit.register(close_db)

app = Flask("app")


ads_view = AdsViews.as_view("ads")
user_view = UserViews.as_view("user")

app.add_url_rule(
    "/ads/<int:ads_id>", view_func=ads_view, methods=["GET", "PATCH", "DELETE"]
)
app.add_url_rule(
    "/user/<int:user_id>", view_func=user_view, methods=["GET", "PATCH", "DELETE"]
)
app.add_url_rule("/ads", view_func=ads_view, methods=["POST"])
app.add_url_rule("/user", view_func=user_view, methods=["POST"])

if __name__ == "__main__":
    app.run()