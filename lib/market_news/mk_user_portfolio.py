import stock
import pandas as pd
import module_path as mp

'''
return a list of a client's stocks
(tickers with no yahoo finance data NOT removed)
'''
def get_client_tickers(cus_id):
    id = 'scb_' + cus_id
    customers_df = pd.read_csv(mp.DIR_DATA_CUSTOMERS + 'customer_trade_book.csv')
    customers_df = customers_df[['ID', 'Symbol', 'Portfolio_Value']]
    customers_df = customers_df[customers_df.ID == id]
    customers_df = customers_df[customers_df.Portfolio_Value > 0]
    ticker_list = list(set(customers_df['Symbol']))
    if len(ticker_list) > 0:
        ticker_list = [(4-len(str(tk)))*'0' + str(tk) +'.HK' for tk in ticker_list]
        print("Customer {} has the following equities in his/her portfolio:".format(id))
        for i, tk in enumerate(ticker_list):
            found = stock.check_all_ticker(tk)
            if found[1] == True:
                print(str(i+1) + ')', tk + ' - ' + found[0])
            else:
                print(str(i+1) + ')', found[0])
        print("\n")
        return ticker_list
    else:
        return None
