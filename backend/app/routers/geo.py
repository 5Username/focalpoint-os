from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.services.geo import get_public_hotspots_geojson

router = APIRouter()

@router.get("/hotspots")
def public_hotspots(region: str = "Kenya"):
    """Return illustrative public hotspot data as GeoJSON."""
    data = get_public_hotspots_geojson(region)
    return JSONResponse(content=data)

@router.get("/hotspots.geojson")
def public_hotspots_download(region: str = "Kenya"):
    """Same data with Content-Disposition so browsers download it as .geojson."""
    data = get_public_hotspots_geojson(region)
    return JSONResponse(
        content=data,
        headers={"Content-Disposition": f"attachment; filename=focalpoint-hotspots-{region.lower()}.geojson"}
    )
