"""OAuth2 authorization-code flow (e.g. 'Sign in with Google') using
Authlib. Demonstration wiring — requires OAUTH2_GOOGLE_CLIENT_ID/SECRET to
be set to actually redirect to a real provider."""
from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Request

from app.core.config import get_settings

settings = get_settings()
router = APIRouter(prefix="/oauth", tags=["OAuth2"])

oauth = OAuth()
oauth.register(
    name="google",
    client_id=settings.OAUTH2_GOOGLE_CLIENT_ID,
    client_secret=settings.OAUTH2_GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


@router.get("/google/login")
async def google_login(request: Request):
    redirect_uri = request.url_for("google_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback", name="google_callback")
async def google_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    userinfo = token.get("userinfo", {})
    # In a full implementation: find-or-create local User, then issue JWTs
    # via AuthService, mirroring the password-flow login endpoint above.
    return {"email": userinfo.get("email"), "note": "demo OAuth2 callback — wire up AuthService here"}
