"""Reusable preprocessing utilities for the customer churn capstone project.

This module contains functions for loading the dataset, cleaning invalid values,
encoding categorical variables, scaling the numerical features, and splitting data
into training and testing sets.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "customer_churn.csv"


def load_dataset(csv_path: str | Path = DATA_PATH) -> pd.DataFrame:
    """Load the customer churn dataset into a pandas DataFrame."""
    dataframe = pd.read_csv(csv_path)
    return dataframe


def clean_dataset(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Clean the churn dataset by handling missing values and conversion issues."""
    cleaned = dataframe.copy()

    cleaned = cleaned.drop_duplicates().reset_index(drop=True)

    if "CustomerID" in cleaned.columns:
        cleaned = cleaned.drop(columns=["CustomerID"])

    cleaned["TotalCharges"] = pd.to_numeric(
        cleaned["TotalCharges"], errors="coerce"
    )
    cleaned["MonthlyCharges"] = pd.to_numeric(
        cleaned["MonthlyCharges"], errors="coerce"
    )
    cleaned["Tenure"] = pd.to_numeric(cleaned["Tenure"], errors="coerce")
    cleaned["SeniorCitizen"] = cleaned["SeniorCitizen"].astype("int64")

    cleaned = cleaned.dropna().reset_index(drop=True)
    return cleaned


def build_preprocessor() -> ColumnTransformer:
    """Create a preprocessing transformer for numerical and categorical fields."""
    numeric_features = ["Tenure", "MonthlyCharges", "TotalCharges", "SeniorCitizen"]
    categorical_features = ["Contract", "PaymentMethod", "PaperlessBilling"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_features),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_features),
        ],
        remainder="drop",
    )
    return preprocessor


def build_pipeline(estimator) -> Pipeline:
    """Build a sklearn pipeline that combines preprocessing and a model."""
    pipeline = Pipeline(
        steps=[
            ("preprocessor", build_preprocessor()),
            ("model", estimator),
        ]
    )
    return pipeline


def split_data(dataframe: pd.DataFrame, test_size: float = 0.25, random_state: int = 42):
    """Split the dataset into training and testing partitions."""
    features = dataframe.drop(columns=["Churn"])
    target = dataframe["Churn"]
    return train_test_split(
        features,
        target,
        test_size=test_size,
        random_state=random_state,
        stratify=target,
    )
