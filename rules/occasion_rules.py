# Formality levels per category
CATEGORY_FORMALITY = {
    # Casual tops
    'tshirt': 'casual',
    'hoodie': 'casual',
    # Smart casual tops
    'shirt': 'smart_casual',
    'polo': 'smart_casual',
    'jacket': 'smart_casual',
    # Casual bottoms
    'jeans': 'casual',
    'shorts': 'casual',
    # Smart casual bottoms
    'trousers': 'smart_casual',
    'chinos': 'smart_casual',
    # Casual footwear
    'sneakers': 'casual',
    'sandals': 'casual',
    # Smart casual footwear
    'boots': 'smart_casual',
    'loafers': 'smart_casual',
    'shoes': 'smart_casual',
}

# Per occasion — how many casual vs smart casual outfits
OCCASION_SPLIT = {
    'college':   {'casual': 3, 'smart_casual': 2},
    'everyday':  {'casual': 4, 'smart_casual': 1},
    'party':     {'casual': 2, 'smart_casual': 3},
    'date':      {'casual': 1, 'smart_casual': 4},
    'work':      {'casual': 0, 'smart_casual': 5},
    'wedding':   {'casual': 0, 'smart_casual': 5},
    'festival':  {'casual': 4, 'smart_casual': 1},
}

# Allowed formality levels per occasion
OCCASION_FORMALITY = {
    'college':  ['casual', 'smart_casual'],
    'everyday': ['casual', 'smart_casual'],
    'party':    ['casual', 'smart_casual'],
    'date':     ['smart_casual'],
    'work':     ['smart_casual'],
    'wedding':  ['smart_casual'],
    'festival': ['casual', 'smart_casual'],
}

# Preferred color moods per occasion
OCCASION_COLOR_MOOD = {
    'college':  {
        'preferred': ['white', 'grey', 'navy', 'black', 'blue'],
        'bonus': ['olive', 'maroon', 'teal'],
        'avoid': ['pink', 'lavender', 'gold'],
    },
    'everyday': {
        'preferred': ['white', 'grey', 'beige', 'navy', 'black'],
        'bonus': ['olive', 'brown', 'teal'],
        'avoid': ['bright red', 'hot pink', 'neon'],
    },
    'party': {
        'preferred': ['black', 'white', 'red', 'navy'],
        'bonus': ['maroon', 'teal', 'royal blue'],
        'avoid': ['beige', 'olive', 'grey'],
    },
    'date': {
        'preferred': ['navy', 'white', 'beige', 'maroon', 'olive'],
        'bonus': ['teal', 'brown', 'camel'],
        'avoid': ['neon', 'orange', 'bright yellow'],
    },
    'work': {
        'preferred': ['navy', 'grey', 'white', 'black', 'beige'],
        'bonus': ['teal', 'maroon', 'brown'],
        'avoid': ['orange', 'yellow', 'bright red', 'pink'],
    },
    'wedding': {
        'preferred': ['navy', 'grey', 'white', 'black', 'beige'],
        'bonus': ['maroon', 'teal', 'brown'],
        'avoid': ['orange', 'yellow', 'bright red'],
    },
    'festival': {
        'preferred': ['orange', 'yellow', 'red', 'green', 'white'],
        'bonus': ['teal', 'coral', 'turquoise'],
        'avoid': ['grey', 'black', 'navy'],
    },
}

def get_formality(category: str) -> str:
    return CATEGORY_FORMALITY.get(category.lower(), 'casual')

def get_occasion_split(occasion: str) -> dict:
    return OCCASION_SPLIT.get(occasion.lower(), {'casual': 3, 'smart_casual': 2})

def get_allowed_formality(occasion: str) -> list:
    return OCCASION_FORMALITY.get(occasion.lower(), ['casual', 'smart_casual'])

def score_occasion(occasion: str, top_color: str, bottom_color: str, shoe_color: str) -> float:
    occasion = occasion.lower()
    mood = OCCASION_COLOR_MOOD.get(occasion, {})

    preferred = mood.get('preferred', [])
    bonus = mood.get('bonus', [])
    avoid = mood.get('avoid', [])

    colors = [top_color.lower(), bottom_color.lower(), shoe_color.lower()]

    score = 0.6  # base

    for color in colors:
        if color in preferred:
            score += 0.12
        elif color in bonus:
            score += 0.06
        elif color in avoid:
            score -= 0.1

    return round(min(1.0, max(0.2, score)), 2)

def get_occasion_note(occasion: str, top_color: str, bottom_color: str) -> str:
    occasion = occasion.lower()
    mood = OCCASION_COLOR_MOOD.get(occasion, {})
    preferred = mood.get('preferred', [])
    avoid = mood.get('avoid', [])

    if top_color.lower() in avoid or bottom_color.lower() in avoid:
        return f'This color combination is a bold choice for {occasion} — consider more muted tones.'
    elif top_color.lower() in preferred and bottom_color.lower() in preferred:
        return f'This is a great color combination for {occasion}.'
    else:
        return f'This outfit works for {occasion}.'