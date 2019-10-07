import numpy as np
from scipy import stats
import scipy.stats as stats
import pandas as pd

meta = pd.read_pickle("/Volumes/NATHAN/out/metadata/improved_meta/complete.pkl")

kind = 'avg_time_short'

times = meta[['medium', kind]]
times = times[pd.notnull(times.avg_time_short)]

film_times =  times[times['medium'] == 'films'][kind].values.tolist()
novel_times =  times[times['medium'] == 'novels'][kind].values.tolist()
tv_times =  times[times['medium'] == 'tv'][kind].values.tolist()

from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.multicomp import MultiComparison

f, p = stats.f_oneway(film_times, novel_times, tv_times)
 
print ('One-way ANOVA')
print ('=============')
 
print ('F value:', f)
print ('P value:', p, '\n')


mc = MultiComparison(times[kind].tolist(), times['medium'].tolist())
result = mc.tukeyhsd()
print(result)
print(mc.groupsunique)