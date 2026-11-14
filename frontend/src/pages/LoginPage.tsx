import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { saveAuth } from '../lib/auth'

export default function LoginPage() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      const body = new URLSearchParams()
      body.append('username', email)
      body.append('password', password)

      const res = await fetch('http://localhost:8000/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.detail || 'Login failed')

      saveAuth(data.access_token, data.email, data.full_name || '')
      navigate('/dashboard')
    } catch (err: any) {
      setError(err.message || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-md mx-auto px-4 py-16">
      <h1 className="text-2xl font-bold mb-2">Sign in</h1>
      <p className="text-slate-400 text-sm mb-8">Access your FocalPoint workspaces</p>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm text-slate-400 mb-1">Email</label>
          <input type="email" required value={email} onChange={e => setEmail(e.target.value)}
            className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2" />
        </div>
        <div>
          <label className="block text-sm text-slate-400 mb-1">Password</label>
          <input type="password" required value={password} onChange={e => setPassword(e.target.value)}
            className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2" />
        </div>

        {error && <p className="text-red-400 text-sm">{error}</p>}

        <button type="submit" disabled={loading}
          className="w-full bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white font-medium py-3 rounded-lg">
          {loading ? 'Signing in…' : 'Sign in'}
        </button>
      </form>

      <div className="mt-6 space-y-3">
        <p className="text-sm text-slate-500 text-center">Or continue with</p>
        <div className="grid grid-cols-2 gap-3">
          <a href="http://localhost:8000/api/oauth/google/login"
            className="text-center text-sm border border-slate-700 rounded-lg py-2.5 hover:bg-slate-900 transition">
            Google
          </a>
          <a href="http://localhost:8000/api/oauth/microsoft/login"
            className="text-center text-sm border border-slate-700 rounded-lg py-2.5 hover:bg-slate-900 transition">
            Microsoft
          </a>
        </div>
      </div>

      <div className="mt-6 text-sm text-slate-400 space-y-2">
        <p>No account? <Link to="/register" className="text-indigo-400 hover:underline">Register</Link></p>
        <p><Link to="/forgot-password" className="text-indigo-400 hover:underline">Forgot password?</Link></p>
      </div>
    </div>
  )
}
