import { useState, createContext, useContext } from 'react'
import { BrowserRouter, Routes, Route, Link, useLocation } from 'react-router-dom'
import BriefsPage from './pages/BriefsPage'
import TravelPage from './pages/TravelPage'
import IncidentsPage from './pages/IncidentsPage'
import CrisisPage from './pages/CrisisPage'
import { t, availableLanguages, Lang } from './i18n'

const LangContext = createContext<{ lang: Lang; setLang: (l: Lang) => void }>({
  lang: 'en',
  setLang: () => {}
})

export function useLang() {
  return useContext(LangContext)
}

function Nav() {
  const location = useLocation()
  const { lang, setLang } = useLang()

  const linkClass = (path: string) =>
    `px-3 py-2 rounded-lg text-sm font-medium transition ${
      location.pathname === path
        ? 'bg-indigo-600 text-white'
        : 'text-slate-400 hover:text-white hover:bg-slate-800'
    }`

  return (
    <nav className="border-b border-slate-800 bg-slate-950/80 backdrop-blur sticky top-0 z-10">
      <div className="max-w-5xl mx-auto px-4 py-3 flex flex-wrap items-center justify-between gap-3">
        <Link to="/" className="font-bold text-indigo-400 tracking-tight">
          {t(lang, 'appName')}
        </Link>

        <div className="flex flex-wrap items-center gap-1">
          <Link to="/briefs" className={linkClass('/briefs')}>{t(lang, 'briefs')}</Link>
          <Link to="/travel" className={linkClass('/travel')}>{t(lang, 'travel')}</Link>
          <Link to="/incidents" className={linkClass('/incidents')}>{t(lang, 'incidents')}</Link>
          <Link to="/crisis" className={linkClass('/crisis')}>{t(lang, 'crisis')}</Link>

          <select
            value={lang}
            onChange={(e) => setLang(e.target.value as Lang)}
            className="ml-2 bg-slate-900 border border-slate-700 text-slate-300 text-sm rounded-lg px-2 py-1.5"
            aria-label={t(lang, 'language')}
          >
            {availableLanguages.map((l) => (
              <option key={l.code} value={l.code}>{l.label}</option>
            ))}
          </select>
        </div>
      </div>
    </nav>
  )
}

function Home() {
  const { lang } = useLang()

  return (
    <div className="max-w-5xl mx-auto px-4 py-10">
      <header className="mb-12">
        <h1 className="text-3xl sm:text-4xl font-bold text-white mb-3">
          {t(lang, 'appName')}
        </h1>
        <p className="text-slate-400 text-lg max-w-2xl">
          {t(lang, 'tagline')}. Clean outputs. Offline capable. Built for real field conditions.
        </p>
      </header>

      <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <Link to="/briefs" className="group p-6 rounded-2xl bg-slate-900 border border-slate-800 hover:border-indigo-500/50 transition">
          <div className="text-2xl mb-3">📋</div>
          <h2 className="text-lg font-semibold text-indigo-300">{t(lang, 'briefs')}</h2>
          <p className="text-slate-500 text-sm mt-2">Structured security updates for busy SFPs</p>
        </Link>

        <Link to="/travel" className="group p-6 rounded-2xl bg-slate-900 border border-slate-800 hover:border-indigo-500/50 transition">
          <div className="text-2xl mb-3">✈️</div>
          <h2 className="text-lg font-semibold text-indigo-300">{t(lang, 'travel')}</h2>
          <p className="text-slate-500 text-sm mt-2">One-page go / no-go checklists</p>
        </Link>

        <Link to="/incidents" className="group p-6 rounded-2xl bg-slate-900 border border-slate-800 hover:border-indigo-500/50 transition">
          <div className="text-2xl mb-3">📱</div>
          <h2 className="text-lg font-semibold text-indigo-300">{t(lang, 'incidents')}</h2>
          <p className="text-slate-500 text-sm mt-2">Offline-first field reporting</p>
        </Link>

        <Link to="/crisis" className="group p-6 rounded-2xl bg-slate-900 border border-slate-800 hover:border-indigo-500/50 transition">
          <div className="text-2xl mb-3">🗺️</div>
          <h2 className="text-lg font-semibold text-indigo-300">{t(lang, 'crisis')}</h2>
          <p className="text-slate-500 text-sm mt-2">Humanitarian context overview</p>
        </Link>
      </div>

      <footer className="mt-20 text-center text-slate-600 text-sm">
        {t(lang, 'disclaimer')}
      </footer>
    </div>
  )
}

export default function App() {
  const [lang, setLang] = useState<Lang>('en')

  return (
    <LangContext.Provider value={{ lang, setLang }}>
      <BrowserRouter>
        <div className="min-h-screen bg-slate-950 text-slate-100">
          <Nav />
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/briefs" element={<BriefsPage />} />
            <Route path="/travel" element={<TravelPage />} />
            <Route path="/incidents" element={<IncidentsPage />} />
            <Route path="/crisis" element={<CrisisPage />} />
          </Routes>
        </div>
      </BrowserRouter>
    </LangContext.Provider>
  )
}
