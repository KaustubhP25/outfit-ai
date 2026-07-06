from pydantic import BaseModel
from typing import Optional

class ClothingItem(BaseModel):
    id: str
    category: str
    colors: list[str]
    pattern: str = 'solid'
    fit: str = 'regular'  # regular, baggy
    image_url: Optional[str] = None

class OutfitRequest(BaseModel):
    occasion: str
    skin_tone: str  # spring, summer, autumn, winter
    wardrobe: list[ClothingItem]
    anchor_item: Optional[ClothingItem] = None

class OutfitItem(BaseModel):
    category: str
    color: str
    fit: str
    image_url: Optional[str] = None

class LayerItem(BaseModel):
    category: str
    color: str
    fit: str
    image_url: Optional[str] = None

class OutfitScores(BaseModel):
    color_harmony: float
    skin_tone: float
    occasion: float
    popularity: float
    silhouette: float
    total: float

class Outfit(BaseModel):
    top: OutfitItem
    layer: Optional[LayerItem] = None
    bottom: OutfitItem
    footwear: OutfitItem
    scores: OutfitScores
    formality: str
    color_explanation: str
    skin_tone_note: str
    occasion_note: str
    silhouette_note: str

class GapItem(BaseModel):
    category: str
    color: str
    reason: str
    unlocks: int  # how many new outfits this adds

class OutfitResponse(BaseModel):
    casual: list[Outfit]
    smart_casual: list[Outfit]
    gap_recommendations: list[GapItem]
    total_possible_outfits: int