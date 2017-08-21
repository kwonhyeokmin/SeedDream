import pandas as pd
from sklearn.cluster import KMeans
from sklearn import preprocessing, metrics
import pyclust

def clustering(data, attribute, k):

    kdata = data[[x for x in attribute]] # define attribute of clustering
    x = kdata.values
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    kdata = pd.DataFrame(x_scaled)

    km = kmeans(kdata, k)
    data['km_'+str(k)] = km.labels_

    kmd = kmedoid(kdata, k, 50)
    data['kmd_'+str(k)] = kmd.labels_

    print('kmeans silhouette score: ', metrics.silhouette_score(x, km.labels_, metric='euclidean'))
    #print('kmedoids silhouette score: ', metrics.silhouette_score(x, kmd.labels_, metric='euclidean'))
    return data

def kmeans(kdata, n_clusters):
    k = KMeans(n_clusters=n_clusters, random_state=33).fit(kdata)
    return k

def kmedoid(kdata, n_clusters, n_trial):
    k = pyclust.KMedoids(n_clusters=n_clusters, n_trials=n_trial)
    k.fit(kdata.values)
    return k