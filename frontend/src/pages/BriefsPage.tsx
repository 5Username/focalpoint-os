import { useState } from 'react'
import { useLang } from '../App'
import { t } from '../i18n'

export default function BriefsPage() {
  const { lang } = useLang()
  const [org, setOrg] = useState('Example NGO Kenya')
  const [region, setRegion] = useState('Kenya')
  const [loading, setLoading] = useState(false)
  const [pdfLoading, setPdfLoading] = useState(false)
  const [result, setResult] = useState<any>(null)

  async function generate() {
    setLoading(true)
    try {
      const res = await fetch('http://localhost:8000/api/briefs/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ organization: org, region, language: lang })
      })
      const data = await res.json()
      setResult(data)
    } catch {
      setResult({
        title: `Weekly Security Brief — ${org}`,
        region,
        week_of: new Date().toISOString().slice(0, 10),
        sections: {
          executive_summary: 'Key developments this week remain within normal parameters for the operating environment.',
          crime_and_banditry: 'Public reporting indicates continued incidents in traditional hotspot counties.',
          political_security: 'No significant political violence reported.',
          terrorism_and_extremism: 'No new public claims of significance.',
          health_and_disease: 'Standard seasonal health advisories apply.',
          humanitarian_context: 'Public humanitarian indicators remain elevated in several known areas.',
          recommendations: [
            'Maintain current security posture',
            'Continue restrictions on night road movement in high-risk counties',
            'Ensure staff receive updated contact cascade',
            'Review travel requests against latest assessments'
          ]
        },
        disclaimer: 'This is a research and coordination product compiled from public sources. It is not licensed security advice.'
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
        body: JSON.stringify({ type: 'brief', data: result })
      })
      if (!res.ok) throw new Error('PDF generation failed')
      const blob = await res.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `weekly-brief-${region.toLowerCase().replace(/\s+/g, '-')}.pdf`
      a.click()
      window.URL.revokeObjectURL(url)
    } catch {
      // Fallback: use browser print
      window.print()
    } finally {
      setPdfLoading(false)
    }
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-2">{t(lang, 'briefs')}</h1>
      <p className="text-slate-400 mb-8 text-sm">Generate a clean, structured brief for your organisation.</p>

      <div className="space-y-4 mb-8">
        <div>
          <label className="block text-sm text-slate-400 mb-1">{t(lang, 'organization')}</label>
          <input value={org} onChange={e => setOrg(e.target.value)}
            className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white" />
        </div>
        <div>
          <label className="block text-sm text-slate-400 mb-1">{t(lang, 'region')}</label>
          <input value={region} onChange={e => setRegion(e.target.value)}
            className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white" />
        </div>
        <button onClick={generate} disabled={loading}
          className="w-full bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white font-medium py-3 rounded-lg transition">
          {loading ? 'Generating…' : t(lang, 'generateBrief')}
        </button>
      </div>

      {result && (
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-5">
          <div className="flex justify-between items-start gap-4">
            <div>
              <h2 className="text-xl font-semibold text-indigo-300">{result.title}</h2>
              <p className="text-slate-500 text-sm mt-1">{result.region} • Week of {result.week_of}</p>
            </div>
            <button onClick={downloadPdf} disabled={pdfLoading}
              className="shrink-0 bg-emerald-700 hover:bg-emerald-600 disabled:opacity-50 text-white text-sm font-medium px-4 py-2 rounded-lg">
              {pdfLoading ? 'Preparing…' : t(lang, 'downloadPdf')}
            </button>
          </div>

          {Object.entries(result.sections || {}).map(([key, value]) => (
            key === 'sources_used' ? null : (
              <div key={key}>
                <h3 className="text-sm font-medium text-slate-400 uppercase tracking-wide mb-1">
                  {key.replace(/_/g, ' ')}
                </h3>
                {Array.isArray(value) ? (
                  <ul className="list-disc list-inside text-slate-300 space-y-1">
                    {(value as string[]).map((item, i) => <li key={i}>{item}</li>)}
                  </ul>
                ) : (
                  <p className="text-slate-300 leading-relaxed">{value as string}</p>
                )}
              </div>
            )
          ))}

          <p className="text-xs text-slate-600 border-t border-slate-800 pt-4">{result.disclaimer}</p>
        </div>
      )}
    </div>
  )
}
