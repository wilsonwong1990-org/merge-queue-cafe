"""Café menu data and helpers."""

MAX_MENU_SIZE = 4

COFFEE_ITEMS = [
    {
        "name": "Drip Coffee",
        "category": "coffee",
        "price": 3.50,
        "description": "Classic house-brewed drip coffee.",
    },
    {
        "name": "Espresso",
        "category": "coffee",
        "price": 4.00,
        "description": "A bold, concentrated shot of pure coffee.",
    },
    # slot:espresso
    # slot:latte
    # slot:cappuccino
    # slot:americano
    # slot:cold-brew
]

TEA_ITEMS = [
    {
        "name": "Green Tea",
        "category": "tea",
        "price": 2.75,
        "description": "Steamed organic green tea.",
    },
    # slot:matcha-latte
    # slot:chai-latte
]

OTHER_ITEMS = [
    # slot:hot-chocolate
]

MENU_ITEMS = COFFEE_ITEMS + TEA_ITEMS + OTHER_ITEMS

if len(MENU_ITEMS) > MAX_MENU_SIZE:
    raise RuntimeError(
        f"FATAL: Menu has {len(MENU_ITEMS)} items but the kitchen can only handle "
        f"{MAX_MENU_SIZE}! The app cannot start. Remove items or increase MAX_MENU_SIZE."
    )


def get_menu():
    """Return the full menu sorted by category then name."""
    return sorted(MENU_ITEMS, key=lambda item: (item["category"], item["name"]))


def get_categories():
    """Return unique categories from the menu."""
    return sorted({item["category"] for item in MENU_ITEMS})
