import ta_user_portfolio as taup

##### helpers ##################################################################

#def portfolio_news_mapping(portfolio, news_source):














################################################################################

def analyze_news():
    print("*******************************************************")
    print("Enter your client\'s id (number only):")
    cus_id = input()
    cus_ticker_list = taup.get_client_tickers(cus_id)
    if cus_ticker_list == None or cus_ticker_list == []:
        print("Customer data not found!")
        cus_ticker_list = []

    #if cus_ticker_list != []:
    #    portfolio_news_mapping(cus_ticker_list, 'aastocks')
