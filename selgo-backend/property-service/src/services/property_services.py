from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, desc, asc
from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime, timedelta
from ..repositories.repositories import PropertyCategoryRepository, PropertyRepository
from ..models.models import PropertyCategory, Property, PropertyFavorite, PropertyView, PropertyMessage
from ..models.property_schemas import PropertyCategoryCreate, PropertyCreate, PropertyUpdate, PropertyFilterParams

class PropertyCategoryService:
    @staticmethod
    def create_category(db: Session, category_data: PropertyCategoryCreate) -> PropertyCategory:
        return PropertyCategoryRepository.create(db, category_data.dict())
    
    @staticmethod
    def get_category_by_id(db: Session, category_id: int) -> Optional[PropertyCategory]:
        return PropertyCategoryRepository.get_by_id(db, category_id)
    
    @staticmethod
    def get_all_categories(db: Session, skip: int = 0, limit: int = 100) -> List[PropertyCategory]:
        return PropertyCategoryRepository.get_all(db, skip, limit)
    
    @staticmethod
    def update_category(db: Session, category_id: int, category_data: PropertyCategoryCreate) -> Optional[PropertyCategory]:
        return PropertyCategoryRepository.update(db, category_id, category_data.dict())
    
    @staticmethod
    def delete_category(db: Session, category_id: int) -> bool:
        return PropertyCategoryRepository.delete(db, category_id)

class PropertyService:
    @staticmethod
    def create_property(db: Session, property_data: PropertyCreate, user_id: str) -> Property:
        property_dict = property_data.dict()
        property_dict['owner_id'] = user_id
        return PropertyRepository.create(db, property_dict)
    
    @staticmethod
    def get_property_by_id(db: Session, property_id: str, increment_view: bool = False) -> Optional[Property]:
        prop = PropertyRepository.get_by_id(db, property_id)
        if prop and increment_view:
            return PropertyRepository.increment_view_count(db, property_id)
        return prop
    
    @staticmethod
    def get_all_properties(db: Session, skip: int = 0, limit: int = 100) -> List[Property]:
        return PropertyRepository.get_all(db, skip, limit)
    
    @staticmethod
    def filter_properties(db: Session, filters: PropertyFilterParams) -> Tuple[List[Property], int]:
        return PropertyRepository.filter_properties(db, filters)

    @staticmethod
    def update_property(db: Session, property_id: str, property_data: PropertyUpdate, user_id: str) -> Optional[Property]:
        prop = PropertyRepository.get_by_id(db, property_id)
        if not prop or str(prop.owner_id) != user_id:
            return None
        
        property_dict = property_data.dict(exclude_unset=True)
        return PropertyRepository.update(db, property_id, property_dict)
    
    @staticmethod
    def delete_property(db: Session, property_id: str, user_id: str) -> bool:
        prop = PropertyRepository.get_by_id(db, property_id)
        if not prop or str(prop.owner_id) != user_id:
            return False
        
        return PropertyRepository.delete(db, property_id)
    
    # Finn.no-like enhanced features
    
    @staticmethod
    def get_similar_properties(db: Session, property_id: str, limit: int = 6) -> List[Property]:
        """Get similar properties based on location, price, and type."""
        base_property = PropertyRepository.get_by_id(db, property_id)
        if not base_property:
            return []
        
        # Calculate price range (±20%)
        price_min = float(base_property.price) * 0.8
        price_max = float(base_property.price) * 1.2
        
        query = db.query(Property).filter(
            Property.id != property_id,
            Property.status == "active",
            Property.property_type == base_property.property_type,
            Property.price.between(price_min, price_max)
        )
        
        # Prefer same city
        if base_property.city:
            query = query.filter(Property.city == base_property.city)
        
        return query.limit(limit).all()
    
    @staticmethod
    def toggle_favorite(db: Session, property_id: str, user_id: str) -> bool:
        """Add or remove property from user's favorites."""
        existing = db.query(PropertyFavorite).filter(
            PropertyFavorite.property_id == property_id,
            PropertyFavorite.user_id == user_id
        ).first()
        
        if existing:
            db.delete(existing)
            db.commit()
            return False
        else:
            favorite = PropertyFavorite(property_id=property_id, user_id=user_id)
            db.add(favorite)
            db.commit()
            return True
    
    @staticmethod
    def get_price_history(db: Session, property_id: str) -> List[Dict]:
        """Get price history for a property (placeholder - would need price history table)."""
        # This would require a PropertyPriceHistory table in a real implementation
        property_obj = PropertyRepository.get_by_id(db, property_id)
        if not property_obj:
            return []
        
        # Return current price as single entry for now
        return [{
            "date": property_obj.created_at.isoformat(),
            "price": float(property_obj.price),
            "change_type": "initial"
        }]
    
    @staticmethod
    def advanced_search(db: Session, search_params: Dict[str, Any]) -> Tuple[List[Property], int]:
        """Advanced property search with multiple filters."""
        query = db.query(Property).filter(Property.status == "active")
        
        # Location filters
        if search_params.get("city"):
            query = query.filter(Property.city.ilike(f"%{search_params['city']}%"))
        
        if search_params.get("postal_code"):
            query = query.filter(Property.postal_code == search_params["postal_code"])
        
        # Property type filters
        if search_params.get("property_type"):
            query = query.filter(Property.property_type == search_params["property_type"])
        
        if search_params.get("property_category"):
            query = query.filter(Property.property_category == search_params["property_category"])
        
        if search_params.get("housing_type"):
            query = query.filter(Property.housing_type.ilike(f"%{search_params['housing_type']}%"))
        
        # Size filters
        if search_params.get("min_bedrooms"):
            query = query.filter(Property.bedrooms >= search_params["min_bedrooms"])
        
        if search_params.get("max_bedrooms"):
            query = query.filter(Property.bedrooms <= search_params["max_bedrooms"])
        
        if search_params.get("min_bathrooms"):
            query = query.filter(Property.bathrooms >= search_params["min_bathrooms"])
        
        if search_params.get("max_bathrooms"):
            query = query.filter(Property.bathrooms <= search_params["max_bathrooms"])
        
        if search_params.get("min_area"):
            query = query.filter(Property.use_area >= search_params["min_area"])
        
        if search_params.get("max_area"):
            query = query.filter(Property.use_area <= search_params["max_area"])
        
        # Price filters
        if search_params.get("min_price"):
            query = query.filter(Property.price >= search_params["min_price"])
        
        if search_params.get("max_price"):
            query = query.filter(Property.price <= search_params["max_price"])
        
        # Feature filters
        if search_params.get("has_balcony") is not None:
            query = query.filter(Property.has_balcony == search_params["has_balcony"])
        
        if search_params.get("has_terrace") is not None:
            query = query.filter(Property.has_terrace == search_params["has_terrace"])
        
        if search_params.get("has_parking") is not None:
            query = query.filter(Property.has_parking == search_params["has_parking"])
        
        if search_params.get("has_garden") is not None:
            query = query.filter(Property.has_garden == search_params["has_garden"])
        
        if search_params.get("is_furnished") is not None:
            query = query.filter(Property.is_furnished == search_params["is_furnished"])
        
        # Year built filters
        if search_params.get("year_built_from"):
            query = query.filter(Property.year_built >= search_params["year_built_from"])
        
        if search_params.get("year_built_to"):
            query = query.filter(Property.year_built <= search_params["year_built_to"])
        
        # Energy rating filter
        if search_params.get("energy_rating"):
            query = query.filter(Property.energy_rating == search_params["energy_rating"])
        
        # Get total count before pagination
        total = query.count()
        
        # Sorting
        sort_by = search_params.get("sort_by", "created_at")
        sort_order = search_params.get("sort_order", "desc")
        
        if sort_by == "price":
            order_col = Property.price
        elif sort_by == "area":
            order_col = Property.use_area
        elif sort_by == "bedrooms":
            order_col = Property.bedrooms
        elif sort_by == "updated_at":
            order_col = Property.updated_at
        else:
            order_col = Property.created_at
        
        if sort_order == "asc":
            query = query.order_by(asc(order_col))
        else:
            query = query.order_by(desc(order_col))
        
        # Pagination
        page = search_params.get("page", 1)
        limit = search_params.get("limit", 20)
        offset = (page - 1) * limit
        
        properties = query.offset(offset).limit(limit).all()
        
        return properties, total
    
    @staticmethod
    def get_market_statistics(db: Session, city: Optional[str] = None, property_type: Optional[str] = None) -> Dict[str, Any]:
        """Get market statistics for properties."""
        query = db.query(Property).filter(Property.status == "active")
        
        if city:
            query = query.filter(Property.city.ilike(f"%{city}%"))
        
        if property_type:
            query = query.filter(Property.property_type == property_type)
        
        # Basic statistics
        total_properties = query.count()
        
        if total_properties == 0:
            return {
                "total_properties": 0,
                "average_price": 0,
                "median_price": 0,
                "min_price": 0,
                "max_price": 0,
                "average_area": 0
            }
        
        # Price statistics
        price_stats = query.with_entities(
            func.avg(Property.price).label('avg_price'),
            func.min(Property.price).label('min_price'),
            func.max(Property.price).label('max_price')
        ).first()
        
        # Area statistics
        area_stats = query.filter(Property.use_area.isnot(None)).with_entities(
            func.avg(Property.use_area).label('avg_area')
        ).first()
        
        return {
            "total_properties": total_properties,
            "average_price": float(price_stats.avg_price) if price_stats.avg_price else 0,
            "min_price": float(price_stats.min_price) if price_stats.min_price else 0,
            "max_price": float(price_stats.max_price) if price_stats.max_price else 0,
            "average_area": float(area_stats.avg_area) if area_stats.avg_area else 0
        }
    
    @staticmethod
    def get_price_trends(db: Session, city: Optional[str] = None, months: int = 12) -> List[Dict]:
        """Get price trends over time."""
        # This would require historical data - returning placeholder for now
        end_date = datetime.now()
        start_date = end_date - timedelta(days=months * 30)
        
        # In a real implementation, this would query historical price data
        # For now, return sample trend data
        trends = []
        for i in range(months):
            month_date = start_date + timedelta(days=i * 30)
            trends.append({
                "month": month_date.strftime("%Y-%m"),
                "average_price": 5000000 + (i * 50000),  # Sample increasing trend
                "property_count": 100 + (i * 5)
            })
        
        return trends
    
    @staticmethod
    def send_contact_message(db: Session, property_id: str, contact_data: Dict[str, Any]) -> bool:
        """Send message to property owner."""
        property_obj = PropertyRepository.get_by_id(db, property_id)
        if not property_obj:
            return False
        
        message = PropertyMessage(
            property_id=property_id,
            sender_name=contact_data.get("name", ""),
            sender_email=contact_data.get("email", ""),
            sender_phone=contact_data.get("phone", ""),
            message=contact_data.get("message", "")
        )
        
        db.add(message)
        db.commit()
        return True
    
    @staticmethod
    def get_featured_properties(db: Session, limit: int = 10) -> List[Property]:
        """Get featured properties."""
        return db.query(Property).filter(
            Property.status == "active",
            Property.is_featured == True
        ).order_by(desc(Property.featured_until)).limit(limit).all()
    
    @staticmethod
    def get_recent_properties(db: Session, limit: int = 10) -> List[Property]:
        """Get recently added properties."""
        return db.query(Property).filter(
            Property.status == "active"
        ).order_by(desc(Property.created_at)).limit(limit).all()
    
    @staticmethod
    def get_popular_properties(db: Session, limit: int = 10) -> List[Property]:
        """Get most viewed properties."""
        return db.query(Property).filter(
            Property.status == "active"
        ).order_by(desc(Property.views_count)).limit(limit).all()
    
    @staticmethod
    def get_properties_in_bounds(db: Session, north: float, south: float, east: float, west: float, limit: int = 100) -> List[Dict]:
        """Get properties within map bounds."""
        # This would use PostGIS functions in a real implementation
        # For now, return basic property data for map markers
        properties = db.query(Property).filter(
            Property.status == "active"
        ).limit(limit).all()
        
        return [{
            "id": str(prop.id),
            "title": prop.title,
            "price": float(prop.price),
            "latitude": 59.9139,  # Oslo coordinates as placeholder
            "longitude": 10.7522,
            "property_type": prop.property_type
        } for prop in properties]
    
    @staticmethod
    def report_property(db: Session, property_id: str, report_data: Dict[str, Any], user_id: Optional[str] = None) -> bool:
        """Report a property for inappropriate content."""
        property_obj = PropertyRepository.get_by_id(db, property_id)
        if not property_obj:
            return False
        
        # In a real implementation, this would create a PropertyReport record
        # For now, just log the report
        print(f"Property {property_id} reported by user {user_id}: {report_data}")
        return True
    
    @staticmethod
    def get_properties_by_user(db: Session, user_id: str, status: Optional[str] = None, limit: int = 20, offset: int = 0) -> List[Property]:
        """Get properties by user ID."""
        query = db.query(Property).filter(Property.owner_id == user_id)
        
        if status:
            query = query.filter(Property.status == status)
        
        return query.order_by(desc(Property.created_at)).offset(offset).limit(limit).all()