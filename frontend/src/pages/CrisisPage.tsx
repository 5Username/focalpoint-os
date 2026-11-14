import { useLang } from '../App'
import { t } from '../i18n'

export default function CrisisPage() {
  const { lang } = useLang()

  // Demo data — in production this would come from the ethical OSINT service
  const overview = {
    region: 'East Africa',
    summary: 'Public humanitarian indicators remain elevated in several areas. This overview is compiled exclusively from open sources for coordination purposes.',
    themes: [
      { theme: 'Food security', status: 'Stressed in several zones', trend: 'stable' },
      { theme: 'Displacement', status: 'Ongoing in known areas', trend: 'stable' },
      { theme: 'Access constraints', status: 'Present on some routes', trend: 'stable' },
      { theme: 'Protection', status: 'Requires continued monitoring', trend: 'stable' }
    ]
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-2">{t(lang, 'crisis')}</h1>
      <p className="text-slate-400 mb-8 text-sm">
        Lightweight humanitarian context overview for coordination (public sources only).
      </p>

      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-6">
        <div>
          <h2 className="text-lg font-semibold text-indigo-300">{overview.region}</h2>
          <p className="text-slate-400 text-sm mt-1">{overview.summary}</p>
        </div>

        <div>
          <h3 className="text-sm font-medium text-slate-400 mb-3">Key Themes</h3>
          <div className="space-y-3">
            {overview.themes.map((item, i) => (
              <div key={i} className="flex justify-between items-start border-b border-slate-800 pb-2">
                <div>
                  <div className="font-medium">{item.theme}</div>
                  <div className="text-sm text-slate-500">{item.status}</div>
                </div>
                <span className="text-xs px-2 py-1 rounded bg-slate-800 text-slate-400">{item.trend}</span>
              </div>
            ))}
          </div>
        </div>

        <p className="text-xs text-slate-600 border-t border-slate-800 pt-4">
          {t(lang, 'disclaimer')}
        </p>
      </div>

      <p className="mt-6 text-sm text-slate-500">
        Future versions will support simple map layers (Leaflet) and GeoJSON export of public hotspot areas.
      </p>
    </div>
  )
}
