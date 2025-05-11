from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from schemas.response import Response
from services.brand import BrandService
from fastapi.responses import ORJSONResponse
from starlette.concurrency import run_in_threadpool

router = APIRouter()
brand_service = BrandService()

@router.get("/brands/search", response_model=Response)
async def search_brands(
    brand_name: str,
    db: Session = Depends(get_db)
):
    try:
        result = await run_in_threadpool(brand_service.search_brands, brand_name, db)
        return ORJSONResponse(content={"data": result}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/brands/{fid}", response_model=Response)
async def get_brands(
    fid: int,
    radius: str = Query(..., regex="^(500|1000|5)$", description="Radius in meters (500, 1000) or front of store (5)"),
    db: Session = Depends(get_db)
):
    try:
        clean_radius = radius.strip('"\'')
        if clean_radius not in ["500", "1000", "5"]:
            raise HTTPException(
                status_code=422, 
                detail=f"Invalid radius value: {radius}. Must be one of: 500, 1000, 5"
            )
        result = await run_in_threadpool(brand_service.get_brands, clean_radius, fid, db)
        return ORJSONResponse(content={"response": result}, status_code=200)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))