import time
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from database import get_db
from schemas.response import Response
from services.property_layer import PropertyLayerService
from fastapi.responses import ORJSONResponse
from starlette.concurrency import run_in_threadpool


router = APIRouter()
property_layer_service = PropertyLayerService()

@router.get("/properties", response_class=ORJSONResponse)
async def get_properties_layer_data(request: Request):
    try:
        if not hasattr(request.app.state, "property_data_cache"):
            raise HTTPException(status_code=503, detail="Data not loaded yet")
        return ORJSONResponse(content={"data": request.app.state.property_data_cache}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
