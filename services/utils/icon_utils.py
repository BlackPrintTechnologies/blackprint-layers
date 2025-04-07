class IconMapper:
    # Category to icon URL mapping
    CATEGORY_ICON_MAP = {
        'Restaurant': '/static/icons/restaurant.png',
        'Retail': '/static/icons/retail.png',
        'Entertainment': '/static/icons/entertainment.png',
        'Services': '/static/icons/services.png',
        'Education': '/static/icons/education.png',
        'Healthcare': '/static/icons/healthcare.png',
        'Transportation': '/static/icons/transportation.png',
        'Office': '/static/icons/office.png',
        'Other': '/static/icons/other.png'
    }

    @staticmethod
    def get_icon_url(category: str) -> str:
        """
        Get the icon URL for a given category.
        Returns a default icon if category is not found.
        """
        return IconMapper.CATEGORY_ICON_MAP.get(category, '/static/icons/other.png') 