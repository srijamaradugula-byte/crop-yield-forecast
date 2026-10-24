"""Turn a numeric forecast into a farmer advisory message (English + Telugu)."""

# typical yield (quintals/acre) used to judge whether forecast is low/normal/high
BENCHMARK = {"paddy": 24, "cotton": 9, "maize": 28, "chilli": 14}

def build_alert(crop: str, district: str, predicted: float, area_acres: float) -> dict:
    ref = BENCHMARK.get(crop.lower())
    total = predicted * area_acres
    if ref is None:
        level = "normal"
    elif predicted < 0.85 * ref:
        level = "low"
    elif predicted > 1.1 * ref:
        level = "high"
    else:
        level = "normal"

    tips_en = {
        "low": "Expected yield is below average. Check irrigation and pest/disease status; consult your local agriculture officer.",
        "normal": "Expected yield is near average. Continue current practices.",
        "high": "Expected yield is above average. Arrange storage and market early.",
    }
    tips_te = {
        "low": "దిగుబడి సగటు కంటే తక్కువగా ఉండే అవకాశం ఉంది. నీటి పారుదల, తెగుళ్లను పరిశీలించి వ్యవసాయ అధికారిని సంప్రదించండి.",
        "normal": "దిగుబడి సగటుకు దగ్గరగా ఉంటుంది. ప్రస్తుత పద్ధతులను కొనసాగించండి.",
        "high": "దిగుబడి సగటు కంటే ఎక్కువగా ఉండే అవకాశం ఉంది. నిల్వ మరియు మార్కెట్ ముందే ఏర్పాటు చేసుకోండి.",
    }
    head = (f"{crop.title()} ({district.title()}): forecast {predicted:.1f} quintals/acre, "
            f"about {total:.1f} quintals for {area_acres} acres.")
    return {"level": level, "message_en": f"{head} {tips_en[level]}", "message_te": tips_te[level]}
