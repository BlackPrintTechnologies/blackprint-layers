from sqlalchemy.orm import Session
from sqlalchemy import text
import logging

# Configure logging
logger = logging.getLogger(__name__)

class PropertyLayerService:
    def get_properties_layer_data(self, db: Session):
        logger.info("Getting property layer data")
        
        try:
            query = text('''
                SELECT   
                    fid,
                    centroid,
                    street_address,
                    is_on_market,
                    total_surface_area,
                    total_construction_area,
                    property_type_inmuebles24,
                    year_built,
                    special_facilities,
                    unit_land_value,
                    land_value,
                    key_vus,
                    predominant_level,
                    total_houses,
                    locality_size,
                    floor_levels,
                    open_space,
                    id_land_use,
                    id_municipality,
                    id_city_blocks
                FROM blackprint_db_prd.data_product.v_parcel_v3
                WHERE 
                    (is_on_market != 'Off Market')
                    AND (
                        property_type_spot2 IN ('Local Comercial')
                        OR property_type_inmuebles24 IN (
                            'Local comercial',
                            'Local en centro comercial',
                            'Terreno comercial'
                        )
                    )
            ''')
            
            result = db.execute(query)
            rows = result.fetchall()
            properties = [dict(row) for row in rows]
            
            logger.info(f"Successfully retrieved {len(properties)} properties")
            return properties
        except Exception as e:
            logger.error(f"Error retrieving properties: {str(e)}")
            raise 