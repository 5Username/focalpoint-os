import { BrowserRouter, Routes, Route, Link, useLocation } from 'react-router-dom'
import BriefsPage from './pages/BriefsPage'
import TravelPage from './pages/TravelPage'
import IncidentsPage from './pages/IncidentsPage'

function Nav() {
  const location = useLocation()
  const linkClass = (path: string) =>
    `px-3 py-2 rounded-lg text-sm font-medium transition ${
      location.pathname === path
        ? 'bg-indigo-600 text-white'
        : 'text-slate-400 hover:text-white hover:bg-slate-800'
    }`

  return (
    <nav className="border-b border-slate-800 bg-slate-950/80 backdrop-blur sticky top-0 z-10">
      <div className="max-w-4xl mx-auto px-4 py-3 flex items-center justify-between">
        <Link to="/" className="font-bold text-indigo-400 tracking-tight">
          FocalPoint OS
        </Link>
        <div className="flex gap-1">
          <Link to="/briefs" className={linkClass('/briefs')}>Briefs</Link>
          <Link to="/travel" className={linkClass('/travel')}>Travel</Link>
          <Link to="/incidents" className={linkClass('/incidents')}>Incidents</Link>
        </div>
      </div>
    </nav>
  )
}

function Home() {
  return (
    <div className="max-w-4xl mx-auto px-4 py-10">
      <header className="mb-12">
        <h1 className="text-3xl sm:text-4xl font-bold text-white mb-3">
          FocalPoint OS
        </h1>
        <p className="text-slate-400 text-lg max-w-2xl">
          Practical tools for NGO Security Focal Points working in Kenya and East Africa.
          Clean outputs. Offline capable. Built for real field conditions.
        </p>
      </header>

      <div className="grid gap-5 sm:grid-cols-3">
        <Link to="/briefs" className="group p-6 rounded-2xl bg-slate-900 border border-slate-800 hover:border-indigo-500/50 transition">
          <div className="text-2xl mb-3">📋</div>
          <h2 className="text-lg font-semibold text-indigo-300 group-hover:text-indigo-200">Weekly Briefs</h2>
          <p className="text-slate-500 text-sm mt-2">Structured security updates for busy SFPs</p>
        </Link>

        <Link to="/travel" className="group p-6 rounded-2xl bg-slate-900 border border-slate-800 hover:border-indigo-500/50 transition">
          <div className="text-2xl mb-3">✈️</div>
          <h2 className="text-lg font-semibold text-indigo-300 group-hover:text-indigo-200">Travel Risk Packs</h2>
          <p className="text-slate-500 text-sm mt-2">One-page go / no-go checklists</p>
        </Link>

        <Link to="/incidents" className="group p-6 rounded-2xl bg-slate-900 border border-slate-800 hover:border-indigo-500/50 transition">
          <div className="text-2xl mb-3">📱</div>
          <h2 className="text-lg font-semibold text-indigo-300 group-hover:text-indigo-200">Incident Logger</h2>
          <p className="text-slate-500 text-sm mt-2">Offline-first field reporting</p>
        </Link>
      </div>

      <footer className="mt-20 text-center text-slate-600 text-sm">
        Research & coordination tool only • Not licensed security advice
      </footer>
    </div>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-slate-950 text-slate-100">
        <Nav />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/briefs" element={<BriefsPage />} />
          <Route path="/travel" element={<TravelPage />} />
          <Route path="/incidents" element={<IncidentsPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}
