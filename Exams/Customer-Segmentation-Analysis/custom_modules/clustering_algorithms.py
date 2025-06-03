import numpy as np
from sklearn.cluster import KMeans, AgglomerativeClustering
from fcmeans import FCM


def kmeans_clustering(data, k):
    model = KMeans(n_clusters=k, n_init=10, random_state=42)
    labels = model.fit_predict(data)
    return labels

def ward_clustering(data, k):
    model = AgglomerativeClustering(n_clusters=k, linkage='ward')
    labels = model.fit_predict(data)
    return labels

def fuzzy_cmeans_clustering(data, k):
    model = FCM(n_clusters=k)
    model.fit(data)
    labels = model.predict(data)
    memberships = model.u  # fuzzy membership matrix
    return labels, memberships
