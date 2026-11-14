# Workspace Invite Links

## Create an invite

```bash
curl -X POST http://localhost:8000/api/invites/workspaces/{workspace_id}/invites \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"email": "colleague@ngo.org", "role": "member"}'
```

Response includes `invite_link` and `token`.

## Accept an invite

1. User must be logged in.
2. Open `/accept-invite?token=...` or paste the token on that page.
3. The user is added to the workspace with the invited role.

Invites expire after 7 days.
