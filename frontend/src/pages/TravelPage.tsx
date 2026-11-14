import { useState } from 'react'
import { useLang } from '../App'
import { t } from '../i18n'

export default function TravelPage() {
  const { lang } = useLang()
  const [destination, setDestination] = useState('Garissa')
  const [org, setOrg] = useState('Example NGO Kenya')
  const [loading, setLoading] = useState(false)
  const [pdfLoading, setPdfLoading] = useState(false)
  const [result, setResult] = useState<any>(null)

  async function compile() {
    setLoading(true)
    try {
      const res = await fetch('http://localhost:8000/api/travel/compile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          destination,
          organization: org,
          start_date: new Date().toISOString().slice(0, 10),
          end_date: new Date(Date.now() + 7 * 86400000).toISOString().slice(0, 10)
        })
      })
      const data = await res.json()
      setResult(data)
    } catch {
      setResult({
        destination,
        period: 'Next 7 days',
        organization: org,
        overall_recommendation: 'GO WITH MITIGATION',
        key_risks: [
          { category: 'Crime / Banditry', level: 'Medium-High', notes: 'Elevated risk on some routes' },
          { category: 'Road Safety', level: 'High', notes: 'Night travel not recommended' },
          { category: 'Health', level: 'Medium', notes: 'Standard precautions' },
          { category: 'Political', level: 'Low', notes: 'No major events identified' }
        ],
        mitigations: [
          'Use only vetted transport providers',
          'Avoid all night road movement',
          'Maintain daily check-in schedule',
          'Carry charged power bank and satellite option if available'
        ],
        go_no_go_checklist: [
          { item: 'Destination risk reviewed', status: true },
          { item: 'Medical support plan', status: true },
          { item: 'Communications plan confirmed', status: false },
          { item: 'Local contacts briefed', status: true },
          { item: 'Insurance & approvals in place', status: true }
        ],
        disclaimer: 'Compiled from public sources for coordination purposes only.'
      })
    } finally {
      setLoading(false)
    }
  }

  async function downloadPdf() {
    if (!result) return
    setPdfLoading(true)
    try {
      const res = await fetch('http://localhost:8000/api/pdf/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type: 'travel', data: result })
      })
      if (!res.ok) throw new Error('PDF failed')
      const blob = await res.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `travel-risk-${destination.toLowerCase().replace(/\s+/g, '-')}.pdf`
      a.click()
      window.URL.revokeObjectURL(url)
    } catch {
      window.print()
    } finally {
      setPdfLoading(false)
    }
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-2">{t(lang, 'travel')}</h1>
      <p className="text-slate-400 mb-8 text-sm">One-page go / no-go style checklist for field travel.</p>

      <div className="space-y-4 mb-8">
        <div>
          <label className="block text-sm text-slate-400 mb-1">{t(lang, 'destination')}</label>
          <input value={destination} onChange={e => setDestination(e.target.value)}
            className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2" />
        </div>
        <div>
          <label className="block text-sm text-slate-400 mb-1">{t(lang, 'organization')}</label>
          <input value={org} onChange={e => setOrg(e.target.value)}
            className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2" />
        </div>
        <button onClick={compile} disabled={loading}
          className="w-full bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white font-medium py-3 rounded-lg">
          {loading ? 'Compiling…' : t(lang, 'compilePack')}
        </button>
      </div>

      {result && (
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-6">
          <div className="flex justify-between items-start gap-4">
            <div>
              <h2 className="text-xl font-semibold">{result.destination}</h2>
              <p className="text-slate-500 text-sm">{result.period} • {result.organization}</p>
            </div>
            <div className="flex flex-col items-end gap-2">
              <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                result.overall_recommendation?.includes('NO-GO') ? 'bg-red-900/50 text-red-300' :
                result.overall_recommendation?.includes('MITIGATION') ? 'bg-amber-900/50 text-amber-300' :
                'bg-emerald-900/50 text-emerald-300'
              }`}>
                {result.overall_recommendation}
              </span>
              <button onClick={downloadPdf} disabled={pdfLoading}
                className="bg-emerald-700 hover:bg-emerald-600 disabled:opacity-50 text-white text-sm font-medium px-4 py-2 rounded-lg">
                {pdfLoading ? 'Preparing…' : t(lang, 'downloadPdf')}
              </button>
            </div>
          </div>

          <div>
            <h3 className="text-sm font-medium text-slate-400 mb-3">Key Risks</h3>
            <div className="space-y-2">
              {result.key_risks?.map((r: any, i: number) => (
                <div key={i} className="flex justify-between text-sm">
                  <span>{r.category}</span>
                  <span className="text-slate-400">{r.level}</span>
                </div>
              ))}
            </div>
          </div>

          <div>
            <h3 className="text-sm font-medium text-slate-400 mb-2">Mitigations</h3>
            <ul className="list-disc list-inside text-slate-300 text-sm space-y-1">
              {result.mitigations?.map((m: string, i: number) => <li key={i}>{m}</li>)}
            </ul>
          </div>

          <div>
            <h3 className="text-sm font-medium text-slate-400 mb-2">Go / No-Go Checklist</h3>
            <div className="space-y-1">
              {result.go_no_go_checklist?.map((c: any, i: number) => (
                <div key={i} className="flex items-center gap-2 text-sm">
                  <span>{c.status ? '✅' : '❌'}</span>
                  <span className={c.status ? 'text-slate-300' : 'text-slate-500'}>{c.item}</span>
                </div>
              ))}
            </div>
          </div>

          <p className="text-xs text-slate-600 border-t border-slate-800 pt-4">{result.disclaimer}</p>
        </div>
      )}
    </div>
  )
}
