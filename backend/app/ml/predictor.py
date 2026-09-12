"""Machine Learning Model Inference Service (Hiruna, Sampath & Team)."""
import os
import pickle
import logging
from typing import Optional, Any
import numpy as np

logger = logging.getLogger(__name__)


class ResumeMatchPredictor:
    """Loads trained ML classification model and predicts candidate-job suitability percentage."""

    def __init__(self, model_path: Optional[str] = None):
        base_dir = os.path.dirname(__file__)
        self.model_path = model_path or os.path.join(base_dir, "model.pkl")
        self.model: Optional[Any] = None
        self.model_name: str = "Unavailable"
        self.load_model()

    def load_model(self) -> bool:
        """Load pickled scikit-learn model from disk."""
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, "rb") as f:
                    self.model = pickle.load(f)
                self.model_name = type(self.model).__name__
                logger.info(f"Loaded trained ML model: {self.model_name}")
                return True
            except Exception as e:
                logger.error(f"Error loading ML model from {self.model_path}: {e}")
                self.model = None
                self.model_name = "Error Loading"
                return False
        else:
            logger.warning(f"ML model artifact not found at {self.model_path}.")
            return False

    @property
    def is_ready(self) -> bool:
        return self.model is not None

    def predict_match_probability(self, feature_vector: np.ndarray) -> float:
        """Predict candidate suitability probability using the trained ML model.

        Returns match percentage between 0.0% and 100.0%.
        """
        if self.model is not None:
            try:
                # Use model.predict_proba for soft probability distribution [P(0), P(1)]
                proba = self.model.predict_proba(feature_vector)[0][1]
                return round(float(proba * 100.0), 1)
            except Exception as e:
                logger.error(f"Prediction failed with trained model: {e}")

        # If model is not trained yet, use weighted feature expectation
        # feature_vector has [tfidf_sim, skill_overlap, skill_count, missing_ratio, exp_delta, exp_fit, edu_ordinal]
        try:
            tfidf_sim = feature_vector[0][0]
            skill_overlap = feature_vector[0][1]
            exp_fit = feature_vector[0][5]
            baseline_score = (skill_overlap * 0.55) + (tfidf_sim * 0.30) + (exp_fit * 0.15)
            return round(float(np.clip(baseline_score * 100.0, 5.0, 99.0)), 1)
        except Exception:
            return 50.0


# Singleton predictor service
predictor_service = ResumeMatchPredictor()
