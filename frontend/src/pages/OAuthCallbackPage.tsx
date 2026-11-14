import { useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { saveAuth } from '../lib/auth'

export default function OAuthCallbackPage() {
  const [params] = useSearchParams()
  const navigate = useNavigate()

  useEffect(() => {
    const token = params.get('token')
    const email = params.get('email') || ''
    const fullName = params.get('full_name') || ''

    if (token) {
      saveAuth(token, email, fullName)
      navigate('/dashboard')
    } else {
      navigate('/login')
    }
  }, [])

  return (
    <div className="max-w-md mx-auto px-4 py-16 text-center">
      <p className="text-slate-400">Completing sign-in…</p>
    </div>
  )
}
