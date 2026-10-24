from src.alerts import build_alert
from src.config import DATA_PATH
from src.generate_sample_data import main as gen
from src.preprocess import load_and_clean

def test_cleaning_removes_duplicates_and_null_targets():
    gen(n=300)
    df = load_and_clean(DATA_PATH)
    assert not df.duplicated().any()
    assert df["yield_per_acre"].notna().all()

def test_alert_levels():
    assert build_alert("paddy", "eluru", 10, 2)["level"] == "low"
    assert build_alert("paddy", "eluru", 24, 2)["level"] == "normal"
    assert build_alert("paddy", "eluru", 30, 2)["level"] == "high"
