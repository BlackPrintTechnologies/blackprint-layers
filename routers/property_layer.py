from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.response import Response
from services.property_layer import PropertyLayerService
from fastapi.responses import JSONResponse

router = APIRouter()
property_layer_service = PropertyLayerService()

@router.get("/properties", response_model=Response)
def get_properties_layer_data(db: Session = Depends(get_db)):
    try:
        result = property_layer_service.get_properties_layer_data(db)
        return JSONResponse(content={"data": result}, status_code=200)
        return Response.success(data={"response": result})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 