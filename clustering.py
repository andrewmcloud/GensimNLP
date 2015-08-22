__author__ = 'andrew'

from sklearn.cluster import KMeans
from gensim import matutils, corpora, interfaces
from numpy import transpose, where
from fileTools import verify_filesave
from operator import itemgetter
from itertools import chain
from scipy.sparse import coo_matrix
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cm
import os

def kmeans(data, k=3):
    if (isinstance(data, corpora.MmCorpus)):
        data = matutils.corpus2csc(data)
    elif (isinstance(data, interfaces.TransformedCorpus)):
        data = matutils.corpus2csc(data)
    else:
        raise SystemExit('Clustering on non-gensim objects not implemented.')
    data = transpose(data)
    km = KMeans(n_clusters=k)
    clusters = km.fit_predict(data)
    centers = km.cluster_centers_
    return data, clusters, centers


def plot_2d_clusters(data, clusters, centers, writedir, filename='clusters.png'):
    k = len(centers)
    data = data.toarray()

    rainbow = plt.get_cmap('rainbow')
    cNorm = colors.Normalize(vmin=0, vmax=k)
    scalarMap = cm.ScalarMappable(norm=cNorm, cmap=rainbow)

    #plot each cluster in separate color
    for c in range(0, k):
        inds = where(clusters == c)[0]
        print(inds)
        print(data[inds,0:2])
        colorVal = scalarMap.to_rgba(c)
        plt.scatter(data[inds,0], data[inds,1], color=colorVal, marker='x')
        plt.scatter(centers[c,0], centers[c,1], color=colorVal, marker='o')
        plt.annotate(c, xy=(centers[c,0], centers[c,1]))

    plot_path = os.path.join(writedir + verify_filesave(writedir, filename))
    plt.savefig(plot_path)
    plt.show()

def cluster_terms(data, clusters, centers, dictionary, writedir, filename='cluster_terms.txt'):
    k = len(centers)

    #create an ordered list of terms from dictionary
    feature_names = sorted(dictionary.items(), key=itemgetter(0))
    feature_names = [x[1] for x in feature_names]


    for c in range(0, k):
        print '\nCluster {}'.format(c)
        inds = where(clusters == c)[0]
        notinds = where(clusters != c)[0]

        xinds = data[inds, :]
        xnotinds = data[notinds, :]
        cluster_words = xinds.mean(axis=0) - xnotinds.mean(axis=0)

        s = sorted(tuple(zip(feature_names, cluster_words.transpose())), key=lambda q: q[1], reverse=True)

        for i in range(0, 20):
            print '{}: {}'.format(s[i][0], s[i][1].item(0))




