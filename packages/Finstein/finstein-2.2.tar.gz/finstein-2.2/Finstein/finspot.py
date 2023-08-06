import math

def IR(spot:list, m=1):
    """
    IR(): A function to calculate Single Effective Interest Rate from an array of spot rates.

    :param spot: An array/List of Spot rates 
    :type spot: list
    :param m: Frequency of Interest Calculation (eg: 2 for Semi-annually), defaults to 1.
    :type m: float
    :return: float, None for -ve values of m.
    :rtype: float
    """
    if(m<=0 or len(spot)==0):
        return None
    return spot[-1]



def FR(spot:list, k:float, m=1):
    """
    FR(): A function to calculate Forward Rate from an array of spot rates.

    :param spot: An array/List of Spot rates 
    :type spot: list
    :param k: Term Period to calculate Forward rate from. (Eg: Nth year forward rate **K** years from now)
    :type k: float
    :param m: Frequency of Interest Calculation (eg: 2 for Semi-annually), defaults to 1.
    :type m: float
    :return: float, None for -ve values of m.
    :rtype: float
    """

    if(m<=0 or k<=0 or len(spot)<=1 or k>len(spot)):
        return None
    
    num = (1+spot[-1]/m)**(len(spot)*m)
    denom = (1+spot[k-1]/m)**(k*m)
    if(denom==0):
        return None

    sum = (num/denom) -1

    return sum
    