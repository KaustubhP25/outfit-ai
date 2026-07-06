from config import SCORING_WEIGHTS
from rules.color_rules import score_outfit_colors
from rules.skin_tone_rules import score_skin_tone, get_skin_tone_note
from rules.occasion_rules import score_occasion, get_occasion_note
from rules.silhouette_rules import score_silhouette, get_silhouette_note
from core.types import OutfitScores

def score_outfit(
    top_category: str,
    top_color: str,
    top_fit: str,
    bottom_category: str,
    bottom_color: str,
    bottom_fit: str,
    shoe_category: str,
    shoe_color: str,
    occasion: str,
    skin_tone: str,
    layer_category: str = None,
    layer_color: str = None,
) -> tuple[OutfitScores, str, str, str, str]:

    # Individual scores
    color_score = score_outfit_colors(top_color, bottom_color, shoe_color)
    skin_score = score_skin_tone(skin_tone, top_color, bottom_color)
    occasion_score = score_occasion(occasion, top_color, bottom_color, shoe_color)
    silhouette_score = score_silhouette(top_fit, bottom_fit, layer_category, top_fit)

    # Popularity is baked into color score already
    popularity_score = color_score * 0.8

    # Weighted total
    total = (
        color_score / 10 * SCORING_WEIGHTS['color_harmony'] +
        skin_score       * SCORING_WEIGHTS['skin_tone'] +
        occasion_score   * SCORING_WEIGHTS['occasion'] +
        popularity_score / 10 * SCORING_WEIGHTS['popularity']
    ) * 10

    # Apply silhouette multiplier
    total = total * (0.7 + silhouette_score * 0.3)
    total = round(min(10.0, max(1.0, total)), 1)

    scores = OutfitScores(
        color_harmony=round(color_score, 1),
        skin_tone=round(skin_score * 10, 1),
        occasion=round(occasion_score * 10, 1),
        popularity=round(popularity_score, 1),
        silhouette=round(silhouette_score * 10, 1),
        total=total,
    )

    # Notes
    color_note = build_color_note(top_color, bottom_color, shoe_color, layer_color, layer_category)
    skin_note = get_skin_tone_note(skin_tone, top_color)
    occasion_note = get_occasion_note(occasion, top_color, bottom_color)
    silhouette_note = get_silhouette_note(top_fit, bottom_fit, layer_category)

    return scores, color_note, skin_note, occasion_note, silhouette_note

def build_color_note(
    top_color: str,
    bottom_color: str,
    shoe_color: str,
    layer_color: str = None,
    layer_category: str = None,
) -> str:
    neutral = ['white', 'black', 'grey', 'beige']

    if top_color in neutral and bottom_color not in neutral:
        base = f'The neutral {top_color} top lets the {bottom_color} bottom stand out.'
    elif bottom_color in neutral and top_color not in neutral:
        base = f'The {top_color} top pops against the neutral {bottom_color} bottom.'
    elif top_color == bottom_color:
        base = f'The monochrome {top_color} look is clean and intentional.'
    else:
        base = f'The {top_color} and {bottom_color} complement each other well.'

    if shoe_color in neutral:
        shoe_note = f'The {shoe_color} footwear anchors the outfit cleanly.'
    else:
        shoe_note = f'The {shoe_color} footwear adds a distinctive finishing touch.'

    if layer_color and layer_category:
        layer_note = f'The {layer_color} {layer_category} adds depth and dimension to the look.'
        return f'{base} {layer_note} {shoe_note}'

    return f'{base} {shoe_note}'