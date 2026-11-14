"""
GeoJSON export and illustrative public hotspot data for crisis mapping.
All points are illustrative and based on public-context knowledge only.
"""

from typing import Dict, Any, List

def get_public_hotspots_geojson(region: str = "Kenya") -> Dict[str, Any]:
    """
    Returns a GeoJSON FeatureCollection of illustrative public-context points.
    These are NOT real-time or authoritative. For coordination UI demos only.
    """
    features: List[Dict[str, Any]] = [
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [39.65, 0.45]},
            "properties": {
                "name": "Garissa area",
                "category": "attention",
                "note": "Elevated public attention (illustrative)",
                "region": region
            }
        },
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [35.6, 3.1]},
            "properties": {
                "name": "Turkana / West Pokot zone",
                "category": "monitoring",
                "note": "Ongoing monitoring (illustrative)",
                "region": region
            }
        },
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [36.8, -1.3]},
            "properties": {
                "name": "Nairobi urban",
                "category": "urban",
                "note": "Standard urban risk profile (illustrative)",
                "region": region
            }
        },
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [40.1, -2.3]},
            "properties": {
                "name": "Coastal corridor",
                "category": "monitoring",
                "note": "Public monitoring context (illustrative)",
                "region": region
            }
        }
    ]

    return {
        "type": "FeatureCollection",
        "features": features,
        "metadata": {
            "description": "Illustrative public-context points only. Not authoritative.",
            "region": region,
            "attribution": "Public knowledge / open context for coordination UI demos"
        }
    }
