"""
Ethical public OSINT collectors — ReliefWeb style approach.

Rules followed:
- Only publicly available sources
- Always attribute
- No private data, no login walls
- Suitable for humanitarian / NGO coordination
"""

from typing import List, Dict, Any
from datetime import datetime

def collect_public_sources(region: str = "Kenya") -> List[Dict[str, Any]]:
    """
    Structured public source summaries.
    In production these would call real public endpoints
    (ReliefWeb API, government open data, public advisories)
    with caching and rate limiting.
    """
    now = datetime.utcnow().isoformat() + "Z"

    sources = [
        {
            "source": "Public open reporting (aggregated)",
            "region": region,
            "type": "crime_and_security",
            "summary": "Publicly reported incidents continue to follow established patterns in known hotspot areas. No exceptional escalation noted in open sources for the current period.",
            "retrieved_at": now,
            "attribution": "Compiled from openly available public reports"
        },
        {
            "source": "Public health advisories",
            "region": region,
            "type": "health",
            "summary": "Standard seasonal health guidance remains in effect. No major new public health emergencies declared in the primary operating areas.",
            "retrieved_at": now,
            "attribution": "Public health authority releases and open bulletins"
        },
        {
            "source": "Open political & civil reporting",
            "region": region,
            "type": "political",
            "summary": "No major political violence events recorded in open sources during the review period. Routine monitoring of planned gatherings continues.",
            "retrieved_at": now,
            "attribution": "Open media and public statements"
        },
        {
            "source": "Humanitarian context (public)",
            "region": region,
            "type": "humanitarian",
            "summary": "Public humanitarian updates indicate ongoing needs in traditional areas of concern. Access constraints remain largely consistent with previous periods.",
            "retrieved_at": now,
            "attribution": "Public humanitarian situation reports and open datasets"
        },
        {
            "source": "Displacement & protection (public)",
            "region": region,
            "type": "protection",
            "summary": "Open data sources show stable displacement figures relative to the previous reporting window. Protection concerns continue to be monitored through public channels.",
            "retrieved_at": now,
            "attribution": "Public displacement tracking and protection monitoring summaries"
        }
    ]
    return sources

def build_brief_sections(region: str = "Kenya") -> Dict[str, Any]:
    sources = collect_public_sources(region)
    return {
        "executive_summary": "Overall environment remains within expected parameters based on publicly available information. No major escalations identified in open sources.",
        "crime_and_banditry": next((s["summary"] for s in sources if s["type"] == "crime_and_security"), "No significant public updates."),
        "political_security": next((s["summary"] for s in sources if s["type"] == "political"), "No significant public updates."),
        "terrorism_and_extremism": "No new public claims of operational significance identified in open sources during this period. Existing posture remains appropriate.",
        "health_and_disease": next((s["summary"] for s in sources if s["type"] == "health"), "Standard advisories apply."),
        "humanitarian_context": next((s["summary"] for s in sources if s["type"] == "humanitarian"), "No major new public updates."),
        "recommendations": [
            "Maintain current security posture",
            "Continue restrictions on non-essential night road movement in higher-risk areas",
            "Ensure staff contact cascade is up to date",
            "Review pending travel against latest public assessments"
        ],
        "sources_used": [{"name": s["source"], "attribution": s["attribution"]} for s in sources]
    }

def get_crisis_overview(region: str = "East Africa") -> Dict[str, Any]:
    """Simple humanitarian crisis overview structure for mapping / dashboard use."""
    return {
        "region": region,
        "updated": datetime.utcnow().isoformat() + "Z",
        "summary": "Public humanitarian indicators remain elevated in several areas. This overview is compiled exclusively from open sources for coordination purposes.",
        "key_themes": [
            {"theme": "Food security", "status": "Stressed in several zones", "trend": "stable"},
            {"theme": "Displacement", "status": "Ongoing in known areas", "trend": "stable"},
            {"theme": "Access constraints", "status": "Present on some routes", "trend": "stable"},
            {"theme": "Protection", "status": "Requires continued monitoring", "trend": "stable"}
        ],
        "disclaimer": "For research and coordination only. Not an official humanitarian assessment."
    }
