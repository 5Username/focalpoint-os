import { useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'

export default function VerifyEmailPage() {
  const [params] = useSearchParams()
  const tokenFromUrl = params.get('token') || ''
  const [token, setToken] = useState(tokenFromUrl)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleVerify(e: React.FormEvent) {
    e.preventDefault()
    setLoading(true)
    setError('')
    setMessage('')
    try {
      const res = await fetch('http://localhost:8000/api/auth/verify-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token })
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.detail || 'Verification failed')
      setMessage(data.message)
    } catch (err: any) {
      setError(err.message || 'Verification failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-md mx-auto px-4 py-16">
      <h1 className="text-2xl font-bold mb-2">Verify your email</h1>
      <p className="text-slate-400 text-sm mb-8">Enter the verification token sent to your email.</p>

      <form onSubmit={handleVerify} className="space-y-4">
        <div>
          <label className="block text-sm text-slate-400 mb-1">Verification token</label>
          <input required value={token} onChange={e => setToken(e.target.value)}
            className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2" />
        </div>
        {error && <p className="text-red-400 text-sm">{error}</p>}
        {message && <p className="text-emerald-400 text-sm">{message}</p>}
        <button type="submit" disabled={loading}
          className="w-full bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white font-medium py-3 rounded-lg">
          {loading ? 'Verifying…' : 'Verify email'}
        </button>
      </form>

      <p className="mt-6 text-sm text-slate-400">
        <Link to="/login" className="text-indigo-400 hover:underline">Back to sign in</Link>
      </p>
    </div>
  )
}
