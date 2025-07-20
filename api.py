from fastapi import FastAPI, Query, HTTPException, Depends, Request
from fastapi.security.api_key import APIKeyHeader
from typing import List, Optional
import pandas as pd
from datetime import timedelta
import os
from data import get_filtered_images
from lightroom import FIELD_NAMES_LIST, LightroomDB
from config import LR_CATALOG_FILE
from fastapi.responses import StreamingResponse
import io

API_KEY = os.environ.get("API_KEY", "changeme")
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

app = FastAPI()

def verify_api_key(request: Request, api_key_header: str = Depends(api_key_header)):
    api_key_query = request.query_params.get("api_key")
    api_key = api_key_header or api_key_query
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Could not validate API KEY")

@app.get("/by_year_month")
def by_year_month(
    days_back: Optional[int] = Query(None, description="Number of days to look back (default: all)"),
    property: str = Query("lensName", description="The property to group by", enum=[f for f in FIELD_NAMES_LIST if f != "captureTime"]),
    picks_only: bool = Query(False, description="Count only picks (flagged)"),
    catalog_path: str = Query(LR_CATALOG_FILE, description="Path to Lightroom catalog file"),
    api_key: str = Depends(verify_api_key)
):
    # Load images
    with LightroomDB(catalog_path) as lightroom_db:
        results = lightroom_db.get_all_images(picks_only=picks_only)
        selected_data = [{key: item[key] for key in FIELD_NAMES_LIST} for item in results]
        data = pd.DataFrame(selected_data)
        if data.empty:
            return []
        data["captureTime"] = pd.to_datetime(data["captureTime"], format="mixed")
        if days_back:
            start_date = data["captureTime"].max() - timedelta(days=days_back)
            data = data[data["captureTime"] > start_date]
        # Exclude iPhone camera usage
        data = data[~data["cameraName"].str.contains("iPhone", case=False, na=False)]
        # Group by Year-Month and property
        new_data = pd.DataFrame({
            "Year-Month": "01." + data["captureTime"].dt.strftime("%m.%Y"),
            property: data[property]
        })
        count_data = new_data.groupby(["Year-Month", property]).size().reset_index(name="count")
        # Return as list of dicts
        return [
            {"Year-Month": row["Year-Month"], property: row[property], "count": int(row["count"])}
            for _, row in count_data.iterrows()
        ]

@app.get("/by_year_month_csv")
def by_year_month_csv(
    days_back: Optional[int] = Query(None, description="Number of days to look back (default: all)"),
    property: str = Query("lensName", description="The property to group by", enum=[f for f in FIELD_NAMES_LIST if f != "captureTime"]),
    picks_only: bool = Query(False, description="Count only picks (flagged)"),
    catalog_path: str = Query(LR_CATALOG_FILE, description="Path to Lightroom catalog file"),
    api_key: str = Depends(verify_api_key)
):
    with LightroomDB(catalog_path) as lightroom_db:
        results = lightroom_db.get_all_images(picks_only=picks_only)
        selected_data = [{key: item[key] for key in FIELD_NAMES_LIST} for item in results]
        data = pd.DataFrame(selected_data)
        if data.empty:
            output = io.StringIO()
            output.write('Year-Month,{}\n'.format(property))
            output.seek(0)
            return StreamingResponse(output, media_type="text/csv")
        data["captureTime"] = pd.to_datetime(data["captureTime"], format="mixed")
        if days_back:
            start_date = data["captureTime"].max() - timedelta(days=days_back)
            data = data[data["captureTime"] > start_date]
        data = data[~data["cameraName"].str.contains("iPhone", case=False, na=False)]
        new_data = pd.DataFrame({
            "Year-Month": "01." + data["captureTime"].dt.strftime("%m.%Y"),
            property: data[property]
        })
        count_data = new_data.groupby(["Year-Month", property]).size().reset_index(name="Count")
        output = io.StringIO()
        count_data.to_csv(output, index=False)
        output.seek(0)
        return StreamingResponse(output, media_type="text/csv")
