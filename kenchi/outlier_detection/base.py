from abc import abstractmethod, ABC
from typing import Union

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.utils.validation import check_is_fitted

ArrayLike = Union[np.ndarray, pd.DataFrame]


class BaseDetector(BaseEstimator, ABC):
    """Base class for all outlier detectors."""

    # TODO: Implement plot_anomaly_score method
    # TODO: Implement plot_roc_curve method

    @abstractmethod
    def __init__(self, **params) -> None:
        """Initialize parameters."""

    @abstractmethod
    def check_params(self) -> None:
        """Check validity of parameters and raise ValueError if not valid."""

    @abstractmethod
    def fit(self, X: ArrayLike, y: None=None, **fit_params) -> 'BaseDetector':
        """Fit the model according to the given training data."""

    @abstractmethod
    def anomaly_score(self, X: ArrayLike=None) -> np.ndarray:
        """Compute the anomaly score for each sample."""

    @abstractmethod
    def score(self, X: ArrayLike, y: None=None) -> float:
        """Compute the mean log-likelihood of the given data."""

    def predict(self, X: ArrayLike=None, threshold: float=None) -> np.ndarray:
        """Predict if a particular sample is an outlier or not.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features), default None
            Data.

        threshold : float, default None
            User-provided threshold.

        Returns
        -------
        y_pred : ndarray of shape (n_samples,)
            Return 1 for inliers and -1 for outliers.
        """

        check_is_fitted(self, 'threshold_')

        if threshold is None:
            threshold = self.threshold_

        return np.where(self.anomaly_score(X) <= threshold, 1, -1)

    def fit_predict(
        self, X: ArrayLike, y: None=None, threshold: float=None, **fit_params
    ) -> np.ndarray:
        """Fit the model according to the given training data and predict if a
        particular sample is an outlier or not.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training Data.

        y : None
            Ignored.

        threshold : float, default None
            User-provided threshold.

        Returns
        -------
        y_pred : array-like of shape (n_samples,)
            Return 1 for inliers and -1 for outliers.
        """

        return self.fit(X, **fit_params).predict(threshold=threshold)