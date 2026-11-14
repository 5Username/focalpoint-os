# OIDC / OAuth Provider Setup (Google & Microsoft)

FocalPoint OS includes OAuth route stubs for Google and Microsoft.  
Follow this guide to complete a production-ready OIDC integration.

## 1. Google OAuth (OpenID Connect)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project (or select an existing one)
3. Enable **Google Identity** / OAuth consent screen
4. Create OAuth 2.0 Client ID (Web application)
5. Add authorized redirect URI:
   ```
   https://your-domain.com/api/oauth/google/callback
   ```
   For local development:
   ```
   http://localhost:8000/api/oauth/google/callback
   ```
6. Copy the Client ID and Client Secret

Environment variables:
```bash
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-secret
OAUTH_REDIRECT_BASE=https://your-domain.com
```

## 2. Microsoft (Azure AD / Entra ID)

1. Go to [Azure Portal](https://portal.azure.com/) → Microsoft Entra ID
2. App registrations → New registration
3. Set redirect URI:
   ```
   https://your-domain.com/api/oauth/microsoft/callback
   ```
4. Create a client secret
5. Note the Application (client) ID and Directory (tenant) ID

Environment variables:
```bash
MICROSOFT_CLIENT_ID=your-application-client-id
MICROSOFT_CLIENT_SECRET=your-client-secret
MICROSOFT_TENANT_ID=common   # or your tenant ID
```

## 3. Recommended library

```bash
pip install authlib
```

Then replace the stubs in `backend/app/routers/oauth.py` with real `authlib` flows.

### Minimal Google flow sketch

```python
from authlib.integrations.starlette_client import OAuth

oauth = OAuth()
oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)
```

After successful callback:
1. Validate the `id_token`
2. Extract `email` (and prefer `email_verified == true`)
3. Create or find the local user
4. Mark `is_verified = True`
5. Issue the same JWT used by the rest of FocalPoint OS
6. Redirect the browser to the frontend with the token (or set an httpOnly cookie)

## 4. Security checklist

- [ ] Use HTTPS only in production
- [ ] Validate `state` / `nonce`
- [ ] Check `email_verified`
- [ ] Log SSO logins in the audit log
- [ ] Keep local workspace roles separate from the IdP
