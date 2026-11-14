import { useState } from 'react'
import { Link, useSearchParams, useNavigate } from 'react-router-dom'
import { authHeaders, getUser } from '../lib/auth'

export default function AcceptInvitePage() {
  const [params] = useSearchParams()
  const navigate = useNavigate()
  const tokenFromUrl = params.get('token') || ''
  const [token, setToken] = useState(tokenFromUrl)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const user = getUser()

  async function handleAccept(e: React.FormEvent) {
    e.preventDefault()
    if (!user) {
      setError('You must be signed in to accept an invite. Please log in first.')
      return
    }
    setLoading(true)
    setError('')
    setMessage('')
    try {
      const res = await fetch('http://localhost:8000/api/invites/accept', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...authHeaders() },
        body: JSON.stringify({ token })
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.detail || 'Failed to accept invite')
      setMessage(data.message)
      setTimeout(() => navigate('/workspaces'), 1500)
    } catch (err: any) {
      setError(err.message || 'Failed to accept invite')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-md mx-auto px-4 py-16">
      <h1 className="text-2xl font-bold mb-2">Accept workspace invite</h1>
      <p className="text-slate-400 text-sm mb-8">
        {user ? `Signed in as ${user.email}` : 'You need to sign in before accepting an invite.'}
      </p>

      {!user && (
        <p className="mb-6 text-sm">
          <Link to="/login" className="text-indigo-400 hover:underline">Sign in</Link> or{' '}
          <Link to="/register" className="text-indigo-400 hover:underline">create an account</Link> first.
        </p>
      )}

      <form onSubmit={handleAccept} className="space-y-4">
        <div>
          <label className="block text-sm text-slate-400 mb-1">Invite token</label>
          <input required value={token} onChange={e => setToken(e.target.value)}
            className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2" />
        </div>
        {error && <p className="text-red-400 text-sm">{error}</p>}
        {message && <p className="text-emerald-400 text-sm">{message}</p>}
        <button type="submit" disabled={loading || !user}
          className="w-full bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white font-medium py-3 rounded-lg">
          {loading ? 'Accepting…' : 'Accept invite'}
        </button>
      </form>
    </div>
  )
}
