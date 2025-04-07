from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from schemas.response import Response
from services.traffic import TrafficService
from fastapi.responses import JSONResponse
router = APIRouter()
traffic_service = TrafficService()

@router.get("/traffic/{fid}", response_model=Response)
def get_mobility_data_within_buffer(
    fid: int,
    radius: str = Query(..., regex="^(500|1000|5)$", description="Radius in meters (500, 1000) or front of store (5)"),
    db: Session = Depends(get_db)
):
    try:
        # Clean the radius parameter by removing any quotes or extra characters
        clean_radius = radius.strip('"\'')
        
        # Validate the cleaned radius
        if clean_radius not in ["500", "1000", "5"]:
            raise HTTPException(
                status_code=422, 
                detail=f"Invalid radius value: {radius}. Must be one of: 500, 1000, 5"
            )
        print("just before the response")  
        result = traffic_service.get_mobility_data_within_buffer(fid, clean_radius, db)
        # response_data = Response.success(data={"response": result})
        return JSONResponse(content={"response": result}, status_code=200)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 