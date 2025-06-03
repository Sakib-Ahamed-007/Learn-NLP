import numpy as np

class FuzzyDecisionTreeNode:
    def __init__(self, depth=0, max_depth=3):
        self.feature_index = None
        self.threshold = None
        self.left = None
        self.right = None
        self.label = None
        self.depth = depth
        self.max_depth = max_depth

    def _fuzzy_gini(self, memberships):
        total_membership = np.sum(memberships, axis=0)
        gini = 1.0 - np.sum((total_membership / np.sum(total_membership)) ** 2)
        return gini

    def _best_split(self, X, y, memberships):
        best_index = None
        best_thresh = None
        best_gain = -1
        n_samples, n_features = X.shape

        for feature_idx in range(n_features):
            thresholds = np.unique(X[:, feature_idx])
            for t in thresholds:
                left_mask = X[:, feature_idx] <= t
                right_mask = ~left_mask

                if np.sum(left_mask) == 0 or np.sum(right_mask) == 0:
                    continue

                left_membership = memberships[left_mask]
                right_membership = memberships[right_mask]

                gini_total = self._fuzzy_gini(memberships)
                gini_left = self._fuzzy_gini(left_membership)
                gini_right = self._fuzzy_gini(right_membership)

                weighted_gini = (
                    (np.sum(left_membership) * gini_left +
                     np.sum(right_membership) * gini_right)
                    / np.sum(memberships)
                )
                gain = gini_total - weighted_gini

                if gain > best_gain:
                    best_gain = gain
                    best_index = feature_idx
                    best_thresh = t

        return best_index, best_thresh

    def fit(self, X, y, memberships):
        if self.depth >= self.max_depth or len(np.unique(y)) == 1:
            if len(y) == 0:
                self.label = 0
            else:
                self.label = np.bincount(y).argmax()
            return

        self.feature_index = index
        self.threshold = threshold

        left_mask = X[:, index] <= threshold
        right_mask = ~left_mask

        self.left = FuzzyDecisionTreeNode(self.depth + 1, self.max_depth)
        self.left.fit(X[left_mask], y[left_mask], memberships[left_mask])

        self.right = FuzzyDecisionTreeNode(self.depth + 1, self.max_depth)
        self.right.fit(X[right_mask], y[right_mask], memberships[right_mask])

    def predict_single(self, x):
        if self.label is not None:
            return self.label
        if x[self.feature_index] <= self.threshold:
            return self.left.predict_single(x)
        else:
            return self.right.predict_single(x)

    def predict(self, X):
        return np.array([self.predict_single(x) for x in X])
