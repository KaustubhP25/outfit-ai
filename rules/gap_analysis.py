from config import GAP_ANALYSIS_MAX_RECOMMENDATIONS
from rules.color_rules import score_color_pair
from rules.occasion_rules import get_formality

TOP_CATEGORIES = ['tshirt', 'shirt', 'polo', 'hoodie', 'jacket']
BOTTOM_CATEGORIES = ['jeans', 'trousers', 'chinos', 'shorts']
FOOTWEAR_CATEGORIES = ['sneakers', 'boots', 'loafers', 'sandals']

# Most versatile items to recommend
VERSATILE_ITEMS = [
    {'category': 'sneakers',  'color': 'white',  'reason': 'White sneakers pair with almost every color and outfit'},
    {'category': 'sneakers',  'color': 'black',  'reason': 'Black sneakers are the most versatile footwear'},
    {'category': 'jeans',     'color': 'navy',   'reason': 'Navy jeans work with any top color'},
    {'category': 'jeans',     'color': 'black',  'reason': 'Black jeans elevate any casual outfit'},
    {'category': 'tshirt',    'color': 'white',  'reason': 'White tshirt is the most versatile base layer'},
    {'category': 'tshirt',    'color': 'black',  'reason': 'Black tshirt works with any bottom'},
    {'category': 'shirt',     'color': 'white',  'reason': 'White shirt works for casual and smart casual'},
    {'category': 'chinos',    'color': 'beige',  'reason': 'Beige chinos pair with warm and cool tones'},
    {'category': 'jacket',    'color': 'black',  'reason': 'Black jacket elevates any casual outfit'},
    {'category': 'boots',     'color': 'brown',  'reason': 'Brown boots add warmth to earth tone outfits'},
]

def count_new_outfits(new_item: dict, wardrobe: list) -> int:
    tops = [i for i in wardrobe if i.category in TOP_CATEGORIES]
    bottoms = [i for i in wardrobe if i.category in BOTTOM_CATEGORIES]
    footwear = [i for i in wardrobe if i.category in FOOTWEAR_CATEGORIES]

    new_category = new_item['category']
    new_color = new_item['color']

    count = 0

    if new_category in TOP_CATEGORIES:
        for bottom in bottoms:
            for shoe in footwear:
                for bc in bottom.colors:
                    for sc in shoe.colors:
                        if score_color_pair(new_color, bc) > 0.6:
                            count += 1

    elif new_category in BOTTOM_CATEGORIES:
        for top in tops:
            for shoe in footwear:
                for tc in top.colors:
                    for sc in shoe.colors:
                        if score_color_pair(tc, new_color) > 0.6:
                            count += 1

    elif new_category in FOOTWEAR_CATEGORIES:
        for top in tops:
            for bottom in bottoms:
                for tc in top.colors:
                    for bc in bottom.colors:
                        if score_color_pair(tc, bc) > 0.6:
                            count += 1

    return count

def analyze_gaps(wardrobe: list) -> list:
    if not GAP_ANALYSIS_ENABLED:
        return []

    existing = set()
    for item in wardrobe:
        for color in item.colors:
            existing.add((item.category, color.lower()))

    recommendations = []

    for item in VERSATILE_ITEMS:
        key = (item['category'], item['color'])
        if key in existing:
            continue

        unlocks = count_new_outfits(item, wardrobe)
        recommendations.append({
            'category': item['category'],
            'color': item['color'],
            'reason': item['reason'],
            'unlocks': unlocks,
        })

    recommendations.sort(key=lambda x: x['unlocks'], reverse=True)
    return recommendations[:GAP_ANALYSIS_MAX_RECOMMENDATIONS]

# Import here to avoid circular import
from config import GAP_ANALYSIS_ENABLED