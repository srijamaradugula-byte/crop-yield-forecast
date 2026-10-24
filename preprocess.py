"""Data cleaning and feature transformation."""
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from .config import CATEGORICAL, NUMERIC, TARGET, FEATURES

def load_and_clean(path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]
    for col in CATEGORICAL:
        df[col] = df[col].astype(str).str.strip().str.lower()
    df = df.drop_duplicates()
    df = df.dropna(subset=[TARGET])
    df = df[df[TARGET] > 0]
    # drop extreme yield outliers per crop (3 x IQR rule)
    q = df.groupby("crop")[TARGET].quantile([0.25, 0.75]).unstack()
    iqr = q[0.75] - q[0.25]
    lo = df["crop"].map(q[0.25] - 3 * iqr)
    hi = df["crop"].map(q[0.75] + 3 * iqr)
    df = df[(df[TARGET] >= lo) & (df[TARGET] <= hi)]
    return df[FEATURES + [TARGET]].reset_index(drop=True)

def build_preprocessor() -> ColumnTransformer:
    num = Pipeline([("impute", SimpleImputer(strategy="median")),
                    ("scale", StandardScaler())])
    cat = Pipeline([("impute", SimpleImputer(strategy="most_frequent")),
                    ("onehot", OneHotEncoder(handle_unknown="ignore"))])
    return ColumnTransformer([("num", num, NUMERIC), ("cat", cat, CATEGORICAL)])
