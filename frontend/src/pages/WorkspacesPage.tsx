import { useState, useEffect } from 'react'
import { useLang } from '../App'
import { t } from '../i18n'

interface Workspace {
  id: string
  name: string
  region: string
  primary_language: string
  api_key?: string
  created_at: string
  settings?: any
}

export default function WorkspacesPage() {
  const { lang } = useLang()
  const [workspaces, setWorkspaces] = useState<Workspace[]>([])
  const [name, setName] = useState('')
  const [region, setRegion] = useState('Kenya')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')
  const [newKey, setNewKey] = useState<string | null>(null)

  async function load() {
    try {
      const res = await fetch('http://localhost:8000/api/workspaces/')
      const data = await res.json()
      setWorkspaces(data)
    } catch {
      setMessage('Could not load workspaces (is the backend running?)')
    }
  }

  useEffect(() => { load() }, [])

  async function createWorkspace(e: React.FormEvent) {
    e.preventDefault()
    setLoading(true)
    setNewKey(null)
    try {
      const res = await fetch('http://localhost:8000/api/workspaces/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, region, primary_language: lang })
      })
      const data = await res.json()
      setNewKey(data.api_key)
      setMessage(`Workspace "${data.name}" created`)
      setName('')
      load()
    } catch {
      setMessage('Failed to create workspace')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-2">NGO Workspaces</h1>
      <p className="text-slate-400 mb-8 text-sm">
        Create and manage multi-tenant workspaces. Each workspace gets its own API key.
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
          <p className="text-amber-600/80 mt-2 text-xs">Use header: <code>X-API-Key: {newKey}</code></p>
        </div>
      )}

      {message && <p className="text-sm text-slate-400 mb-4">{message}</p>}

      <div className="space-y-3">
        <h2 className="text-lg font-semibold text-indigo-300">Existing Workspaces</h2>
        {workspaces.length === 0 && <p className="text-slate-500 text-sm">No workspaces yet.</p>}
        {workspaces.map(ws => (
          <div key={ws.id} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="flex justify-between items-start">
              <div>
                <div className="font-medium">{ws.name}</div>
                <div className="text-sm text-slate-500">{ws.region} • {ws.primary_language} • ID: {ws.id}</div>
              </div>
              {ws.settings?.brief_schedule?.enabled && (
                <span className="text-xs px-2 py-1 rounded bg-emerald-900/50 text-emerald-300">
                  Scheduled
                </span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
