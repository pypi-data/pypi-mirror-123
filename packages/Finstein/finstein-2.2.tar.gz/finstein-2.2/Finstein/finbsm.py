import numpy as np
from scipy.stats import norm
N = norm.cdf

def bsm(S:float, K:float, T:float, r:float, sigma:float,call_value="both"):

    """
    bsm(): Implementation of Black-Scholes formula for non-dividend paying options

    :param S: Current asset price
    :type S: float
    :param K: Strike price of the option
    :type K: float
    :param T: Time until option expiration 
    :type T: float
    :param r: Risk-free interest rate.
    :type r: float
    :param sigma: Annualized volatility of the asset's returns 
    :type sigma: float
    :param call_value: Takes input as "call", "put", "both"
    :type call_value: string
    :return: Price of the options
    :rtype: float. Returns a dictionary when call_value is set to "both"
    """
    d1 = (np.log(S/K) + (r + sigma**2/2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    Value = 0

    if(call_value=="both"):
        Value_call =  S * N(d1) - K * np.exp(-r*T)* N(d2)
        Value_put = K*np.exp(-r*T)*N(-d2) - S*N(-d1)
        return {"put":Value_put, "call":Value_call}

    if(call_value=="call"):
        Value = S * N(d1) - K * np.exp(-r*T)* N(d2)

    elif(call_value=="put"):
        Value = K*np.exp(-r*T)*N(-d2) - S*N(-d1)
    return Value 

    

def bsm_div(S:float, K:float, T:float, r:float, q:float, sigma:float,call_value="both"):

    """
    bsm_div(): Implementation of Black-Scholes formula for Dividend paying options

    :param S: Current asset price
    :type S: float
    :param K: Strike price of the option
    :type K: float
    :param T: Time until option expiration 
    :type T: float
    :param r: Risk-free interest rate.
    :type r: float
    :param q: The dividend rate of the asset.
    :type q: float
    :param sigma: Annualized volatility of the asset's returns. 
    :type sigma: float
    :param call_value: Takes input as "call", "put", "both"
    :type call_value: string
    :return: Price of the options
    :rtype: float. Returns a dictionary when call_value is set to "both"
    """
    d1 = (np.log(S/K) + (r - q + sigma**2/2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma* np.sqrt(T)
    Value = 0

    if(call_value=="both"):
        Value_put = K*np.exp(-r*T)*N(-d2) - S*np.exp(-q*T)*N(-d1)
        Value_call = S*np.exp(-q*T) * N(d1) - K * np.exp(-r*T)* N(d2)
        return {"put":Value_put, "call":Value_call}

    if (call_value=="call"):
        Value = S*np.exp(-q*T) * N(d1) - K * np.exp(-r*T)* N(d2)

    elif(call_value=="put"):
        Value = K*np.exp(-r*T)*N(-d2) - S*np.exp(-q*T)*N(-d1)

    return Value




