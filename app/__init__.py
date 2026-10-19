from datetime import date

from flask import Flask, request

from app.config import Config
from app.repositories import build_repos


def create_app(config_overrides=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if config_overrides:
        app.config.update(config_overrides)

    app.extensions["repos"] = build_repos(app.config)

    from app.blueprints import auth, jobs, main, mypage, stats, trend

    for module in (main, jobs, trend, auth, mypage, stats):
        app.register_blueprint(module.bp)
    auth.init_oauth(app)

    @app.before_request
    def count_visit():
        if request.endpoint and request.endpoint != "static" and request.method == "GET":
            app.extensions["repos"].stats.increment(request.endpoint)

    @app.template_filter("dday")
    def dday(deadline_at):
        if not deadline_at:
            return "상시"
        diff = (date.fromisoformat(deadline_at) - date.today()).days
        if diff < 0:
            return "마감"
        return "D-DAY" if diff == 0 else f"D-{diff}"

    @app.context_processor
    def inject_globals():
        from flask import session

        return {"current_user": session.get("user")}

    return app
