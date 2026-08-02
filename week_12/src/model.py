"""Model training, evaluation, and persistence utilities.

The module exposes a small set of functions that train several classifiers,
compare their performance, tune the random forest model, and save the best
trained pipeline to disk for deployment.
"""

from __future__ import annotations

import pickle
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from .data_preprocessing import build_pipeline, clean_dataset, load_dataset, split_data


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_OUTPUT = PROJECT_ROOT / "deployment" / "saved_model.pkl"


def train_models(dataframe: pd.DataFrame):
    """Train the main classification models using the cleaned dataset."""
    cleaned = clean_dataset(dataframe)
    X_train, X_test, y_train, y_test = split_data(cleaned)

    models = {
        "Logistic Regression": build_pipeline(LogisticRegression(max_iter=1000, random_state=42)),
        "Decision Tree": build_pipeline(DecisionTreeClassifier(random_state=42)),
        "Random Forest": build_pipeline(RandomForestClassifier(random_state=42, n_estimators=200)),
        "SVM": build_pipeline(SVC(probability=True, random_state=42)),
        "KNN": build_pipeline(KNeighborsClassifier(n_neighbors=5)),
    }

    results = {}
    for name, pipeline in models.items():
        pipeline.fit(X_train, y_train)
        predicted = pipeline.predict(X_test)
        predicted_probs = pipeline.predict_proba(X_test)[:, 1]

        results[name] = {
            "model": pipeline,
            "accuracy": accuracy_score(y_test, predicted),
            "precision": precision_score(y_test, predicted),
            "recall": recall_score(y_test, predicted),
            "f1": f1_score(y_test, predicted),
            "roc_auc": roc_auc_score(y_test, predicted_probs),
            "confusion": confusion_matrix(y_test, predicted),
            "report": classification_report(y_test, predicted, digits=4),
        }
    return cleaned, results


def tune_random_forest(dataframe: pd.DataFrame):
    """Perform hyperparameter tuning on the Random Forest model using GridSearchCV."""
    cleaned = clean_dataset(dataframe)
    X_train, X_test, y_train, y_test = split_data(cleaned)

    estimator = build_pipeline(
        RandomForestClassifier(random_state=42)
    )
    param_grid = {
        "model__n_estimators": [100, 200],
        "model__max_depth": [None, 5, 8],
        "model__min_samples_split": [2, 5],
        "model__min_samples_leaf": [1, 2],
    }

    grid_search = GridSearchCV(
        estimator=estimator,
        param_grid=param_grid,
        scoring="roc_auc",
        cv=3,
        n_jobs=-1,
    )
    grid_search.fit(X_train, y_train)
    tuned_model = grid_search.best_estimator_
    predicted = tuned_model.predict(X_test)
    predicted_probs = tuned_model.predict_proba(X_test)[:, 1]

    metrics = {
        "best_params": grid_search.best_params_,
        "best_score": grid_search.best_score_,
        "accuracy": accuracy_score(y_test, predicted),
        "precision": precision_score(y_test, predicted),
        "recall": recall_score(y_test, predicted),
        "f1": f1_score(y_test, predicted),
        "roc_auc": roc_auc_score(y_test, predicted_probs),
        "confusion": confusion_matrix(y_test, predicted),
    }
    return tuned_model, metrics


def save_model(model, file_path: str | Path = MODEL_OUTPUT) -> None:
    """Persist a trained sklearn pipeline to disk using pickle."""
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("wb") as model_file:
        pickle.dump(model, model_file)


def compare_models(results: dict) -> pd.DataFrame:
    """Create a tidy comparison table for all trained candidate models."""
    summary = []
    for name, metrics in results.items():
        summary.append(
            {
                "Model": name,
                "Accuracy": round(metrics["accuracy"], 4),
                "Precision": round(metrics["precision"], 4),
                "Recall": round(metrics["recall"], 4),
                "F1 Score": round(metrics["f1"], 4),
                "ROC-AUC": round(metrics["roc_auc"], 4),
            }
        )
    return pd.DataFrame(summary).sort_values(by="ROC-AUC", ascending=False)
