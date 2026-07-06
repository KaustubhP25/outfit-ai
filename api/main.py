from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.types import OutfitRequest, OutfitResponse, GapItem
from core.engine import generate_outfits
from rules.gap_analysis import analyze_gaps

app = FastAPI(title='Outfit AI', version='1.0.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/health')
def health():
    return {'status': 'ok', 'version': '1.0.0'}

@app.post('/generate')
def generate(req: OutfitRequest):
    result = generate_outfits(
        wardrobe=req.wardrobe,
        occasion=req.occasion,
        skin_tone=req.skin_tone,
        anchor_item=req.anchor_item,
    )

    if 'error' in result:
        return {'error': result['error']}

    gaps = analyze_gaps(req.wardrobe)

    total_possible = len(result['casual']) + len(result['smart_casual'])

    return {
        'casual': result['casual'],
        'smart_casual': result['smart_casual'],
        'fallback_used': result.get('fallback_used', False),
        'gap_recommendations': gaps,
        'total_possible_outfits': total_possible,
    }