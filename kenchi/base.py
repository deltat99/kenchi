from abc import ABCMeta, abstractmethod

import numpy as np
from sklearn.base import BaseEstimator
from sklearn.metrics import confusion_matrix
from sklearn.utils.validation import check_X_y, check_array


class BaseDetector(BaseEstimator, metaclass=ABCMeta):
    """Base class for all detectors."""

    @abstractmethod
    def compute_anomaly_score(self, X):
        """Compute the anomaly score."""

        pass

    @abstractmethod
    def fit(self, X, y=None):
        """Fit the model according to the given training data."""

        pass

    def fit_predict(self, X, y=None):
        """"Fit the model to the training set X and returns the labels (0
        inlier, 1 outlier) on the training set.

        Parameters
        ----------
        X : array-like, shape = (n_samples, n_features)
            Samples.

        Returns
        -------
        is_outlier : ndarray, shape = (n_samples)
            Return 0 for inliers and 1 for outliers.
        """

        return self.fit(X, y).predict(X)

    def predict(self, X):
        """Predict if a particular sample is an outlier or not.

        Parameters
        ----------
        X : array-like, shape = (n_samples, n_features)
            Test samples.

        Returns
        -------
        is_outlier : ndarray, shape = (n_samples)
            Return 0 for inliers and 1 for outliers.
        """

        X = check_array(X)

        if isinstance(self._threshold, float):
            return (
                self.compute_anomaly_score(X) > self._threshold
            ).astype(np.int32)

        else:
            return np.any(
                self.compute_anomaly_score(X) > self._threshold, axis=1
            ).astype(np.int32)


class DetectorMixin:
    """Mixin class for all detectors."""

    def score(self, X, y):
        """Return the F1 score.

        Parameters
        ----------
        X : array-like, shape = (n_samples, n_features)
            Test samples.

        y : array-like, shape = (n_samples)
            True labels for test samples.

        Returns
        -------
        score : float
            F1 score.
        """

        X, y           = check_X_y(X, y)

        # Compute the confusion matrix
        cnf_matrix     = confusion_matrix(y, self.predict(X), [1, 0])
        tp, fn, fp, tn = np.ravel(cnf_matrix)

        # Compute the specificity (a.k.a. normal sample accuracy)
        r0             = tn / (fp + tn)

        # Compute the sensitivity (a.k.a. anomalous sample accuracy)
        r1             = tp / (tp + fn)

        return 2.0 * r0 * r1 / (r0 + r1)
