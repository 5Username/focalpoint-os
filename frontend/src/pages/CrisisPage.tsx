import { useEffect, useRef, useState } from 'react'
import { useLang } from '../App'
import { t } from '../i18n'

type LayerKey = 'attention' | 'monitoring' | 'urban' | 'heatmap'

const LAYER_LABELS: Record<LayerKey, string> = {
  attention: 'Attention Zones',
  monitoring: 'Monitoring',
  urban: 'Urban Context',
  heatmap: 'Heatmap Overlay'
}

export default function CrisisPage() {
  const { lang } = useLang()
  const mapRef = useRef<HTMLDivElement>(null)
  const mapInstance = useRef<any>(null)
  const layerGroups = useRef<Record<string, any>>({})
  const [activeLayers, setActiveLayers] = useState<Record<LayerKey, boolean>>({
    attention: true,
    monitoring: true,
    urban: true,
    heatmap: false
  })

  const points = [
    { lat: 0.45, lng: 39.65, title: 'Garissa area', note: 'Elevated public attention', category: 'attention' as LayerKey, intensity: 0.9 },
    { lat: 3.1, lng: 35.6, title: 'Turkana / West Pokot', note: 'Ongoing monitoring', category: 'monitoring' as LayerKey, intensity: 0.7 },
    { lat: -1.3, lng: 36.8, title: 'Nairobi urban', note: 'Standard urban profile', category: 'urban' as LayerKey, intensity: 0.5 },
    { lat: -2.3, lng: 40.1, title: 'Coastal corridor', note: 'Public monitoring', category: 'monitoring' as LayerKey, intensity: 0.6 }
  ]

  // Illustrative polygons (rough areas)
  const polygons = [
    {
      coords: [[0.2, 39.3], [0.7, 39.3], [0.7, 40.0], [0.2, 40.0]],
      name: 'North-Eastern attention zone',
      category: 'attention'
    },
    {
      coords: [[2.5, 35.0], [3.5, 35.0], [3.5, 36.2], [2.5, 36.2]],
      name: 'North Rift monitoring area',
      category: 'monitoring'
    }
  ]

  useEffect(() => {
    if (typeof window === 'undefined' || !mapRef.current) return

    const css = document.createElement('link')
    css.rel = 'stylesheet'
    css.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'
    document.head.appendChild(css)

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

      // Create layer groups
      layerGroups.current.attention = L.layerGroup().addTo(map)
      layerGroups.current.monitoring = L.layerGroup().addTo(map)
      layerGroups.current.urban = L.layerGroup().addTo(map)
      layerGroups.current.heatmap = L.layerGroup()

      // Markers
      points.forEach(p => {
        const marker = L.marker([p.lat, p.lng])
          .bindPopup(`<strong>${p.title}</strong><br/>${p.note}`)
        layerGroups.current[p.category].addLayer(marker)
      })

      // Polygons
      polygons.forEach(poly => {
        const polygon = L.polygon(poly.coords, {
          color: poly.category === 'attention' ? '#ef4444' : '#f59e0b',
          weight: 2,
          fillOpacity: 0.15
        }).bindPopup(poly.name)
        layerGroups.current[poly.category].addLayer(polygon)
      })

      // Simple heatmap using circle markers with opacity (no extra plugin required)
      points.forEach(p => {
        const circle = L.circleMarker([p.lat, p.lng], {
          radius: 18 + p.intensity * 20,
          color: '#ef4444',
          fillColor: '#ef4444',
          fillOpacity: 0.15 + p.intensity * 0.25,
          weight: 0
        })
        layerGroups.current.heatmap.addLayer(circle)
      })

      mapInstance.current = map
    }
    document.body.appendChild(script)

    return () => {
      if (mapInstance.current) {
        mapInstance.current.remove()
        mapInstance.current = null
      }
    }
  }, [])

  useEffect(() => {
    const map = mapInstance.current
    if (!map) return
    ;(Object.keys(activeLayers) as LayerKey[]).forEach(key => {
      const group = layerGroups.current[key]
      if (!group) return
      if (activeLayers[key]) {
        if (!map.hasLayer(group)) map.addLayer(group)
      } else {
        if (map.hasLayer(group)) map.removeLayer(group)
      }
    })
  }, [activeLayers])

  function toggleLayer(key: LayerKey) {
    setActiveLayers(prev => ({ ...prev, [key]: !prev[key] }))
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-2">{t(lang, 'crisis')}</h1>
      <p className="text-slate-400 mb-6 text-sm">
        Humanitarian context with polygons, markers and heatmap overlay (illustrative public data only).
      </p>

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
        <div ref={mapRef} style={{ height: '400px', width: '100%' }} />
        <div className="p-3 text-xs text-slate-500 border-t border-slate-800 flex justify-between flex-wrap gap-2">
          <span>Map data © OpenStreetMap • All layers illustrative only</span>
          <a href="http://localhost:8000/api/geo/hotspots.geojson" className="text-indigo-400 hover:underline" target="_blank" rel="noreferrer">
            Download GeoJSON
          </a>
        </div>
      </div>

      <p className="text-xs text-slate-600">
        {t(lang, 'disclaimer')}
      </p>
    </div>
  )
}
