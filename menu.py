"""Café menu data and helpers."""

MAX_MENU_SIZE = 6

COFFEE_ITEMS = [
    {
        "name": "Drip Coffee",
        "category": "coffee",
        "price": 3.50,
        "description": "Classic house-brewed drip coffee.",
    },
    {
        "name": "Cold Brew",
        "category": "coffee",
        "price": 5.00,
        "description": "Slow-steeped for 12 hours, served over ice.",
    },
]

TEA_ITEMS = [
    {
        "name": "Green Tea",
        "category": "tea",
        "price": 2.75,
        "description": "Steamed organic green tea.",
    },
]

OTHER_ITEMS = []

MENU_ITEMS = COFFEE_ITEMS + TEA_ITEMS + OTHER_ITEMS


def get_menu():
    """Return the full menu sorted by category then name."""
    return sorted(MENU_ITEMS, key=lambda item: (item["category"], item["name"]))


def get_categories():
    """Return unique categories from the menu."""
    return sorted({item["category"] for item in MENU_ITEMS})
