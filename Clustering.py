import pandas as pd
from sklearn.cluster import KMeans
from sklearn import preprocessing, metrics
import pyclust

def clustering(data, attribute, k, case, trial):
    kdata = data[[x for x in attribute]] # define attribute of clustering
    x = kdata.values
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    kdata = pd.DataFrame(x_scaled)

    if case==0: # kmeans clustering
        kmLabel = kmeans(kdata, k).labels_
        data['cluster'] = kmLabel
        silhouette_score = metrics.silhouette_score(x, kmLabel, metric='euclidean')
    elif case==1: # kmedoid clustering
        kmdLabel = kmedoid(kdata, k, trial)
        data['cluster'] = kmdLabel
        silhouette_score = metrics.silhouette_score(x, kmdLabel, metric='euclidean')

    return data, silhouette_score

def kmeans(kdata, n_clusters):
    k = KMeans(n_clusters=n_clusters, random_state=33).fit(kdata)
    return k

def kmedoid(kdata, n_clusters, n_trial):
    kmd = pyclust.KMedoids(n_clusters=n_clusters, n_trials=n_trial)
    kmd.fit(kdata.values)

    return kmd.labels_