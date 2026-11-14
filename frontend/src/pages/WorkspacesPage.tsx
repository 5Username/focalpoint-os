import { useState, useEffect } from 'react'
import { useLang } from '../App'
import { authHeaders, getUser } from '../lib/auth'

interface Workspace {
  id: string
  name: string
  region: string
  primary_language: string
  api_key?: string
  created_at: string
  settings?: any
  members?: any[]
}

export default function WorkspacesPage() {
  const { lang } = useLang()
  const user = getUser()
  const [workspaces, setWorkspaces] = useState<Workspace[]>([])
  const [name, setName] = useState('')
  const [region, setRegion] = useState('Kenya')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')
  const [newKey, setNewKey] = useState<string | null>(null)
  const [selectedWs, setSelectedWs] = useState<string | null>(null)
  const [inviteEmail, setInviteEmail] = useState('')
  const [inviteRole, setInviteRole] = useState('member')
  const [invites, setInvites] = useState<any[]>([])
  const [inviteMsg, setInviteMsg] = useState('')

  async function load() {
    try {
      const res = await fetch('http://localhost:8000/api/workspaces/', {
        headers: authHeaders()
      })
      const data = await res.json()
      setWorkspaces(Array.isArray(data) ? data : [])
    } catch {
      setMessage('Could not load workspaces (is the backend running?)')
    }
  }

  useEffect(() => { load() }, [])

  async function createWorkspace(e: React.FormEvent) {
    e.preventDefault()
    setLoading(true)
    setNewKey(null)
    setMessage('')
    try {
      const res = await fetch('http://localhost:8000/api/workspaces/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...authHeaders() },
        body: JSON.stringify({ name, region, primary_language: lang })
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.detail || 'Failed to create')
      setNewKey(data.api_key)
      setMessage(`Workspace "${data.name}" created`)
      setName('')
      load()
    } catch (err: any) {
      setMessage(err.message || 'Failed to create workspace')
    } finally {
      setLoading(false)
    }
  }

  async function loadInvites(wsId: string) {
    setSelectedWs(wsId)
    setInviteMsg('')
    try {
      const res = await fetch(`http://localhost:8000/api/invites/workspaces/${wsId}/invites`, {
        headers: authHeaders()
      })
      const data = await res.json()
      setInvites(Array.isArray(data) ? data : [])
    } catch {
      setInvites([])
    }
  }

  async function sendInvite(e: React.FormEvent) {
    e.preventDefault()
    if (!selectedWs) return
    setInviteMsg('')
    try {
      const res = await fetch(`http://localhost:8000/api/invites/workspaces/${selectedWs}/invites`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...authHeaders() },
        body: JSON.stringify({ email: inviteEmail, role: inviteRole })
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.detail || 'Invite failed')
      setInviteMsg(`Invite sent to ${data.email}. Link: ${data.invite_link}`)
      setInviteEmail('')
      loadInvites(selectedWs)
    } catch (err: any) {
      setInviteMsg(err.message || 'Failed to send invite')
    }
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-2">NGO Workspaces</h1>
      <p className="text-slate-400 mb-8 text-sm">
        Create workspaces, manage members and send invite links.
        {user ? ` Signed in as ${user.email}` : ' Sign in to create workspaces.'}
      </p>

      <form onSubmit={createWorkspace} className="bg-slate-900 border border-slate-800 rounded-2xl p-6 mb-8 space-y-4">
        <h2 className="text-lg font-semibold text-indigo-300">Create Workspace</h2>
        <div>
          <label className="block text-sm text-slate-400 mb-1">Organisation Name</label>
          <input required value={name} onChange={e => setName(e.target.value)}
            className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2" placeholder="Example NGO Kenya" />
        </div>
        <div>
          <label className="block text-sm text-slate-400 mb-1">Primary Region</label>
          <input value={region} onChange={e => setRegion(e.target.value)}
            className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2" />
        </div>
        <button type="submit" disabled={loading}
          className="w-full bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white font-medium py-3 rounded-lg">
          {loading ? 'Creating…' : 'Create Workspace'}
        </button>
      </form>

      {newKey && (
        <div className="bg-amber-950/40 border border-amber-700/50 rounded-xl p-4 mb-6 text-sm">
          <p className="font-medium text-amber-300 mb-1">API Key (copy now — shown only once)</p>
          <code className="block break-all text-amber-100 bg-slate-950 p-2 rounded">{newKey}</code>
        </div>
      )}

      {message && <p className="text-sm text-slate-400 mb-4">{message}</p>}

      <div className="space-y-3 mb-10">
        <h2 className="text-lg font-semibold text-indigo-300">Existing Workspaces</h2>
        {workspaces.length === 0 && <p className="text-slate-500 text-sm">No workspaces yet.</p>}
        {workspaces.map(ws => (
          <div key={ws.id} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="flex justify-between items-start gap-4">
              <div>
                <div className="font-medium">{ws.name}</div>
                <div className="text-sm text-slate-500">{ws.region} • {ws.primary_language} • ID: {ws.id}</div>
              </div>
              <button
                onClick={() => loadInvites(ws.id)}
                className="text-xs px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-indigo-300"
              >
                Manage Invites
              </button>
            </div>
          </div>
        ))}
      </div>

      {selectedWs && (
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4">
          <h2 className="text-lg font-semibold text-indigo-300">Invites for workspace {selectedWs}</h2>

          <form onSubmit={sendInvite} className="space-y-3">
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <input
                type="email"
                required
                placeholder="colleague@ngo.org"
                value={inviteEmail}
                onChange={e => setInviteEmail(e.target.value)}
                className="sm:col-span-2 bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-sm"
              />
              <select
                value={inviteRole}
                onChange={e => setInviteRole(e.target.value)}
                className="bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-sm"
              >
                <option value="member">Member</option>
                <option value="admin">Admin</option>
                <option value="viewer">Viewer</option>
              </select>
            </div>
            <button type="submit" className="bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-medium px-4 py-2 rounded-lg">
              Send Invite
            </button>
          </form>

          {inviteMsg && <p className="text-sm text-slate-400 break-all">{inviteMsg}</p>}

          <div className="space-y-2 mt-4">
            {invites.length === 0 && <p className="text-slate-500 text-sm">No invites yet.</p>}
            {invites.map(inv => (
              <div key={inv.id} className="text-sm border-b border-slate-800 pb-2 flex justify-between">
                <div>
                  <span className="font-medium">{inv.email}</span>
                  <span className="text-slate-500"> · {inv.role}</span>
                </div>
                <span className={inv.accepted ? 'text-emerald-400' : 'text-amber-400'}>
                  {inv.accepted ? 'Accepted' : 'Pending'}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
