# Seasonal color analysis system
# Based on undertone (warm/cool) + depth (light/deep)

SEASONAL_TYPES = ['spring', 'summer', 'autumn', 'winter']

SKIN_TONE_RULES = {
    'spring': {
        'description': 'Warm + Light — golden, peachy undertones',
        'great': ['peach', 'coral', 'camel', 'warm red', 'olive', 'golden yellow', 'warm brown', 'ivory', 'turquoise', 'orange'],
        'good': ['white', 'beige', 'navy', 'teal', 'green', 'brown'],
        'avoid': ['black', 'grey', 'burgundy', 'cool pink', 'lavender', 'stark white'],
    },
    'summer': {
        'description': 'Cool + Light — pink, blue undertones',
        'great': ['lavender', 'soft pink', 'powder blue', 'navy', 'rose', 'mauve', 'cool grey', 'white', 'teal', 'blue'],
        'good': ['black', 'burgundy', 'purple', 'green', 'beige'],
        'avoid': ['orange', 'warm brown', 'gold', 'yellow', 'rust', 'camel'],
    },
    'autumn': {
        'description': 'Warm + Deep — golden, orange undertones',
        'great': ['rust', 'olive', 'burnt orange', 'camel', 'brown', 'forest green', 'maroon', 'mustard', 'beige', 'dark green'],
        'good': ['white', 'navy', 'teal', 'red', 'grey'],
        'avoid': ['black', 'pink', 'cool grey', 'bright white', 'lavender', 'royal blue'],
    },
    'winter': {
        'description': 'Cool + Deep — blue, pink undertones',
        'great': ['black', 'white', 'navy', 'royal blue', 'burgundy', 'emerald', 'hot pink', 'red', 'grey', 'purple'],
        'good': ['teal', 'dark green', 'maroon', 'dark grey', 'blue'],
        'avoid': ['orange', 'beige', 'camel', 'warm brown', 'gold', 'mustard', 'olive'],
    },
}

def score_skin_tone(season: str, top_color: str, bottom_color: str) -> float:
    season = season.lower()
    if season not in SKIN_TONE_RULES:
        return 0.7

    rules = SKIN_TONE_RULES[season]
    top_color = top_color.lower()
    bottom_color = bottom_color.lower()

    def color_score(color):
        if color in rules['great']:
            return 1.0
        elif color in rules['good']:
            return 0.7
        elif color in rules['avoid']:
            return 0.3
        else:
            return 0.6

    top_score = color_score(top_color)
    bottom_score = color_score(bottom_color)

    # Top matters more — closer to face
    return round((top_score * 0.7) + (bottom_score * 0.3), 2)

def get_skin_tone_note(season: str, top_color: str) -> str:
    season = season.lower()
    if season not in SKIN_TONE_RULES:
        return ''

    rules = SKIN_TONE_RULES[season]
    top_color = top_color.lower()
    desc = SKIN_TONE_RULES[season]['description']

    if top_color in rules['great']:
        return f'{top_color.capitalize()} is a perfect match for {season} tones ({desc}). It enhances your natural complexion.'
    elif top_color in rules['good']:
        return f'{top_color.capitalize()} works well with {season} tones ({desc}).'
    elif top_color in rules['avoid']:
        return f'{top_color.capitalize()} can clash with {season} tones — consider a warmer or cooler alternative.'
    else:
        return f'This works for {season} tones ({desc}).'

def get_season_description(season: str) -> str:
    return SKIN_TONE_RULES.get(season, {}).get('description', '')