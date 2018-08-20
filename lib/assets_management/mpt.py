import numpy as np
import pandas as pd
import am_user_portfolio as amup
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

NUM_OF_ASSETS = 0
CUS_TICKER_LIST = []

##### helpers ##################################################################

def generate_random_weights(n):
    weights = np.random.rand(n)
    return np.asmatrix(weights/sum(weights))


def get_p_expected_return(weight_matrix, return_matrix):
    return float('{0:.5f}'.format(float(weight_matrix * return_matrix.T)*100))


def get_p_sigma(weight_matrix, var_cov_matrix):
    return float('{0:.5f}'.format(float(np.sqrt(weight_matrix * var_cov_matrix * weight_matrix.T))))


def generate_opportunity_set(return_matrix, var_cov_matrix):
    expected_return_arr = []
    sigma_arr = []
    for i in range(1000):
        weight_matrix = generate_random_weights(NUM_OF_ASSETS)
        expected_return_arr.append(get_p_expected_return(weight_matrix, return_matrix))
        sigma_arr.append(get_p_sigma(weight_matrix, var_cov_matrix))
    plot_portfolio(np.array(expected_return_arr), np.array(sigma_arr), return_matrix, var_cov_matrix)


def plot_portfolio(expected_return_arr, sigma_arr, return_matrix, var_cov_matrix):
    fig, ax = plt.subplots(1, 1, figsize=(15,15))
    ax.plot(sigma_arr, expected_return_arr, '.', markersize=5, label='Portfolio Opportunity Set')
    ax.xaxis.set_major_locator(MultipleLocator((sigma_arr.max()-sigma_arr.min())/5))

    text = 'The next period (day) expected return of each asset:\n'
    return_list = return_matrix.tolist()
    for i, r in enumerate(return_list[0]):
        text += '{} : {}%\n'.format(CUS_TICKER_LIST[i], str(r*100))
    text += '\nVariance-Covariance Matrix:\n'
    text += '{}'.format(var_cov_matrix)
    plt.text(1.6 , -0.1, text, size=20)

    ax.grid(True)
    ax.legend()
    ax.set_xlabel(r'$\sigma_p$')
    ax.set_ylabel(r'$E(r_p) (%)$')
    fig.tight_layout()
    fig.subplots_adjust(bottom=0.05)
    plt.show()


################################################################################

def optimize_portfolio():
    print("*******************************************************")
    print("Enter your client\'s id (number only):")
    cus_id = input()
    global CUS_TICKER_LIST
    CUS_TICKER_LIST = amup.get_client_tickers(cus_id)
    if CUS_TICKER_LIST == None or CUS_TICKER_LIST == []:
        print("Customer data not found!")
    print("\n")

    if CUS_TICKER_LIST != [] and CUS_TICKER_LIST != None:
        global NUM_OF_ASSETS
        NUM_OF_ASSETS = len(CUS_TICKER_LIST)
        closes = amup.get_closes(CUS_TICKER_LIST)
        return_matrix = amup.get_expected_returns(closes)
        var_cov_matrix = amup.get_var_cov_matrix(closes)
        generate_opportunity_set(return_matrix, var_cov_matrix)
