# All weights and settings in one place
# Change here to affect entire system

SCORING_WEIGHTS = {
    'color_harmony': 0.40,
    'skin_tone':     0.30,
    'occasion':      0.20,
    'popularity':    0.10,
}

# How many outfits to return per occasion split
# Can override per occasion in occasion_rules.py
DEFAULT_OUTFIT_COUNT = 5

# Diversity threshold
# Two outfits must differ in at least this many items
MIN_DIVERSITY = 2

# Minimum score to include an outfit in results
MIN_SCORE_THRESHOLD = 4.0

# Layering
LAYERING_ENABLED = True

# Fit/silhouette rules
SILHOUETTE_ENABLED = True

# Gap analysis
GAP_ANALYSIS_ENABLED = True
GAP_ANALYSIS_MAX_RECOMMENDATIONS = 3

# Future flags — set to True when ready
USE_ML_SCORING = False
USE_TREND_API = False
USE_IMAGE_CLASSIFICATION = False