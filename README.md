
# KMB FastMCP Server

## 簡介 (Introduction)
本專案是一個基於 [FastMCP](https://github.com/jlowin/fastmcp) 的九巴（KMB）API 代理伺服器，提供多種巴士路線、站點、即時到站、票價等查詢工具，並可輕鬆擴充。適合自動化、n8n、AI 應用等場景。

This project is a FastMCP-based proxy server for Kowloon Motor Bus (KMB) public API, providing tools for route, stop, ETA, fare and more. Easy to extend and suitable for automation, n8n, and AI scenarios.
![image](https://github.com/user-attachments/assets/581988af-230e-4de2-bedb-2d38f801b3db)
![image](https://github.com/user-attachments/assets/92c4e074-025c-4b7a-9209-faf31195759a)

---

## 安裝與啟動 (Install & Run)

1. 安裝依賴 (Install dependencies)：
   - 推薦使用 [uv](https://github.com/astral-sh/uv)（官方推薦）
   ```bash
   uv pip install -r pyproject.toml
   ```
   - 或使用 pip：
   ```bash
   pip install -r pyproject.toml
   ```
2. 啟動伺服器 (Start server)-sse：
   ```bash
   fastmcp run server.py:mcp --transport sse --port 8080 --host 0.0.0.0
   # 或 (or)
   python server.py
   ```

---

## 主要工具 (Main Tools)

- `get_kmb_routes()`
  - 查詢所有九巴路線 (Get all KMB routes)
- `get_kmb_route_detail(route, direction, service_type)`
  - 查詢指定路線詳細 (Get route detail)
- `find_routes_by_stop_name(stop_name)`
  - 以站名查詢經過路線 (Find all routes passing a stop by name)
- `get_stops_by_route(route, direction, service_type)`
  - 查詢路線所有站點 (Get all stops for a route)
- `get_eta_by_stop(stop_id)`
  - 查詢站點即時到站時間 (Get ETA for all routes at a stop)
- `get_eta_by_stop_and_route(stop_id, route, service_type)`
  - 查詢某站某路線即時到站時間 (Get ETA for a route at a stop)
- `get_stop_detail(stop_id)`
  - 查詢站點詳細資料 (Get stop detail)
- `get_fare_by_route(route, direction, service_type)`
  - 查詢路線票價（如有）(Get fare info for a route, if available)

---

## 範例 (Example)

### 查詢所有路線 (Get all routes)
```json
{
  "tool": "get_kmb_routes"
}
```

### 以站名查詢經過路線 (Find routes by stop name)
```json
{
  "tool": "find_routes_by_stop_name",
  "stop_name": "美林"
}
```

### 查詢即時到站 (Get ETA)
```json
{
  "tool": "get_eta_by_stop",
  "stop_id": "A3ADFCDF8487ADB9"
}
```

---

## 其他 (Others)
- 本專案僅用於學術/技術交流，資料來源：KMB 公開 API。
- This project is for academic/technical use only. Data source: KMB Open API. 

