"""Train and evaluate the Gradient Boosting model.

Usage: python -m src.train
"""
import json
import joblib
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from .config import (DATA_PATH, FEATURES, METRICS_PATH, MODEL_PATH,
                     RANDOM_STATE, TARGET, TEST_SIZE)
from .preprocess import build_preprocessor, load_and_clean

def main() -> None:
    df = load_and_clean(DATA_PATH)
    X_train, X_test, y_train, y_test = train_test_split(
        df[FEATURES], df[TARGET], test_size=TEST_SIZE, random_state=RANDOM_STATE)

    pipe = Pipeline([
        ("prep", build_preprocessor()),
        ("model", GradientBoostingRegressor(random_state=RANDOM_STATE)),
    ])
    grid = {
        "model__n_estimators": [200, 400],
        "model__learning_rate": [0.05, 0.1],
        "model__max_depth": [3, 4],
    }
    search = GridSearchCV(pipe, grid, cv=3, scoring="neg_mean_absolute_error", n_jobs=-1)
    search.fit(X_train, y_train)

    pred = search.predict(X_test)
    metrics = {
        "best_params": search.best_params_,
        "mae": float(mean_absolute_error(y_test, pred)),
        "rmse": float(np.sqrt(mean_squared_error(y_test, pred))),
        "r2": float(r2_score(y_test, pred)),
        "train_rows": int(len(X_train)), "test_rows": int(len(X_test)),
    }
    MODEL_PATH.parent.mkdir(exist_ok=True)
    joblib.dump(search.best_estimator_, MODEL_PATH)
    METRICS_PATH.write_text(json.dumps(metrics, indent=2))
    print(json.dumps(metrics, indent=2))

if __name__ == "__main__":
    main()
