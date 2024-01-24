import pandas as pd
import numpy as np 

interest_rates_years=[0.1,0.1,0.1]
cash_flows_years=[-100,5,10]
# must be of the same length

def compute_NPV(cash_flows_years,interest_rates_years): 
    T=len(interest_rates_years)
    if T!=len(cash_flows_years):
        npv=np.nan
        return npv
    else:
        npv=0
        for t in range(T):
            npv=npv+cash_flows_years[t]/((1+interest_rates_years[t])**t)
        return npv

npv=compute_NPV(cash_flows_years,interest_rates_years) 