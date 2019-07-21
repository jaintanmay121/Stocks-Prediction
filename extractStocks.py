import bs4
from urllib import request as req
import pandas as pd
import numpy as np
import datetime
import intrinio_sdk
from intrinio_sdk.rest import ApiException


api=""  #Enter your API key from Intrino here

intrinio_sdk.ApiClient().configuration.api_key['api_key'] = api
security_api = intrinio_sdk.SecurityApi()
company_api = intrinio_sdk.CompanyApi()

def stocksData(stock, startDate):
    identifier = stock # str | A Security identifier (Ticker, FIGI, ISIN, CUSIP, Intrinio ID)
    start_date = startDate # date | Return prices on or after the date (optional)
    end_date = datetime.datetime.now() # date | Return prices on or before the date (optional)
    frequency = 'monthly' # str | Return stock prices in the given frequency (optional) (default to daily)
    page_size = 100 # int | The number of results to return (optional) (default to 100)
    next_page = '' # str | Gets the next page of data from a previous API call (optional)

    api_response = security_api.get_security_stock_prices(identifier, start_date=start_date, end_date = end_date, frequency=frequency, page_size=page_size, next_page=next_page)

    date=[]
    op=[]
    cl=[]
    high=[]
    low=[]
    for i in range(len(api_response.stock_prices_dict)):
        date.append(api_response.stock_prices_dict[i]['date'])
        op.append(api_response.stock_prices_dict[i]['open'])
        cl.append(api_response.stock_prices_dict[i]['close'])
        high.append(api_response.stock_prices_dict[i]['high'])
        low.append(api_response.stock_prices_dict[i]['low'])

    l=[date,op,cl,high,low]
    df=pd.DataFrame(l).T
    df.columns=['Date','Open','Close','High','Low']
    df

    df.to_csv('teststocks.csv',index=False)
    
def showComp():
    api_response = company_api.get_all_companies( page_size=5000)
    for i in range(len(api_response.companies)):
        print(f"{api_response.companies_dict[i]['name']}: {api_response.companies_dict[i]['ticker']}")