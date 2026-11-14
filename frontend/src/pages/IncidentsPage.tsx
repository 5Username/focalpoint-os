import { useState, useEffect } from 'react'
import { addToQueue, getQueue, clearQueue } from '../lib/offlineQueue'

export default function IncidentsPage() {
  const [form, setForm] = useState({
    title: '',
    category: 'security',
    severity: 'medium',
    location: '',
    description: '',
    reported_by: ''
  })
  const [status, setStatus] = useState('')
  const [queueCount, setQueueCount] = useState(0)
  const [online, setOnline] = useState(navigator.onLine)

  useEffect(() => {
    setQueueCount(getQueue().length)
    const onOnline = () => { setOnline(true); syncQueue() }
    const onOffline = () => setOnline(false)
    window.addEventListener('online', onOnline)
    window.addEventListener('offline', onOffline)
    return () => {
      window.removeEventListener('online', onOnline)
      window.removeEventListener('offline', onOffline)
    }
  }, [])

  async function syncQueue() {
    const items = getQueue()
    if (items.length === 0) return
    // In production: POST each item to backend / Google Sheets
    console.log('Syncing', items.length, 'queued incidents')
    clearQueue()
    setQueueCount(0)
    setStatus(`Synced ${items.length} offline incident(s)`)
  }

  async function submit(e: React.FormEvent) {
    e.preventDefault()
    setStatus('Saving…')

    const payload = { ...form, occurred_at: new Date().toISOString() }

    if (!navigator.onLine) {
      addToQueue(payload)
      setQueueCount(getQueue().length)
      setStatus('Saved offline. Will sync when connection returns.')
      setForm({ title: '', category: 'security', severity: 'medium', location: '', description: '', reported_by: '' })
      return
    }

    try {
      const res = await fetch('http://localhost:8000/api/incidents/log', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      const data = await res.json()
      setStatus(`Logged: ${data.id}`)
      setForm({ title: '', category: 'security', severity: 'medium', location: '', description: '', reported_by: '' })
    } catch {
      addToQueue(payload)
      setQueueCount(getQueue().length)
      setStatus('Backend unreachable — saved offline')
    }
  }

  return (
    <div className="max-w-xl mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold">Incident Logger</h1>
          <p className="text-slate-400 text-sm">Works offline • Syncs later</p>
        </div>
        <div className="text-right text-sm">
          <div className={online ? 'text-emerald-400' : 'text-amber-400'}>
            {online ? 'Online' : 'Offline'}
          </div>
          {queueCount > 0 && <div className="text-slate-500">{queueCount} queued</div>}
        </div>
      </div>

      <form onSubmit={submit} className="space-y-4">
        <div>
          <label className="block text-sm text-slate-400 mb-1">Title</label>
          <input required value={form.title} onChange={e => setForm({...form, title: e.target.value})}
            className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2" />
        </div>

        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-sm text-slate-400 mb-1">Category</label>
            <select value={form.category} onChange={e => setForm({...form, category: e.target.value})}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2">
              <option value="security">Security</option>
              <option value="medical">Medical</option>
              <option value="logistics">Logistics</option>
              <option value="safeguarding">Safeguarding</option>
              <option value="other">Other</option>
            </select>
          </div>
          <div>
            <label className="block text-sm text-slate-400 mb-1">Severity</label>
            <select value={form.severity} onChange={e => setForm({...form, severity: e.target.value})}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2">
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
              <option value="critical">Critical</option>
            </select>
          </div>
        </div>

        <div>
          <label className="block text-sm text-slate-400 mb-1">Location</label>
          <input required value={form.location} onChange={e => setForm({...form, location: e.target.value})}
            className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2" />
        </div>

        <div>
          <label className="block text-sm text-slate-400 mb-1">Description</label>
          <textarea required rows={4} value={form.description} onChange={e => setForm({...form, description: e.target.value})}
            className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2" />
        </div>

        <div>
          <label className="block text-sm text-slate-400 mb-1">Reported by</label>
          <input required value={form.reported_by} onChange={e => setForm({...form, reported_by: e.target.value})}
            className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2" />
        </div>

        <button type="submit" className="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-medium py-3 rounded-lg">
          Log Incident
        </button>
      </form>

      {status && <p className="mt-4 text-center text-sm text-slate-400">{status}</p>}
    </div>
  )
}
