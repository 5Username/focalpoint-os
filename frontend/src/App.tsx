import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'

function Home() {
  return (
    <div className="min-h-screen p-6 max-w-3xl mx-auto">
      <header className="mb-10">
        <h1 className="text-3xl font-bold text-indigo-400 mb-2">FocalPoint OS</h1>
        <p className="text-slate-400">Toolkit for NGO Security Focal Points</p>
      </header>

      <div className="grid gap-4">
        <Link to="/briefs" className="block p-5 rounded-xl bg-slate-900 border border-slate-800 hover:border-indigo-500 transition">
          <h2 className="text-xl font-semibold text-indigo-300">Weekly Security Briefs</h2>
          <p className="text-slate-400 mt-1 text-sm">Automated OSINT compilation for busy SFPs</p>
        </Link>

        <Link to="/travel" className="block p-5 rounded-xl bg-slate-900 border border-slate-800 hover:border-indigo-500 transition">
          <h2 className="text-xl font-semibold text-indigo-300">Travel Risk Packs</h2>
          <p className="text-slate-400 mt-1 text-sm">One-page go/no-go checklists</p>
        </Link>

        <Link to="/incidents" className="block p-5 rounded-xl bg-slate-900 border border-slate-800 hover:border-indigo-500 transition">
          <h2 className="text-xl font-semibold text-indigo-300">Incident Reporting</h2>
          <p className="text-slate-400 mt-1 text-sm">Offline-capable field logging + Google Sheets sync</p>
        </Link>
      </div>

      <footer className="mt-16 text-center text-slate-600 text-sm">
        Built for real field operations in Kenya & East Africa
      </footer>
    </div>
  )
}

function Placeholder({ title }: { title: string }) {
  return (
    <div className="min-h-screen p-6 max-w-3xl mx-auto">
      <Link to="/" className="text-indigo-400 text-sm mb-6 inline-block">← Back</Link>
      <h1 className="text-2xl font-bold mb-4">{title}</h1>
      <p className="text-slate-400">Module under active development. Backend API is already live.</p>
    </div>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/briefs" element={<Placeholder title="Weekly Security Briefs" />} />
        <Route path="/travel" element={<Placeholder title="Travel Risk Pack Compiler" />} />
        <Route path="/incidents" element={<Placeholder title="Offline Incident Logger" />} />
      </Routes>
    </BrowserRouter>
  )
}
