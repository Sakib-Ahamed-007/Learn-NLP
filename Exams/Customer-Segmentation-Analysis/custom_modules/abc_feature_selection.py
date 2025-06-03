import numpy as np
from sklearn.metrics import silhouette_score

class ABCFeatureSelector:
    def __init__(self, data, num_bees=30, max_iter=20, k_range=(2, 6)):
        self.data = data
        self.num_bees = num_bees
        self.max_iter = max_iter
        self.k_range = k_range
        self.dim = data.shape[1]

    def _fitness(self, features_mask, k):
        selected = self.data[:, features_mask == 1]
        if selected.shape[1] == 0:
            return -1  # Avoid empty selection

        try:
            from sklearn.cluster import KMeans
            labels = KMeans(n_clusters=k, n_init=10).fit_predict(selected)
            score = silhouette_score(selected, labels)
            return score
        except:
            return -1

    def optimize(self, log_every=1):
        food_sources = np.random.randint(2, size=(self.num_bees, self.dim))
        cluster_k = np.random.randint(self.k_range[0], self.k_range[1] + 1, size=self.num_bees)
        fitness = np.array([self._fitness(food_sources[i], cluster_k[i]) for i in range(self.num_bees)])

        for it in range(self.max_iter):
            for i in range(self.num_bees):
                partner = np.random.randint(self.num_bees)
                phi = np.random.uniform(-1, 1, self.dim)
                candidate = np.clip(np.round(food_sources[i] + phi * (food_sources[i] - food_sources[partner])), 0, 1).astype(int)
                candidate_k = np.clip(cluster_k[i] + np.random.randint(-1, 2), *self.k_range)
                new_fitness = self._fitness(candidate, candidate_k)

                if new_fitness > fitness[i]:
                    food_sources[i] = candidate
                    cluster_k[i] = candidate_k
                    fitness[i] = new_fitness

            # 🖨️ Log status every `log_every` iterations
            if (it + 1) % log_every == 0 or it == self.max_iter - 1:
                best_index = np.argmax(fitness)
                print(f"[Iteration {it + 1}/{self.max_iter}] Best Fitness: {fitness[best_index]:.4f} | Best k: {cluster_k[best_index]} | Features Selected: {np.sum(food_sources[best_index])}")

        best_index = np.argmax(fitness)
        return food_sources[best_index], cluster_k[best_index], fitness[best_index]

