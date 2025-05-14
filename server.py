import logging
import requests
from fastmcp import FastMCP
import datetime
 
# 設定 logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

KMB_BASE_URL = "https://data.etabus.gov.hk/v1/transport/kmb"

mcp = FastMCP("KMB API Server 🚍")

@mcp.tool()
def get_kmb_routes() -> list:
    """Get all KMB bus routes.

    Returns:
        list: A list of all KMB bus routes with basic info.
    """
    url = f"{KMB_BASE_URL}/route/"
    logger.info(f"Fetching all KMB routes: {url}")
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json().get("data", [])
        logger.info(f"Fetched {len(data)} routes.")
        return data
    except Exception as e:
        logger.error(f"Error fetching KMB routes: {e}")
        return []

@mcp.tool()
def get_kmb_route_detail(route: str, direction: str, service_type: str) -> dict:
    """Get detail of a specific KMB route (including fare, origin, destination).

    Args:
        route (str): Route number (e.g. '74B').
        direction (str): 'inbound' or 'outbound'.
        service_type (str): Service type (usually '1').

    Returns:
        dict: Route detail info, or error message.
    """
    url = f"{KMB_BASE_URL}/route/{route}/{direction}/{service_type}"
    logger.info(f"Fetching KMB route detail: {url}")
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json().get("data", {})
        logger.info(f"Fetched detail for route {route} {direction} {service_type}.")
        return data
    except Exception as e:
        logger.error(f"Error fetching route detail: {e}")
        return {"error": str(e)}

@mcp.tool()
def find_routes_by_stop_name(stop_name: str) -> list:
    """Find all KMB routes passing through a stop by stop name (Chinese or English).

    Args:
        stop_name (str): The stop name to search for (e.g. '美林' or 'Mei Lam').

    Returns:
        list: A list of route numbers passing through the stop.
    """
    # 1. 取得所有站點
    stops_url = f"{KMB_BASE_URL}/stop"
    logger.info(f"Fetching all stops from {stops_url}")
    try:
        stops_resp = requests.get(stops_url, timeout=20)
        stops_resp.raise_for_status()
        stops = stops_resp.json().get("data", [])
        # 2. 找出站名包含 stop_name 的 stop_id
        matched_stops = [s["stop"] for s in stops if stop_name in s.get("name_tc", "") or stop_name.lower() in s.get("name_en", "").lower()]
        if not matched_stops:
            logger.info(f"No stop found for name: {stop_name}")
            return []
        logger.info(f"Matched stops: {matched_stops}")
        # 3. 取得所有路線-站點對應
        route_stops_url = f"{KMB_BASE_URL}/route-stop"
        logger.info(f"Fetching all route-stop mappings from {route_stops_url}")
        route_stops_resp = requests.get(route_stops_url, timeout=30)
        route_stops_resp.raise_for_status()
        route_stops = route_stops_resp.json().get("data", [])
        # 4. 找出經過這些 stop_id 的所有路線
        routes = set([rs["route"] for rs in route_stops if rs["stop"] in matched_stops])
        logger.info(f"Found {len(routes)} routes passing stop '{stop_name}'")
        return sorted(list(routes))
    except Exception as e:
        logger.error(f"Error in find_routes_by_stop_name: {e}")
        return []

@mcp.tool()
def get_stops_by_route(route: str, direction: str, service_type: str) -> list:
    """Get all stops for a specific KMB route.

    Args:
        route (str): Route number (e.g. '74B').
        direction (str): 'inbound' or 'outbound'.
        service_type (str): Service type (usually '1').

    Returns:
        list: List of stops (with stop_id, seq, etc.) for the route.
    """
    url = f"{KMB_BASE_URL}/route-stop/{route}/{direction}/{service_type}"
    logger.info(f"Fetching stops for route {route} {direction} {service_type}: {url}")
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        data = resp.json().get("data", [])
        logger.info(f"Fetched {len(data)} stops for route {route}.")
        return data
    except Exception as e:
        logger.error(f"Error fetching stops for route: {e}")
        return []

@mcp.tool()
def get_eta_by_stop(stop_id: str) -> list:
    """Get real-time ETA for all routes at a specific stop.

    Args:
        stop_id (str): The stop ID (16 characters).

    Returns:
        list: List of ETA info for all routes at the stop.
    """
    url = f"{KMB_BASE_URL}/stop-eta/{stop_id}"
    logger.info(f"Fetching ETA for stop {stop_id}: {url}")
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json().get("data", [])
        logger.info(f"Fetched ETA for stop {stop_id}, count: {len(data)}.")
        return data
    except Exception as e:
        logger.error(f"Error fetching ETA for stop: {e}")
        return []

@mcp.tool()
def get_eta_by_stop_and_route(stop_id: str, route: str, service_type: str) -> list:
    """Get real-time ETA for a specific route at a specific stop.

    Args:
        stop_id (str): The stop ID (16 characters).
        route (str): Route number (e.g. '74B').
        service_type (str): Service type (usually '1').

    Returns:
        list: List of ETA info for the route at the stop.
    """
    url = f"{KMB_BASE_URL}/eta/{stop_id}/{route}/{service_type}"
    logger.info(f"Fetching ETA for stop {stop_id}, route {route}, service_type {service_type}: {url}")
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json().get("data", [])
        logger.info(f"Fetched ETA for stop {stop_id}, route {route}, count: {len(data)}.")
        return data
    except Exception as e:
        logger.error(f"Error fetching ETA for stop and route: {e}")
        return []

@mcp.tool()
def get_stop_detail(stop_id: str) -> dict:
    """Get detail information for a specific stop.

    Args:
        stop_id (str): The stop ID (16 characters).

    Returns:
        dict: Stop detail info (name, lat, long, etc.).
    """
    url = f"{KMB_BASE_URL}/stop/{stop_id}"
    logger.info(f"Fetching stop detail for {stop_id}: {url}")
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json().get("data", {})
        logger.info(f"Fetched stop detail for {stop_id}.")
        return data
    except Exception as e:
        logger.error(f"Error fetching stop detail: {e}")
        return {"error": str(e)}

@mcp.tool()
def get_fare_by_route(route: str, direction: str, service_type: str) -> dict:
    """Get fare information for a specific KMB route.

    Args:
        route (str): Route number (e.g. '74B').
        direction (str): 'inbound' or 'outbound'.
        service_type (str): Service type (usually '1').

    Returns:
        dict: Fare information (e.g. full fare, section fares, etc.), or error message.
    """
    url = f"{KMB_BASE_URL}/route/{route}/{direction}/{service_type}"
    logger.info(f"Fetching fare info for route {route} {direction} {service_type}: {url}")
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json().get("data", {})
        # 票價欄位名稱依 KMB API 回傳為主，常見有 fare, air_cond_fare, section_fares
        fare_info = {}
        for key in ["fare", "air_cond_fare", "section_fares", "fares"]:
            if key in data:
                fare_info[key] = data[key]
        if not fare_info:
            logger.info(f"No fare info found for route {route}.")
            return {"message": "No fare info found."}
        logger.info(f"Fare info for route {route}: {fare_info}")
        return fare_info
    except Exception as e:
        logger.error(f"Error fetching fare info: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    logger.info("Starting KMB FastMCP server...")
    mcp.run(transport="sse", host="0.0.0.0", port=8080) 
