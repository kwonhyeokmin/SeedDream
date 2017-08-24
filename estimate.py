import numpy
import pandas as pd
def estimate(data, k):
    data = pd.DataFrame(numpy.random.rand(k), columns=['tall', 'cluster'])
    stdlist = numpy.arange(k)

