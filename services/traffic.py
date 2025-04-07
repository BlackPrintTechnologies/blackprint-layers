from sqlalchemy.orm import Session
from sqlalchemy import text
import logging

# Configure logging
logger = logging.getLogger(__name__)

class TrafficService:
    def get_mobility_data_within_buffer(self, fid: int, radius: str, db: Session):
        logger.info(f"Getting mobility data for fid={fid}, radius={radius}")
        
        # Handle the case where radius is None or empty
        if not radius:
            radius = '500'  # Default to 500m radius
            
        query_map = {
            '500': f'''
                SELECT *
                FROM blackprint_db_prd.presentation.dataset_mobility_data_h3 
                WHERE fid = {fid} AND type = 'CIRCLE_500_METERS'
            ''',
            '1000': f'''
                SELECT *
                FROM blackprint_db_prd.presentation.dataset_mobility_data_h3 
                WHERE fid = {fid} AND type = 'CIRCLE_1000_METERS'
            ''',
            '5': f'''
                SELECT *
                FROM blackprint_db_prd.presentation.dataset_mobility_data_h3 
                WHERE fid = {fid} AND type = 'FRONT_OF_STORE'
            '''
        }
        
        try:
            query = text(query_map.get(radius))
            logger.debug(f"Executing query: {query}")
            result = db.execute(query)
            rows = result.fetchall()
            traffic_data = [dict(row) for row in rows]
            # print("Traffic Data",traffic_data)
            logger.info(f"Successfully retrieved {len(traffic_data)} traffic records for fid={fid}, radius={radius}")
            return traffic_data
        except Exception as e:
            logger.error(f"Error retrieving traffic data: {str(e)}",exc_info=True)
            raise 