# Color families
COLOR_FAMILIES = {
    'neutral': ['white', 'black', 'grey', 'beige', 'cream'],
    'dark': ['navy', 'black', 'dark grey', 'charcoal', 'maroon', 'dark green'],
    'earth': ['brown', 'tan', 'camel', 'olive', 'beige', 'rust'],
    'warm': ['red', 'orange', 'yellow', 'maroon', 'rust', 'coral'],
    'cool': ['blue', 'navy', 'teal', 'purple', 'grey'],
    'bright': ['yellow', 'orange', 'red', 'pink', 'coral', 'lime'],
    'pastel': ['light blue', 'lavender', 'mint', 'blush', 'cream'],
}

# Which families work together
FAMILY_HARMONY = {
    'neutral': ['neutral', 'warm', 'cool', 'earth', 'bright', 'pastel', 'dark'],
    'dark':    ['neutral', 'dark', 'earth', 'warm'],
    'earth':   ['neutral', 'earth', 'dark', 'warm'],
    'warm':    ['neutral', 'dark', 'earth'],
    'cool':    ['neutral', 'cool', 'dark'],
    'bright':  ['neutral', 'dark'],
    'pastel':  ['neutral', 'pastel', 'cool'],
}

# Specific known good pairs (color1, color2) -> score bonus
KNOWN_GOOD_PAIRS = {
    ('white', 'navy'): 10,
    ('white', 'black'): 10,
    ('white', 'grey'): 9,
    ('white', 'blue'): 9,
    ('white', 'olive'): 8,
    ('white', 'maroon'): 8,
    ('black', 'white'): 10,
    ('black', 'grey'): 9,
    ('black', 'red'): 8,
    ('black', 'beige'): 8,
    ('black', 'olive'): 8,
    ('grey', 'navy'): 9,
    ('grey', 'white'): 9,
    ('grey', 'black'): 9,
    ('navy', 'white'): 10,
    ('navy', 'beige'): 9,
    ('navy', 'grey'): 9,
    ('navy', 'brown'): 8,
    ('beige', 'white'): 9,
    ('beige', 'navy'): 9,
    ('beige', 'brown'): 9,
    ('beige', 'black'): 8,
    ('maroon', 'black'): 9,
    ('maroon', 'navy'): 8,
    ('maroon', 'beige'): 8,
    ('maroon', 'grey'): 8,
    ('olive', 'white'): 8,
    ('olive', 'black'): 8,
    ('olive', 'beige'): 9,
    ('olive', 'brown'): 9,
    ('brown', 'beige'): 9,
    ('brown', 'white'): 8,
    ('brown', 'navy'): 8,
    ('teal', 'white'): 8,
    ('teal', 'black'): 8,
    ('teal', 'navy'): 7,
}

# Popularity scores for 3-color combinations (top, bottom, shoe)
POPULARITY = {
    ('white', 'navy', 'white'): 9.5,
    ('white', 'black', 'white'): 9.2,
    ('white', 'grey', 'white'): 9.0,
    ('white', 'navy', 'black'): 9.0,
    ('black', 'black', 'white'): 8.8,
    ('grey', 'navy', 'white'): 8.5,
    ('white', 'beige', 'white'): 8.5,
    ('navy', 'beige', 'brown'): 8.5,
    ('white', 'olive', 'white'): 8.2,
    ('black', 'grey', 'white'): 8.2,
    ('maroon', 'black', 'white'): 8.5,
    ('maroon', 'navy', 'white'): 8.2,
    ('olive', 'beige', 'brown'): 8.0,
    ('beige', 'navy', 'brown'): 8.5,
    ('teal', 'black', 'white'): 7.8,
}

def get_color_family(color: str) -> str:
    color = color.lower()
    for family, colors in COLOR_FAMILIES.items():
        if color in colors:
            return family
    return 'neutral'

def score_color_pair(color1: str, color2: str) -> float:
    pair = (color1.lower(), color2.lower())
    reverse = (color2.lower(), color1.lower())

    if pair in KNOWN_GOOD_PAIRS:
        return KNOWN_GOOD_PAIRS[pair] / 10
    if reverse in KNOWN_GOOD_PAIRS:
        return KNOWN_GOOD_PAIRS[reverse] / 10

    f1 = get_color_family(color1)
    f2 = get_color_family(color2)

    if f2 in FAMILY_HARMONY.get(f1, []):
        return 0.7
    return 0.4

def score_outfit_colors(top_color: str, bottom_color: str, shoe_color: str) -> float:
    top_bottom = score_color_pair(top_color, bottom_color)
    bottom_shoe = score_color_pair(bottom_color, shoe_color)
    top_shoe = score_color_pair(top_color, shoe_color)

    harmony = (top_bottom * 0.4 + bottom_shoe * 0.35 + top_shoe * 0.25)

    combo = (top_color.lower(), bottom_color.lower(), shoe_color.lower())
    popularity = POPULARITY.get(combo, 0)
    if popularity == 0:
        reverse_lookup = [v for k, v in POPULARITY.items() if set(k) == set(combo)]
        popularity = reverse_lookup[0] if reverse_lookup else 6.0

    final = (harmony * 0.7) + (popularity / 10 * 0.3)
    return round(final * 10, 1)