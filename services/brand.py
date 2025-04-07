from sqlalchemy.orm import Session
from sqlalchemy import text
from utils.icon_utils import IconMapper
import logging

# Configure logging
logger = logging.getLogger(__name__)

class BrandService:
    def get_brands(self, catchment: str, fid: int, db: Session):
        logger.info(f"Getting brands for fid={fid}, radius={catchment}")
        
        if not catchment:
            catchment = '500'
        
        # Ensure schema is set
        # db.execute(text("SET search_path TO blackprint_db_prd"))
        
        query_map = {
            '500': f'''
                WITH split_values AS (
                    SELECT TRIM(SPLIT_PART(blackprint_db_prd.data_product.v_parcel_v3.ids_pois_500m, ',', n))::INTEGER as value
                    FROM blackprint_db_prd.data_product.v_parcel_v3,
                    (SELECT generate_series(1, REGEXP_COUNT(blackprint_db_prd.data_product.v_parcel_v3.ids_pois_500m, ',') + 1) AS n) num_table
                    WHERE fid = {fid}
                )
                SELECT brand, geometry_wkt, category_1 FROM blackprint_db_prd.presentation.dim_places_v2
                WHERE id_place IN (SELECT value FROM split_values) AND brand IS NOT NULL
            ''',
            '1000': f'''
                WITH split_values AS (
                    SELECT TRIM(SPLIT_PART(blackprint_db_prd.data_product.v_parcel_v3.ids_pois_1km, ',', n))::INTEGER as value
                    FROM blackprint_db_prd.data_product.v_parcel_v3,
                    (SELECT generate_series(1, REGEXP_COUNT(blackprint_db_prd.data_product.v_parcel_v3.ids_pois_1km, ',') + 1) AS n) num_table
                    WHERE fid = {fid}
                )
                SELECT brand, geometry_wkt, category_1 FROM blackprint_db_prd.presentation.dim_places_v2
                WHERE id_place IN (SELECT value FROM split_values) AND brand IS NOT NULL
            ''',
            '5': f'''
                WITH split_values AS (
                    SELECT TRIM(SPLIT_PART(blackprint_db_prd.data_product.v_parcel_v3.ids_pois_front, ',', n))::INTEGER as value
                    FROM blackprint_db_prd.data_product.v_parcel_v3,
                    (SELECT generate_series(1, REGEXP_COUNT(blackprint_db_prd.data_product.v_parcel_v3.ids_pois_front, ',') + 1) AS n) num_table
                    WHERE fid = {fid}
                )
                SELECT brand, geometry_wkt, category_1 FROM blackprint_db_prd.presentation.dim_places_v2
                WHERE id_place IN (SELECT value FROM split_values) AND brand IS NOT NULL
            '''
        }
        
        try:
            query = text(query_map.get(catchment))
            result = db.execute(query)
            rows = result.fetchall()
            
            enhanced_results = []
            for row in rows:
                row_dict = dict(row)
                row_dict['icon_url'] = IconMapper.get_icon_url(row_dict['category_1'])
                enhanced_results.append(row_dict)
            
            logger.info(f"Successfully retrieved {len(enhanced_results)} brands for fid={fid}, radius={catchment}")
            return enhanced_results
        except Exception as e:
            logger.error(f"Error retrieving brands: {str(e)}")
            raise

    def search_brands(self, brand_name: str, db: Session):
        logger.info(f"Searching brands with name: {brand_name}")
        
        try:
            # db.execute(text("SET search_path TO blackprint_db_prd"))
            
            query = text('''
                SELECT DISTINCT brand 
                FROM blackprint_db_prd.presentation.dim_places_v2 
                WHERE brand ILIKE :brand_name
                LIMIT 50
            ''')
            
            result = db.execute(query, {"brand_name": f"{brand_name}%"})
            rows = result.fetchall()
            brands = [dict(row) for row in rows]
            
            logger.info(f"Successfully found {len(brands)} brands matching '{brand_name}'")
            return brands
        except Exception as e:
            logger.error(f"Error searching brands: {str(e)}")
            raise
