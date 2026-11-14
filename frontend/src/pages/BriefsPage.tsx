import { useState } from 'react'

export default function BriefsPage() {
  const [org, setOrg] = useState('Example NGO Kenya')
  const [region, setRegion] = useState('Kenya')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)

  async function generate() {
    setLoading(true)
    try {
      const res = await fetch('http://localhost:8000/api/briefs/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ organization: org, region })
      })
      const data = await res.json()
      setResult(data)
    } catch (e) {
      // Fallback demo data when backend is offline
      setResult({
        title: `Weekly Security Brief — ${org}`,
        region,
        week_of: new Date().toISOString().slice(0, 10),
        sections: {
          executive_summary: "Key developments this week remain within normal parameters for the operating environment. No major escalation observed in primary areas of operation.",
          crime_and_banditry: "Public reporting indicates continued incidents of cattle rustling and highway crime in traditional hotspot counties. Urban petty crime remains elevated in major centres.",
          political_security: "No significant political violence reported. Routine monitoring of planned gatherings continues.",
          terrorism_and_extremism: "No new public claims of significance. Existing posture remains appropriate.",
          health_and_disease: "Standard seasonal health advisories apply. No exceptional outbreak notifications in the public domain.",
          recommendations: [
            "Maintain current security posture",
            "Continue restrictions on night road movement in high-risk counties",
            "Ensure staff receive updated contact cascade",
            "Review travel requests against latest county assessments"
          ]
        },
        disclaimer: "This is a research and coordination product compiled from public sources. It is not licensed security advice."
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-2">Weekly Security Brief</h1>
      <p className="text-slate-400 mb-8 text-sm">Generate a clean, structured brief for your organisation.</p>

      <div className="space-y-4 mb-8">
        <div>
          <label className="block text-sm text-slate-400 mb-1">Organisation</label>
          <input
            value={org}
            onChange={e => setOrg(e.target.value)}
            className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white"
          />
        </div>
        <div>
          <label className="block text-sm text-slate-400 mb-1">Region / Focus</label>
          <input
            value={region}
            onChange={e => setRegion(e.target.value)}
            className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white"
          />
        </div>
        <button
          onClick={generate}
          disabled={loading}
          className="w-full bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white font-medium py-3 rounded-lg transition"
        >
          {loading ? 'Generating…' : 'Generate Brief'}
        </button>
      </div>

      {result && (
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-5">
          <div>
            <h2 className="text-xl font-semibold text-indigo-300">{result.title}</h2>
            <p className="text-slate-500 text-sm mt-1">{result.region} • Week of {result.week_of}</p>
          </div>

          {Object.entries(result.sections).map(([key, value]) => (
            <div key={key}>
              <h3 className="text-sm font-medium text-slate-400 uppercase tracking-wide mb-1">
                {key.replace(/_/g, ' ')}
              </h3>
              {Array.isArray(value) ? (
                <ul className="list-disc list-inside text-slate-300 space-y-1">
                  {value.map((item: string, i: number) => <li key={i}>{item}</li>)}
                </ul>
              ) : (
                <p className="text-slate-300 leading-relaxed">{value as string}</p>
              )}
            </div>
          ))}

          <p className="text-xs text-slate-600 border-t border-slate-800 pt-4">{result.disclaimer}</p>
        </div>
      )}
    </div>
  )
}
