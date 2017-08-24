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
        km = kmeans(kdata, k)
        data['cluster'] = km.labels_

    elif case==1: # kmedoid clustering
        kmd = kmedoid(kdata, k, trial)
        data['cluster'] = kmd.labels_

    return data, metrics.silhouette_score(x, km.labels_, metric='euclidean')

def kmeans(kdata, n_clusters):
    k = KMeans(n_clusters=n_clusters, random_state=33).fit(kdata)
    return k

def kmedoid(kdata, n_clusters, n_trial):
    k = pyclust.KMedoids(n_clusters=n_clusters, n_trials=n_trial)
    k.fit(kdata.values)
    return k