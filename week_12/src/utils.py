"""Visualization and reporting utilities used throughout the capstone notebook.

The functions in this file create confusion matrices, evaluation summaries,
ROC curves, and bar plots for feature importance and category distributions.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.metrics import confusion_matrix, roc_curve


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def plot_confusion_matrix(y_true, y_pred, labels=None) -> None:
    """Display a normalized confusion matrix for a classifier."""
    labels = labels or [0, 1]
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["No Churn", "Churn"], yticklabels=["No Churn", "Churn"])
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()
    plt.show()


def print_metrics(y_true, y_pred, y_prob=None) -> pd.DataFrame:
    """Create a metric summary table from a set of predictions."""
    from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score

    metrics = {
        "Accuracy": round(accuracy_score(y_true, y_pred), 4),
        "Precision": round(precision_score(y_true, y_pred), 4),
        "Recall": round(recall_score(y_true, y_pred), 4),
        "F1 Score": round(f1_score(y_true, y_pred), 4),
    }
    if y_prob is not None:
        metrics["ROC-AUC"] = round(roc_auc_score(y_true, y_prob), 4)
    return pd.DataFrame(metrics, index=[0])


def plot_roc_curve(y_true, y_prob, label: str) -> None:
    """Draw the receiver operating characteristic curve for a classifier."""
    fpr, tpr, _ = roc_curve(y_true, y_prob)
    plt.plot(fpr, tpr, label=label)
    plt.plot([0, 1], [0, 1], linestyle="--", color="gray")
    plt.title("ROC Curve")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_feature_importance(model, feature_names: list[str]) -> None:
    """Plot feature importances when the model exposes them."""
    if hasattr(model, "feature_importances_"):
        importances = pd.Series(model.feature_importances_, index=feature_names)
        importances = importances.sort_values(ascending=False)
        importances.plot(kind="bar", figsize=(10, 5), color="steelblue")
        plt.title("Feature Importance")
        plt.ylabel("Importance")
        plt.tight_layout()
        plt.show()


def save_summary_table(summary: pd.DataFrame, output_file: str | Path) -> None:
    """Persist a metrics comparison DataFrame as a CSV file."""
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(output_path, index=False)
