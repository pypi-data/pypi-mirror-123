import math
from scipy.stats import norm,t

def ztest(X:float, mu:float, sd:float,n:float,alpha=0.05,two_tail=False):

  """
  ztest(): Calculates Z test for single sample, two tailed as well as single.

  :param X: Sample mean
  :type X: float
  :param mu: Population mean/ Data mean
  :type mu: float
  :param sd: Standard Deviation
  :type sd: float
  :param n: Sample size
  :type n: float
  :param alpha: P value Limit/Significance value (default:0.05)
  :type alpha: float
  :param two_tail: Enter true for conducting two-tailed test. (default: False)
  :type two_tail: Boolean 
  :return: [Z value, Pvalue, True/False (Test was conclusive or not)]
  :rtype: list
  """
  tail=1

  if(two_tail):
    tail=2
  if(sd==0 or n==0):
    return None
  z=(X-mu)/(sd/(math.sqrt(n)))
  pval=tail*(norm.sf(abs(z)))
  conclusion = (pval<=alpha)

  return [round(z, 3), round(pval, 4), conclusion]

def ztest2(X1:float, X2:float, mudiff:float, sd1:float, sd2:float, n1:float, n2:float,alpha=0.05,two_tail=False):
  """
  ztest2(): Calculates Z test for two sampled data, two tailed as well as single.

  :param X1: Sample mean 1
  :type X: float
  :param X2: Sample mean 2
  :type X: float
  :param mudiff: mean difference
  :type mu: float
  :param sd1: Standard Deviation 1
  :type sd1: float
  :param sd2: Standard Deviation 2
  :type sd2: float
  :param n1: Sample size 1
  :type n1: float
  :param n2: Sample size 2
  :type n2: float
  :param alpha: P value Limit/Significance value (default:0.05)
  :type alpha: float
  :param two_tail: Enter true for conducting two-tailed test. (default: False)
  :type two_tail: Boolean 
  :return: [Z score, P value, True/False (Test was conclusive or not)]
  :rtype: list
  """

  tail=1
  if(two_tail):
    tail=2

  if(n1+n2<=0):
    return None

  pooledSE = math.sqrt(sd1**2/n1 + sd2**2/n2)
  if (pooledSE==0):
    return None
  z = ((X1 - X2) - mudiff)/pooledSE
  pval = tail*norm.sf(abs(z))
  conclusion = (pval<=alpha)
  return [round(z, 3), round(pval, 4), conclusion]

def ztestp(P1:float, P2:float,P:float, mudiff:float, n1:float, n2:float, alpha=0.05,two_tail=False):
  """
  ztestp(): Calculates Z test for two population proportions, two tailed as well as single.

  :param P1: Proportion 1
  :type P1: float
  :param P2: Proportion 2
  :type P2: float
  :param P: Overall Proportion 
  :type P: float
  :param mudiff: mean difference
  :type mudiff: float
  :param n1: Sample size 2
  :type n1: float
  :param n2: Sample size 2
  :type n2: float
  :param alpha: P value Limit/Significance value (default:0.05)
  :type alpha: float
  :param two_tail: Enter true for conducting two-tailed test. (default: False)
  :type two_tail: Boolean 
  :return: [Z value, Pvalue, True/False (Test was conclusive or not)]
  :rtype: list
  """
  tail=1
  if(two_tail):
    tail=2
  if(n1+n2<=0):
    return None
  z = ((P1-P2)-mudiff)/math.sqrt(P*(1-P)*((1/n1)+(1/n2)))
  pval = tail*norm.sf(abs(z))
  conclusion = (pval<=alpha)

  return [round(z, 3), round(pval, 4), conclusion]


def ttest(X:float, mu:float, sd:float, n:float, alpha=0.5,two_tail=False):
  """ttest(): Calculates T test for single sample, two tailed as well as single. This function works for Paired tests as well as the formula is same.

  :param X: Sample mean
  :type X: float
  :param mu: Population mean/ Data mean
  :type mu: float
  :param sd: Standard Deviation
  :type sd: float
  :param n: Sample size
  :type n: float
  :param alpha: P value Limit/Significance value (default:0.05)
  :type alpha: float
  :param two_tail: Enter true for conducting two-tailed test. (default: False)
  :type two_tail: Boolean 
  :return: [T score, P value, True/False (Test was conclusive or not)]
  :rtype: list
  """
  tail=1
  if(two_tail):
    tail=2
  if(sd==0 or n==0):
    return None

  tt=(X-mu)/(sd/(math.sqrt(n)))
  pval=tail*(t.sf(abs(tt),n-1))
  conclusion = (pval<=alpha)
  return [round(tt, 3), round(pval, 4), conclusion]

def ttest2(X1:float, X2:float, mudiff:float, sd1:float, sd2:float, n1:float, n2:float,alpha=0.05,V=False,two_tail=False):
  """ttest2(): Calculates T test for two sampled data (independent), two tailed as well as single.

  :param X1: Sample mean 1
  :type X: float
  :param X2: Sample mean 2
  :type X: float
  :param mudiff: mean difference
  :type mu: float
  :param sd1: Standard Deviation 1
  :type sd1: float
  :param sd2: Standard Deviation 2
  :type sd2: float
  :param n1: Sample size 1
  :type n1: float
  :param n2: Sample size 2
  :type n2: float
  :param alpha: P value Limit/Significance value (default:0.05)
  :type alpha: float
  :param V: Enter True assuming equal variances. (default: False)
  :type V: Boolean 
  :param two_tail: Enter true for conducting two-tailed test. (default: False)
  :type two_tail: Boolean 
  :return: [T score, P value, True/False (Test was conclusive or not)]
  :rtype: list
  """
  tail=1
  if(two_tail):
    tail=2
  if(n1+n2<=0):
    return None
  if(V):
    pooledSE = math.sqrt((((sd1**2)*(n1-1) +(sd2**2)*(n2-1))/(n1+n2-2)))*math.sqrt(1/n1 + 1/n2)
  else:
    pooledSE = math.sqrt(sd1**2/n1 + sd2**2/n2)
  print(pooledSE)


  if (pooledSE==0):
    return None
  tt = ((X1 - X2) - mudiff)/pooledSE
  pval = tail*(t.sf(abs(tt),n1+n2-2))
  conclusion = (pval<=alpha)

  return [round(tt, 3), round(pval, 4), conclusion]




