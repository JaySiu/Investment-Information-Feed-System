import pandas as pd
import am_user_portfolio as amup







def optimize_portfolio():
    print("*******************************************************")
    print("Enter your client\'s id (number only):")
    cus_id = input()
    cus_ticker_list = amup.get_client_tickers(cus_id)
    if cus_ticker_list == None or cus_ticker_list == []:
        print("Customer data not found!")
        cus_ticker_list = []
    print("\n")

    if cus_ticker_list != []:
        closes = amup.get_closes(cus_ticker_list)
        expected_returns = amup.get_expected_returns(closes)
        var_cov_matrix = amup.get_var_cov_matrix(closes)
