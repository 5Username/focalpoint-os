# RBAC Implementation Details & SSO Options

## Current RBAC Model

FocalPoint OS uses a simple, practical role-based access control model per workspace.

### Roles

| Role    | Typical permissions                                      |
|---------|----------------------------------------------------------|
| owner   | Full control, billing, delete workspace, manage members  |
| admin   | Manage members, schedules, settings, invites             |
| member  | Create briefs, travel packs, log incidents               |
| viewer  | Read-only access to briefs, packs, analytics             |

### How it is implemented

- Roles are stored on `workspace_members.role`
- API key authentication bypasses user roles (machine-to-machine)
- JWT users are associated with workspaces via membership records
- Sensitive actions currently require a **verified email** (`require_verified_user`)
- Fine-grained permission checks can be added by inspecting the membership role before allowing an action

### Example: Checking role before an action

```python
def require_workspace_role(ws_id: str, allowed_roles: list[str], user_email: str):
    # Pseudo-code
    member = get_member(ws_id, user_email)
    if not member or member.role not in allowed_roles:
        raise HTTPException(403, "Insufficient permissions")
```

### Recommended next RBAC improvements

1. Explicit permission matrix (resource + action)
2. Middleware that injects the current membership role
3. UI that hides buttons the user is not allowed to use
4. Audit every role change

---

## SSO Integration Options

For NGOs that already use organisational identity providers, SSO is highly desirable.

### Recommended approaches

| Method              | Best for                          | Complexity |
|---------------------|-----------------------------------|------------|
| **OAuth2 / OIDC**   | Google, Microsoft, Okta, Auth0    | Medium     |
| **SAML 2.0**        | Large enterprise / government IdPs| Higher     |
| **Magic link**      | Simple passwordless login         | Low        |

### Practical recommendation for FocalPoint OS

1. **Short term**: Keep email + password + verification (already implemented).
2. **Medium term**: Add Google / Microsoft OAuth (OIDC) using `authlib` or `python-social-auth`.
3. **Long term**: Support SAML for large institutional clients if demanded.

### Example OIDC (Google) sketch

```python
# Using authlib
from authlib.integrations.starlette_client import OAuth

oauth = OAuth()
oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

@app.get("/api/auth/google/login")
async def google_login(request):
    redirect_uri = "https://yourdomain.com/api/auth/google/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)
```

After successful callback:
- Create or find the user by email
- Mark `is_verified = True` (provider already verified the email)
- Issue the same JWT used by the rest of the system

### Security notes for SSO

- Always validate the `id_token` / claims
- Prefer `email_verified == true` from the provider
- Still keep local roles inside each workspace
- Log SSO logins in the audit log

---

## Invite Code Snippets

### Create invite (backend already implemented)

```bash
curl -X POST http://localhost:8000/api/invites/workspaces/{ws_id}/invites \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"email": "colleague@ngo.org", "role": "member"}'
```

### Accept invite

```bash
curl -X POST http://localhost:8000/api/invites/accept \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"token": "invite-token-here"}'
```

### Frontend

- Manage invites: Workspaces page → “Manage Invites”
- Accept invite: `/accept-invite?token=...`

---

## Forced Email Verification

Sensitive actions (create workspace, update workspace, configure schedule, add members) now use:

```python
auth=Depends(require_verified_user)
```

Unverified users receive HTTP 403 with a clear message asking them to verify their email first.
