from itertools import product
from config import MIN_DIVERSITY, MIN_SCORE_THRESHOLD, LAYERING_ENABLED
from core.types import ClothingItem, OutfitItem, LayerItem, Outfit, OutfitScores
from core.scorer import score_outfit
from rules.occasion_rules import (
    get_formality, get_allowed_formality, get_occasion_split
)
from rules.silhouette_rules import can_layer, get_valid_layers

TOP_CATEGORIES = ['tshirt', 'shirt', 'polo', 'hoodie']
LAYER_CATEGORIES = ['jacket', 'overshirt']
BOTTOM_CATEGORIES = ['jeans', 'trousers', 'chinos', 'shorts']
FOOTWEAR_CATEGORIES = ['sneakers', 'boots', 'loafers', 'sandals']

def expand_by_color(item: ClothingItem) -> list[dict]:
    return [
        {
            'id': item.id,
            'category': item.category,
            'color': color,
            'fit': item.fit,
            'pattern': item.pattern,
            'image_url': item.image_url,
            'formality': get_formality(item.category),
        }
        for color in item.colors
    ]

def is_diverse(outfit_a: dict, outfit_b: dict) -> bool:
    differences = 0
    if outfit_a['top']['color'] != outfit_b['top']['color'] or \
       outfit_a['top']['category'] != outfit_b['top']['category']:
        differences += 1
    if outfit_a['bottom']['color'] != outfit_b['bottom']['color'] or \
       outfit_a['bottom']['category'] != outfit_b['bottom']['category']:
        differences += 1
    if outfit_a['footwear']['color'] != outfit_b['footwear']['color'] or \
       outfit_a['footwear']['category'] != outfit_b['footwear']['category']:
        differences += 1
    return differences >= MIN_DIVERSITY

def filter_diverse(outfits: list) -> list:
    selected = []
    for outfit in outfits:
        diverse = all(is_diverse(outfit, s) for s in selected)
        if diverse:
            selected.append(outfit)
    return selected

def build_outfit_object(
    top: dict,
    bottom: dict,
    shoe: dict,
    occasion: str,
    skin_tone: str,
    layer: dict = None,
) -> dict:
    scores, color_note, skin_note, occasion_note, silhouette_note = score_outfit(
        top_category=top['category'],
        top_color=top['color'],
        top_fit=top['fit'],
        bottom_category=bottom['category'],
        bottom_color=bottom['color'],
        bottom_fit=bottom['fit'],
        shoe_category=shoe['category'],
        shoe_color=shoe['color'],
        occasion=occasion,
        skin_tone=skin_tone,
        layer_category=layer['category'] if layer else None,
        layer_color=layer['color'] if layer else None,
    )

    return {
        'top': top,
        'layer': layer,
        'bottom': bottom,
        'footwear': shoe,
        'scores': scores,
        'formality': top['formality'],
        'color_explanation': color_note,
        'skin_tone_note': skin_note,
        'occasion_note': occasion_note,
        'silhouette_note': silhouette_note,
        'total_score': scores.total,
    }

def generate_outfits(
    wardrobe: list[ClothingItem],
    occasion: str,
    skin_tone: str,
    anchor_item: ClothingItem = None,
) -> dict:
    allowed_formality = get_allowed_formality(occasion)
    split = get_occasion_split(occasion)

    # Expand items by color
    tops = [
        e for item in wardrobe
        if item.category in TOP_CATEGORIES
        and get_formality(item.category) in allowed_formality
        for e in expand_by_color(item)
    ]

    layers = [
        e for item in wardrobe
        if item.category in LAYER_CATEGORIES
        and get_formality(item.category) in allowed_formality
        for e in expand_by_color(item)
    ] if LAYERING_ENABLED else []

    bottoms = [
        e for item in wardrobe
        if item.category in BOTTOM_CATEGORIES
        and get_formality(item.category) in allowed_formality
        for e in expand_by_color(item)
    ]

    footwear = [
        e for item in wardrobe
        if item.category in FOOTWEAR_CATEGORIES
        and get_formality(item.category) in allowed_formality
        for e in expand_by_color(item)
    ]

    if not tops or not bottoms or not footwear:
        return {'error': 'Not enough items for this occasion. Add more clothing.'}

    # Filter by anchor
    if anchor_item:
        anchor_color = anchor_item.colors[0]
        anchor_category = anchor_item.category

        if anchor_category in TOP_CATEGORIES:
            tops = [t for t in tops if t['category'] == anchor_category and t['color'] == anchor_color]
        elif anchor_category in BOTTOM_CATEGORIES:
            bottoms = [b for b in bottoms if b['category'] == anchor_category and b['color'] == anchor_color]
        elif anchor_category in FOOTWEAR_CATEGORIES:
            footwear = [f for f in footwear if f['category'] == anchor_category and f['color'] == anchor_color]
        elif anchor_category in LAYER_CATEGORIES:
            layers = [l for l in layers if l['category'] == anchor_category and l['color'] == anchor_color]

    # Generate all combinations
    all_outfits = []

    for top, bottom, shoe in product(tops, bottoms, footwear):
        outfit = build_outfit_object(top, bottom, shoe, occasion, skin_tone)
        if outfit['total_score'] >= MIN_SCORE_THRESHOLD:
            all_outfits.append(outfit)

        # With layer
        if LAYERING_ENABLED:
            for layer in layers:
                if can_layer(top['category'], layer['category']):
                    layered = build_outfit_object(top, bottom, shoe, occasion, skin_tone, layer)
                    if layered['total_score'] >= MIN_SCORE_THRESHOLD:
                        all_outfits.append(layered)

    # Sort by score
    all_outfits.sort(key=lambda x: x['total_score'], reverse=True)

    # Split by formality
    casual_outfits = [o for o in all_outfits if o['formality'] == 'casual']
    smart_outfits = [o for o in all_outfits if o['formality'] == 'smart_casual']

    # Apply diversity filter
    casual_diverse = filter_diverse(casual_outfits)
    smart_diverse = filter_diverse(smart_outfits)

    # Get target counts
    casual_count = split.get('casual', 3)
    smart_count = split.get('smart_casual', 2)

    # Fallback if not enough smart casual
    final_casual = casual_diverse[:casual_count]
    final_smart = smart_diverse[:smart_count]

    if len(final_smart) < smart_count:
        extra_needed = smart_count - len(final_smart)
        extra_casual = [
            o for o in casual_diverse
            if o not in final_casual
        ][:extra_needed]
        final_casual += extra_casual

    return {
        'casual': final_casual,
        'smart_casual': final_smart,
        'fallback_used': len(final_smart) < smart_count,
    }