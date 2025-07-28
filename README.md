# Simple Lightroom Catalog Analytics

This repository provides tools to analyze your Adobe Lightroom Classic catalog, either by running local scripts and exporting to CSV/Excel, or by hosting an HTTP API for direct integration with tools like Excel or Google Sheets.

## Features

- **Analyze Lightroom catalog data**: Group by lens, camera, focal length, aperture, or shutter speed.
- **Export results to CSV for Excel/Sheets**: Use the script to generate CSV files for easy import.
- **Host a FastAPI HTTP API**: Query your catalog data over HTTP, with support for filtering and grouping.
- **API key authentication**: Secure your API endpoints.
- **Docker support**: Easily run the API in a container.

---

## Local Usage: Export CSV for Excel/Sheets

You can run the analysis locally and copy/paste the results into Excel or Google Sheets.

### Example: List Most Used Lenses

```bash
python3 csv_by_year_month.py --lookback 365 --property lensName --picks-only
```

This will generate `output.csv` with columns:

- `Year-Month` (e.g. `01.07.2025`)
- `lensName` (or other property)
- `Count`

Open `output.csv` in Excel or Google Sheets for further analysis.

---

## Hosting the API (Docker)

You can host the API to expose your catalog data directly to Excel, Google Sheets, or other tools.

### 1. Build and Run with Docker Compose

Create a `catalog` folder and place a copy of your Lightroom catalog file (e.g. `catalog-v13-3.lrcat`) inside it.

Sample `docker-compose.yml`:

```yaml
version: "3.8"

services:
  lightroom-api:
    image: ghcr.io/pppontusw/simple-lightroom-analytics-api:latest
    ports:
      - "8089:8000"
    environment:
      - API_KEY=changeme
      - LR_CATALOG_FILE=/catalog/catalog-v13-3.lrcat
    volumes:
      - /catalog:/catalog:rw
    restart: unless-stopped
```

Build and start:

```bash
docker-compose up --build
```

### 2. Query the API

Example (JSON):

```
curl "http://localhost:8089/by_year_month?property=cameraName&days_back=30&picks_only=true&api_key=changeme"
```

Example (CSV, tab-separated):

```
curl "http://localhost:8089/by_year_month_csv?property=lensName&delimiter=tab&api_key=changeme"
```

You can import the CSV endpoint directly into Excel or Google Sheets using their "Import from web" features.

---

## API Endpoints

- `/by_year_month` — Returns grouped data in JSON format
- `/by_year_month_csv` — Returns grouped data in CSV format (supports `delimiter` query param: `,`, `;`, or `tab`)

### Query Parameters
- `days_back` — Number of days to look back (default: all)
- `property` — Group by: lensName, cameraName, focalLength, aperture, shutterSpeed
- `picks_only` — Only include flagged images
- `delimiter` (CSV only) — `,`, `;`, or `tab`
- `api_key` — API key for authentication
- `catalog_path` - (optional) path to the catalog, if you need to query multiple catalogs for example

---

## Security
- The API requires an API key, provided via the `X-API-Key` header or `api_key` query parameter.
- The Lightroom Catalog file includes all necessary metadata, the original photos are not required to be accessible at all from the script / api.
- Always use a copy of your Lightroom catalog and not the original.
- The whole project is almost fully ~vibe coded~™ so use at your own risk.

## License
MIT
