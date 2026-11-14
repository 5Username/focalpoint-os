"""
Ethical public OSINT collectors.

Rules:
- Only public, openly available sources
- Always attribute the source
- No scraping behind logins, no paid APIs without keys, no private data
- Rate-limit friendly
- Designed for humanitarian / NGO coordination use
"""

from typing import List, Dict, Any
from datetime import datetime

def collect_public_sources(region: str = "Kenya") -> List[Dict[str, Any]]:
    """
    Returns a list of public source summaries.
    In production these would call real public endpoints (ReliefWeb, government sites, etc.)
    with proper attribution and caching.
    """
    # Placeholder structure that demonstrates ethical approach
    sources = [
        {
            "source": "Public open reporting (aggregated)",
            "region": region,
            "type": "crime_and_security",
            "summary": "Publicly reported incidents continue to follow established patterns in known hotspot areas. No exceptional escalation noted in open sources for the current period.",
            "retrieved_at": datetime.utcnow().isoformat() + "Z",
            "attribution": "Compiled from openly available public reports"
        },
        {
            "source": "Public health advisories",
            "region": region,
            "type": "health",
            "summary": "Standard seasonal health guidance remains in effect. No major new public health emergencies declared in the primary operating areas.",
            "retrieved_at": datetime.utcnow().isoformat() + "Z",
            "attribution": "Public health authority releases and open bulletins"
        },
        {
            "source": "Open political & civil reporting",
            "region": region,
            "type": "political",
            "summary": "No major political violence events recorded in open sources during the review period. Routine monitoring of planned gatherings continues.",
            "retrieved_at": datetime.utcnow().isoformat() + "Z",
            "attribution": "Open media and public statements"
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
        "recommendations": [
            "Maintain current security posture",
            "Continue restrictions on non-essential night road movement in higher-risk areas",
            "Ensure staff contact cascade is up to date",
            "Review pending travel against latest public assessments"
        ],
        "sources_used": [{"name": s["source"], "attribution": s["attribution"]} for s in sources]
    }
