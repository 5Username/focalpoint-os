import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { authHeaders, getUser, clearAuth } from '../lib/auth'
import { useNavigate } from 'react-router-dom'

export default function DashboardPage() {
  const navigate = useNavigate()
  const user = getUser()
  const [summary, setSummary] = useState<any>(null)
  const [error, setError] = useState('')

  useEffect(() => {
    if (!user) {
      navigate('/login')
      return
    }
    fetch('http://localhost:8000/api/analytics/summary', {
      headers: authHeaders()
    })
      .then(r => {
        if (r.status === 401) {
          clearAuth()
          navigate('/login')
          return null
        }
        return r.json()
      })
      .then(data => data && setSummary(data))
      .catch(() => setError('Could not load analytics'))
  }, [])

  function logout() {
    clearAuth()
    navigate('/login')
  }

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <div className="flex justify-between items-start mb-8">
        <div>
          <h1 className="text-2xl font-bold">Dashboard</h1>
          <p className="text-slate-400 text-sm">
            {user ? `Signed in as ${user.full_name || user.email}` : ''}
          </p>
        </div>
        <button onClick={logout} className="text-sm text-slate-400 hover:text-white">
          Sign out
        </button>
      </div>

      {error && <p className="text-red-400 text-sm mb-4">{error}</p>}

      {summary && (
        <>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-10">
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
              <div className="text-2xl font-bold text-indigo-300">{summary.workspace_count}</div>
              <div className="text-sm text-slate-500">Workspaces</div>
            </div>
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
              <div className="text-2xl font-bold text-indigo-300">{summary.total_briefs_generated}</div>
              <div className="text-sm text-slate-500">Briefs generated</div>
            </div>
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
              <div className="text-2xl font-bold text-indigo-300">{summary.total_incidents_logged}</div>
              <div className="text-sm text-slate-500">Incidents logged</div>
            </div>
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
              <div className="text-2xl font-bold text-indigo-300">{summary.recent_activity?.length || 0}</div>
              <div className="text-sm text-slate-500">Recent events</div>
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
              <h2 className="font-semibold text-indigo-300 mb-4">Workspaces</h2>
              {summary.workspaces?.length === 0 && <p className="text-slate-500 text-sm">No workspaces yet.</p>}
              <div className="space-y-3">
                {summary.workspaces?.map((w: any) => (
                  <div key={w.id} className="flex justify-between items-center text-sm border-b border-slate-800 pb-2">
                    <div>
                      <div className="font-medium">{w.name}</div>
                      <div className="text-slate-500">Briefs: {w.briefs} · Incidents: {w.incidents}</div>
                    </div>
                    <Link to={`/workspaces`} className="text-indigo-400 text-xs hover:underline">View</Link>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
              <h2 className="font-semibold text-indigo-300 mb-4">Recent Activity (Audit Log)</h2>
              {(!summary.recent_activity || summary.recent_activity.length === 0) && (
                <p className="text-slate-500 text-sm">No activity yet.</p>
              )}
              <div className="space-y-3 max-h-80 overflow-y-auto">
                {summary.recent_activity?.map((a: any) => (
                  <div key={a.id} className="text-sm border-b border-slate-800 pb-2">
                    <div className="font-medium">{a.action}</div>
                    <div className="text-slate-500">{a.details}</div>
                    <div className="text-xs text-slate-600 mt-1">{a.user_email} · {a.created_at}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </>
      )}

      {!summary && !error && <p className="text-slate-500">Loading analytics…</p>}
    </div>
  )
}
