from collections import Counter

def estimate(data, k):
    stdlen = len(data) / k

    counterList = []
    tlist = [x for x in range(k)]
    for i in range(0, k - 1):
        c = Counter(data['cluster'].iloc[int((i) * stdlen):int((i + 1) * stdlen)])
        for j in range(1, k + 1):
            t = c.most_common(j)[j-1]
            if t[0] in tlist:
                counterList.append(t[0])
                tlist.remove(t[0])
                break
    counterList.append(tlist[:][0])

    data['stdcluster'] = 0
    for i in range(0, k - 1):
        data['stdcluster'].iloc[int((i) * stdlen):int((i + 1) * stdlen)] = counterList[i]
    data['stdcluster'].iloc[int(k*stdlen):] = counterList[k-1]

    error = data['cluster']==data['stdcluster']
    count = 0
    for each in error:
        if each:
            count+=1

    print(count/len(error))

