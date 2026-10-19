"""Google / 카카오 OAuth 뼈대 (Authlib). 키가 없으면 해당 로그인은 비활성. 사용자는 세션에만 저장."""
from authlib.integrations.flask_client import OAuth
from flask import Blueprint, flash, redirect, render_template, session, url_for

bp = Blueprint("auth", __name__)
oauth = OAuth()


def init_oauth(app):
    oauth.init_app(app)
    cfg = app.config
    if cfg["GOOGLE_CLIENT_ID"]:
        oauth.register(
            name="google",
            client_id=cfg["GOOGLE_CLIENT_ID"],
            client_secret=cfg["GOOGLE_CLIENT_SECRET"],
            server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
            client_kwargs={"scope": "openid email profile"},
        )
    if cfg["KAKAO_CLIENT_ID"]:
        oauth.register(
            name="kakao",
            client_id=cfg["KAKAO_CLIENT_ID"],
            client_secret=cfg["KAKAO_CLIENT_SECRET"],
            authorize_url="https://kauth.kakao.com/oauth/authorize",
            access_token_url="https://kauth.kakao.com/oauth/token",
            api_base_url="https://kapi.kakao.com/",
            client_kwargs={"scope": "profile_nickname"},
        )


def _client(provider):
    return getattr(oauth, provider, None) if provider in ("google", "kakao") else None


@bp.route("/login")
def login():
    return render_template("login.html", enabled={p: _client(p) is not None for p in ("google", "kakao")})


@bp.route("/login/<provider>")
def login_provider(provider):
    client = _client(provider)
    if client is None:
        flash(f"{provider} 로그인이 설정되지 않았습니다. .env에 클라이언트 키를 입력하세요.")
        return redirect(url_for("auth.login"))
    return client.authorize_redirect(url_for("auth.callback", provider=provider, _external=True))


@bp.route("/auth/<provider>/callback")
def callback(provider):
    client = _client(provider)
    if client is None:
        return redirect(url_for("auth.login"))
    token = client.authorize_access_token()
    if provider == "google":
        info = token.get("userinfo") or {}
        user = {"id": f"google:{info.get('sub')}", "name": info.get("name") or info.get("email")}
    else:
        info = client.get("v2/user/me", token=token).json()
        nickname = (info.get("properties") or {}).get("nickname")
        user = {"id": f"kakao:{info.get('id')}", "name": nickname or "카카오 사용자"}
    session["user"] = user  # TODO: 사용자 저장소(DB) 도입 시 upsert
    return redirect(url_for("main.index"))


@bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("main.index"))
