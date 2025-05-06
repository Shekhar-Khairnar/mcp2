from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP


# intialize FastMCP server

mcp = FastMCP('Weather')

# constants

NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"


async def make_nws_request(url:str) -> dict[str, Any] | None:
    """
    Make a request to the NWS API with proper error handling.

    """
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"

    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None
        
def format_alert(feature: dict) -> str:
    """ Format an alert feature into a readable string."""
    props =feature['properties']
    return f"""
            Event: {props.get('event','Unkown')}
            Area: {props.get('areaDesc','Unknown')}
            Severity:  {props.get('severity', 'Unknown')}
            Description: {props.get('descripton','No description available')}
            Instruction: {props.get('instruction','No specific instructions provided')}
            """

@mcp.tool()
async def get_alerts(state: str) -> str:
    """
    Get weather alert for a US state.

    Args:
        state: Two-letter US state code (eg. NY) 
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    # print(f"[DEBUG] Requesting: {url}")  
    data = await make_nws_request(url)

    if not data or 'features' not in data:
        return 'Unable to fetch alerts or no alerts found'
    
    if not data['features']:
        return "No active alerts for this state"
    
    alerts = [format_alert(feature) for feature in data['features']]
    return "\n-----\n".join(alerts)


@mcp.resource("echo://{message}")
def echo_resource(message: str) -> str:
    """ Ecgo a message as a resource"""
    return f"Resource echo: {message}"