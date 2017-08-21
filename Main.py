import Preprocess
import Clustering
from sklearn import metrics
def main():
    path = '생육조사자료_2작기.xlsx'
    data = Preprocess.preprocess(path)
    attribute = ['초장(cm)', '경경(mm)', '잎길이(cm)', '잎 폭(cm)', '잎 수 (개)']
    ksample = Clustering.clustering(data, attribute, 4)
    #print(ksample)


if __name__ == "__main__":
    main()