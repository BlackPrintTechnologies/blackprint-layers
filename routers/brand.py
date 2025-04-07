from fastapi import APIRouter, Depends, HTTPException, Query
# from sqlalchemy.orm import Session
# from database import get_db
# from schemas.response import Response
# from services.brand import BrandService

# router = APIRouter()
# brand_service = BrandService()

# @router.get("/brands/{fid}", response_model=Response)
# def get_brands(
#     fid: int,
#     radius: str = Query(..., regex="^(500|1000|5)$", description="Radius in meters (500, 1000) or front of store (5)"),
#     db: Session = Depends(get_db)
# ):
#     try:
#         # Clean the radius parameter by removing any quotes or extra characters
#         clean_radius = radius.strip('"\'')
        
#         # Validate the cleaned radius
#         if clean_radius not in ["500", "1000", "5"]:
#             raise HTTPException(
#                 status_code=422, 
#                 detail=f"Invalid radius value: {radius}. Must be one of: 500, 1000, 5"
#             )
            
#         result = brand_service.get_brands(clean_radius, fid, db)
#         return Response.success(data={"response": result})
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @router.get("/brands/search", response_model=Response)
# def search_brands(
#     brand_name: str,
#     db: Session = Depends(get_db)
# ):
#     try:
#         result = brand_service.search_brands(brand_name, db)
#         return Response.success(data=result)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e)) 


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.response import Response
from services.brand import BrandService
from fastapi.responses import JSONResponse

router = APIRouter()
brand_service = BrandService()

@router.get("/brands/search", response_model=Response)
def search_brands(
    brand_name: str,
    db: Session = Depends(get_db)
):
    try:
        result = brand_service.search_brands(brand_name, db)
        return JSONResponse(content={"data": result}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
    
    


# @router.get("/brands/{fid}", response_model=Response)
# def get_brands(
#     fid: int,
#     db: Session = Depends(get_db)
# ):
#     try:
#         result = brand_service.get_brands(fid, db)
#         return Response.success(data={"response": result})
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

#####################################################################################
@router.get("/brands/{fid}", response_model=Response)
def get_brands(
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
            
        result = brand_service.get_brands(clean_radius, fid, db)
        return Response.success(data={"response": result})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))