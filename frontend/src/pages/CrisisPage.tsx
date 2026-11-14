import { useEffect, useRef, useState } from 'react'
import { useLang } from '../App'
import { t } from '../i18n'

type LayerKey = 'attention' | 'monitoring' | 'urban'

const LAYER_LABELS: Record<LayerKey, string> = {
  attention: 'Attention Zones',
  monitoring: 'Monitoring',
  urban: 'Urban Context'
}

export default function CrisisPage() {
  const { lang } = useLang()
  const mapRef = useRef<HTMLDivElement>(null)
  const mapInstance = useRef<any>(null)
  const markersRef = useRef<any[]>([])
  const [activeLayers, setActiveLayers] = useState<Record<LayerKey, boolean>>({
    attention: true,
    monitoring: true,
    urban: true
  })

  const points = [
    { lat: 0.45, lng: 39.65, title: 'Garissa area', note: 'Elevated public attention (illustrative)', category: 'attention' as LayerKey },
    { lat: 3.1, lng: 35.6, title: 'Turkana / West Pokot zone', note: 'Ongoing monitoring', category: 'monitoring' as LayerKey },
    { lat: -1.3, lng: 36.8, title: 'Nairobi urban', note: 'Standard urban risk profile', category: 'urban' as LayerKey },
    { lat: -2.3, lng: 40.1, title: 'Coastal corridor', note: 'Public monitoring context', category: 'monitoring' as LayerKey }
  ]

  function renderMarkers(L: any, map: any) {
    // Clear existing
    markersRef.current.forEach(m => map.removeLayer(m))
    markersRef.current = []

    points.forEach(p => {
      if (!activeLayers[p.category]) return
      const marker = L.marker([p.lat, p.lng])
        .addTo(map)
        .bindPopup(`<strong>${p.title}</strong><br/>${p.note}<br/><em>${LAYER_LABELS[p.category]}</em>`)
      markersRef.current.push(marker)
    })
  }

  useEffect(() => {
    if (typeof window === 'undefined' || !mapRef.current) return

    const link = document.createElement('link')
    link.rel = 'stylesheet'
    link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'
    document.head.appendChild(link)

    const script = document.createElement('script')
    script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'
    script.onload = () => {
      // @ts-ignore
      const L = window.L
      if (!L || mapInstance.current) return

      const map = L.map(mapRef.current).setView([0.5, 38], 6)
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
      }).addTo(map)

      mapInstance.current = map
      renderMarkers(L, map)
    }
    document.body.appendChild(script)

    return () => {
      if (mapInstance.current) {
        mapInstance.current.remove()
        mapInstance.current = null
      }
    }
  }, [])

  // Re-render markers when filters change
  useEffect(() => {
    // @ts-ignore
    const L = window.L
    if (L && mapInstance.current) {
      renderMarkers(L, mapInstance.current)
    }
  }, [activeLayers])

  function toggleLayer(key: LayerKey) {
    setActiveLayers(prev => ({ ...prev, [key]: !prev[key] }))
  }

  const overview = {
    region: 'East Africa / Kenya focus',
    summary: 'Public humanitarian indicators remain elevated in several areas. This overview is compiled exclusively from open sources for coordination purposes.',
    themes: [
      { theme: 'Food security', status: 'Stressed in several zones', trend: 'stable' },
      { theme: 'Displacement', status: 'Ongoing in known areas', trend: 'stable' },
      { theme: 'Access constraints', status: 'Present on some routes', trend: 'stable' },
      { theme: 'Protection', status: 'Requires continued monitoring', trend: 'stable' }
    ]
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-2">{t(lang, 'crisis')}</h1>
      <p className="text-slate-400 mb-6 text-sm">
        Humanitarian context overview + filterable public map layers (illustrative).
      </p>

      {/* Layer filters */}
      <div className="flex flex-wrap gap-2 mb-4">
        {(Object.keys(LAYER_LABELS) as LayerKey[]).map(key => (
          <button
            key={key}
            onClick={() => toggleLayer(key)}
            className={`text-xs px-3 py-1.5 rounded-full border transition ${
              activeLayers[key]
                ? 'bg-indigo-600 border-indigo-500 text-white'
                : 'bg-slate-900 border-slate-700 text-slate-400'
            }`}
          >
            {LAYER_LABELS[key]}
          </button>
        ))}
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden mb-6">
        <div ref={mapRef} style={{ height: '380px', width: '100%' }} />
        <div className="p-3 text-xs text-slate-500 border-t border-slate-800 flex justify-between">
          <span>Map data © OpenStreetMap • Markers illustrative only</span>
          <a href="http://localhost:8000/api/geo/hotspots.geojson" className="text-indigo-400 hover:underline" target="_blank" rel="noreferrer">
            Download GeoJSON
          </a>
        </div>
      </div>

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
    </div>
  )
}
