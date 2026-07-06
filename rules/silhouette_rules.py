from config import SILHOUETTE_ENABLED

# Valid layer combinations
VALID_LAYERS = {
    'tshirt': ['overshirt', 'jacket'],
    'shirt':  ['jacket'],
    'polo':   ['jacket'],
}

# Invalid layer combinations
INVALID_LAYERS = {
    'hoodie': ['jacket'],  # too bulky
}

# Silhouette compatibility
# (top_fit, bottom_fit) -> score
SILHOUETTE_SCORES = {
    ('regular', 'regular'): 1.0,
    ('regular', 'baggy'):   0.9,
    ('baggy',   'regular'): 0.9,
    ('baggy',   'baggy'):   0.3,  # too much volume
}

# Layer + fit compatibility
LAYER_FIT_SCORES = {
    ('regular', 'jacket'):    1.0,
    ('regular', 'overshirt'): 1.0,
    ('baggy',   'jacket'):    0.3,  # jacket won't fit over baggy
    ('baggy',   'overshirt'): 0.7,
}

def can_layer(base_category: str, layer_category: str) -> bool:
    if not SILHOUETTE_ENABLED:
        return True
    valid = VALID_LAYERS.get(base_category.lower(), [])
    invalid = INVALID_LAYERS.get(base_category.lower(), [])
    return layer_category.lower() in valid and layer_category.lower() not in invalid

def score_silhouette(top_fit: str, bottom_fit: str, layer_category: str = None, base_fit: str = None) -> float:
    if not SILHOUETTE_ENABLED:
        return 1.0

    base_score = SILHOUETTE_SCORES.get(
        (top_fit.lower(), bottom_fit.lower()), 0.7
    )

    if layer_category and base_fit:
        layer_score = LAYER_FIT_SCORES.get(
            (base_fit.lower(), layer_category.lower()), 0.7
        )
        return round((base_score * 0.6) + (layer_score * 0.4), 2)

    return round(base_score, 2)

def get_silhouette_note(top_fit: str, bottom_fit: str, layer_category: str = None) -> str:
    if top_fit == 'baggy' and bottom_fit == 'baggy':
        return 'Both pieces are oversized — consider slim bottoms to balance the silhouette.'
    elif top_fit == 'baggy' and bottom_fit == 'regular':
        return 'Baggy top with regular fit bottom creates a balanced relaxed silhouette.'
    elif layer_category == 'jacket' and top_fit == 'baggy':
        return 'A jacket over a baggy top may not fit well — consider a regular fit base.'
    elif layer_category:
        return f'The {layer_category} layers well over your base top.'
    else:
        return 'Clean silhouette with good proportions.'

def get_valid_layers(base_category: str) -> list[str]:
    return VALID_LAYERS.get(base_category.lower(), [])