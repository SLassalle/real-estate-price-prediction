# src/preprocessing.py
from __future__ import annotations

from typing import List, Tuple, Optional

import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.impute import SimpleImputer


# ----------------------------
# Configuration
# ----------------------------

TARGET_COL = "SalePrice"

# Dropped by design (Issue #4)
DROP_COLS = [
    "Order",
    "PID",
    "Mo Sold",
    "Yr Sold",
    "Sale Type",
    "Sale Condition",
    "Pool QC",
    "Alley",
    "Fence",
    "Misc Feature",
]

# Ordinal columns (from inventory)
ORDINAL_COLS = [
    "Overall Qual",
    "Overall Cond",
    "Exter Qual",
    "Exter Cond",
    "Bsmt Qual",
    "Bsmt Cond",
    "Bsmt Exposure",
    "BsmtFin Type 1",
    "BsmtFin Type 2",
    "Heating QC",
    "Kitchen Qual",
    "Functional",
    "Fireplace Qu",
    "Garage Finish",
    "Garage Qual",
    "Garage Cond",
    "Land Slope",
    "Lot Shape",
    "Paved Drive",
]

# Nominal categorical (one-hot)
NOMINAL_COLS = [
    "MS Zoning",
    "Street",
    "Land Contour",
    "Utilities",
    "Lot Config",
    "Neighborhood",
    "Condition 1",
    "Condition 2",
    "Bldg Type",
    "House Style",
    "Roof Style",
    "Roof Matl",
    "Exterior 1st",
    "Exterior 2nd",
    "Mas Vnr Type",
    "Foundation",
    "Heating",
    "Central Air",
    "Electrical",
    "Garage Type",
]

# Numeric columns (from inventory)
NUMERIC_COLS = [
    "Lot Frontage",
    "Lot Area",
    "Mas Vnr Area",
    "BsmtFin SF 1",
    "BsmtFin SF 2",
    "Bsmt Unf SF",
    "Total Bsmt SF",
    "1st Flr SF",
    "2nd Flr SF",
    "Low Qual Fin SF",
    "Gr Liv Area",
    "Bsmt Full Bath",
    "Bsmt Half Bath",
    "Full Bath",
    "Half Bath",
    "Bedroom AbvGr",
    "Kitchen AbvGr",
    "TotRms AbvGrd",
    "Fireplaces",
    "Garage Cars",
    "Garage Area",
    "Wood Deck SF",
    "Open Porch SF",
    "Enclosed Porch",
    "3Ssn Porch",
    "Screen Porch",
    "Pool Area",
    "Misc Val",
]


# ----------------------------
# Ordinal mappings
# ----------------------------

QUAL_SCALE = ["None", "Po", "Fa", "TA", "Gd", "Ex"]

ORDINAL_CATEGORIES = {
    # Quality/Condition style variables
    "Exter Qual": QUAL_SCALE,
    "Exter Cond": QUAL_SCALE,
    "Bsmt Qual": QUAL_SCALE,
    "Bsmt Cond": QUAL_SCALE,
    "Heating QC": QUAL_SCALE,
    "Kitchen Qual": QUAL_SCALE,
    "Fireplace Qu": QUAL_SCALE,
    "Garage Qual": QUAL_SCALE,
    "Garage Cond": QUAL_SCALE,
    # Basement exposure
    "Bsmt Exposure": ["None", "No", "Mn", "Av", "Gd"],
    # Basement finish types
    "BsmtFin Type 1": ["None", "Unf", "LwQ", "Rec", "BLQ", "ALQ", "GLQ"],
    "BsmtFin Type 2": ["None", "Unf", "LwQ", "Rec", "BLQ", "ALQ", "GLQ"],
    # Garage finish
    "Garage Finish": ["None", "Unf", "RFn", "Fin"],
    # Land slope
    "Land Slope": ["Gtl", "Mod", "Sev"],
    # Lot shape
    "Lot Shape": ["IR3", "IR2", "IR1", "Reg"],
    # Paved drive
    "Paved Drive": ["N", "P", "Y"],
    # Functional
    "Functional": ["Sal", "Sev", "Maj2", "Maj1", "Mod", "Min2", "Min1", "Typ"],
}


# ----------------------------
# Validation
# ----------------------------

def _validate_columns(
    df: pd.DataFrame,
    *,
    require_target: bool = True
) -> None:
    """
    Fail fast if expected columns are missing.

    require_target=True  -> train dataset
    require_target=False -> inference dataset (no target)
    """
    expected = set(NUMERIC_COLS + NOMINAL_COLS + ORDINAL_COLS + DROP_COLS)
    if require_target:
        expected.add(TARGET_COL)

    missing = sorted(list(expected - set(df.columns)))
    if missing:
        raise ValueError(f"Missing expected columns in dataframe: {missing}")


# ----------------------------
# Custom transformer
# ----------------------------

class DropColumns(BaseEstimator, TransformerMixin):
    """
    sklearn-compatible dropper.
    Safe for inference: errors='ignore'.
    """
    def __init__(self, columns: List[str]):
        self.columns = columns

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X.drop(columns=self.columns, errors="ignore")


# ----------------------------
# Preprocessor
# ----------------------------

def make_preprocessor() -> ColumnTransformer:
    """
    Leakage-safe preprocessing:
    - Numeric: median imputation
    - Nominal categorical: most_frequent imputation + one-hot
    - Ordinal categorical: constant 'None' + ordinal encoding
    - Overall Qual/Cond remain numeric (already ordinal numeric)
    """

    ordinal_numeric = ["Overall Qual", "Overall Cond"]
    ordinal_encode = [c for c in ORDINAL_COLS if c not in ordinal_numeric]

    # Keep order consistent with ordinal_encode
    categories_in_order = [ORDINAL_CATEGORIES[c] for c in ordinal_encode]

    numeric_pipe = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
    ])

    nominal_pipe = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])

    ordinal_pipe = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="constant", fill_value="None")),
        ("ordinal", OrdinalEncoder(
            categories=categories_in_order,
            handle_unknown="use_encoded_value",
            unknown_value=-1,
        )),
    ])

    ordinal_numeric_pipe = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_pipe, NUMERIC_COLS),
            ("nom", nominal_pipe, NOMINAL_COLS),
            ("ord_num", ordinal_numeric_pipe, ordinal_numeric),
            ("ord", ordinal_pipe, ordinal_encode),
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )

    return preprocessor


def make_full_pipeline() -> Pipeline:
    """
    Full preprocessing pipeline (enterprise pattern):
    drop -> column transformer
    """
    return Pipeline(steps=[
        ("drop", DropColumns(DROP_COLS)),
        ("prep", make_preprocessor()),
    ])


# ----------------------------
# Split helpers
# ----------------------------

def split_X_y(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    _validate_columns(df, require_target=True)

    # Keep raw X (with DROP_COLS still present) to prove that the pipeline is responsible for dropping
    X = df.drop(columns=[TARGET_COL])
    y = df[TARGET_COL].copy()
    return X, y


# ----------------------------
# Notebook helpers
# ----------------------------

def fit_transform_preview(df: pd.DataFrame, n_rows: int = 5) -> None:
    """
    Quick sanity check helper for notebooks:
    - ensures pipeline fits end-to-end (drop included)
    - prints shapes and feature names preview
    """
    X, y = split_X_y(df)
    pipe = make_full_pipeline()
    X_t = pipe.fit_transform(X, y)

    print("Raw X shape:", X.shape)
    print("y shape:", y.shape)
    print("Transformed X shape:", X_t.shape)

    try:
        pre = pipe.named_steps["prep"]
        feat_names = pre.get_feature_names_out()
        print("n_features_out:", len(feat_names))
        print("first 30 feature names:", list(feat_names[:30]))
    except Exception:
        print("Feature names not available.")

    print("Preview (first rows):")
    print(X_t[:n_rows])


def validate_with_cv(
    df: pd.DataFrame,
    *,
    cv: int = 5,
    scoring: str = "neg_root_mean_squared_error",
    model=None
) -> dict:
    """
    Minimal enterprise validation for Issue requirement:
    - run cross-validation with a baseline model
    - proves leakage-safe fit/transform per fold

    Returns dict with mean/std of CV scores.

    Notes:
    - default model is Ridge (strong baseline for regression)
    """
    from sklearn.linear_model import Ridge
    from sklearn.model_selection import cross_val_score

    if model is None:
        model = Ridge(alpha=1.0)

    X, y = split_X_y(df)

    model_pipe = Pipeline(steps=[
        ("prep", make_full_pipeline()),
        ("model", model),
    ])

    scores = cross_val_score(
        model_pipe,
        X,
        y,
        cv=cv,
        scoring=scoring
    )

    return {
        "cv": cv,
        "scoring": scoring,
        "mean_score": float(scores.mean()),
        "std_score": float(scores.std()),
        "all_scores": [float(s) for s in scores],
    }
