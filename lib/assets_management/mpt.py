import numpy as np
import pandas as pd
import am_user_portfolio as amup
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from matplotlib.ticker import MultipleLocator

NUM_OF_ASSETS = 0
CUS_TICKER_LIST = []
RISK_FREE = 0

##### helpers ##################################################################

def generate_random_weights(n):
    weights = np.random.rand(n)
    return np.asmatrix(weights/sum(weights))


def sharpe_ratio(expected_return, sigma):
    return (expected_return - RISK_FREE) / sigma


def get_p_expected_return(weight_matrix, return_matrix):
    if type(weight_matrix) == type([]):
        weight_matrix = np.asmatrix(weight_matrix)
    return float('{0:.5f}'.format(float(weight_matrix * return_matrix.T)*100))


def get_p_sigma(weight_matrix, var_cov_matrix):
    if type(weight_matrix) == type([]):
        weight_matrix = np.asmatrix(weight_matrix)
    return float('{0:.5f}'.format(float(np.sqrt(weight_matrix * var_cov_matrix * weight_matrix.T))))


def target(x, return_matrix, var_cov_matrix):
    x = np.asmatrix(x)
    expected_return = get_p_expected_return(x, return_matrix)
    sigma = get_p_sigma(x, var_cov_matrix)
    #print((expected_return - RISK_FREE) / sigma)
    return -(expected_return - RISK_FREE) / sigma


#def find_efficient_frontier(return_matrix, var_cov_matrix, target_range):



def generate_opportunity_set(return_matrix, var_cov_matrix):
    expected_return_arr = []
    sigma_arr = []
    optimal_weights = []
    max_sharpe = optimal_sigma = optimal_return = 0
    for i in range(8888):
        weight_matrix = generate_random_weights(NUM_OF_ASSETS)
        r = get_p_expected_return(weight_matrix, return_matrix)
        sigma = get_p_sigma(weight_matrix, var_cov_matrix)
        s_r = sharpe_ratio(r, sigma)
        expected_return_arr.append(r)
        sigma_arr.append(sigma)
        if s_r > max_sharpe:
            max_sharpe = s_r
            optimal_sigma = sigma
            optimal_return = r
            optimal_weights = weight_matrix.tolist()[0]
    return (np.array(expected_return_arr), np.array(sigma_arr), max_sharpe, optimal_return, optimal_sigma, optimal_weights)


'''
def optimize_CAL(return_matrix, var_cov_matrix):
    num_assets = return_matrix.size
    #x = np.zeros(return_matrix.size)
    cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0.0, 1.0) for i in range(num_assets))       # passing bounds causes error

    optimal_weights = minimize(target, num_assets*[1./num_assets,], args=(return_matrix, var_cov_matrix,), method='SLSQP', bounds=bounds, constraints=cons)
    #optimal_return = get_p_expected_return(optimal_weights, return_matrix)
    #optimal_sharpe = get_p_sigma(optimal_weights, var_cov_matrix)
    print(optimal_weights.x)

    optimal_weights = []
    optimal_return = optimal_sigma = optimal_sharpe = 0
    for i in range(len(x)):
        x[i] = 1
        weights = np.asmatrix(minimize(target, x, args=(return_matrix, var_cov_matrix,), method='SLSQP', constraints=cons, options={'maxiter': 10000, 'disp': True}).x)
        w_return = get_p_expected_return(weights, return_matrix)
        sigma = get_p_sigma(weights, var_cov_matrix)
        sharpe = sharpe_ratio(w_return, sigma)
        if sharpe > optimal_sharpe:
            optimal_weights = weights
            optimal_return = w_return
            optimal_sigma = sigma
        x[i] = 0
    x = np.ones(return_matrix.size)
    weights = np.asmatrix(minimize(target, x, args=(return_matrix, var_cov_matrix,), method='SLSQP', constraints=cons, options={'maxiter': 10000, 'disp': True}).x)
    w_return = get_p_expected_return(weights, return_matrix)
    sigma = get_p_sigma(weights, var_cov_matrix)
    sharpe = sharpe_ratio(w_return, sigma)
    if sharpe > optimal_sharpe:
        optimal_weights = weights
        optimal_return = w_return
        optimal_sigma = sigma

    #return (optimal_weights.tolist()[0], optimal_return, optimal_sigma)
'''


def plot_portfolio(expected_return_arr, sigma_arr, return_matrix, var_cov_matrix, optimal_weights, optimal_return, optimal_sigma, max_sharpe):
    fig, ax = plt.subplots(1, 1, figsize=(15,15))
    plt.suptitle('Portfolio Optimization', fontsize = 20, fontweight='bold')
    #eff_fron_return, eff_fron_sigma = find_efficient_frontier(expected_return_arr, sigma_arr)

    # plot portfolio opportunity set
    ax.plot(sigma_arr, expected_return_arr, 'o', markersize=8, label='Portfolio Opportunity Set', zorder=5)
    # plot CAL
    extend_x = 3.0
    extend_y = RISK_FREE + extend_x * (optimal_return - RISK_FREE) / optimal_sigma
    ax.plot([0, optimal_sigma, extend_x], [RISK_FREE, optimal_return, extend_y], label='CAL', color='red', zorder=6)
    # plot markers
    ax.scatter([0, optimal_sigma], [RISK_FREE, optimal_return], c='black', marker='x', s=[15**2], zorder=7)
    asset_returns = (np.asarray(return_matrix)*100).tolist()[0]
    asset_sigmas = [np.sqrt(var_cov_matrix[i,i]) for i in range(len(var_cov_matrix))]
    ax.scatter(asset_sigmas, asset_returns, c='black', marker='x', s=[15**2], zorder=7)

    text = 'The next period (3-month) expected return of each asset:\n'
    return_list = return_matrix.tolist()[0]
    for i, r in enumerate(return_list):
        text += '{} : {}%\n'.format(CUS_TICKER_LIST[i], str(r*100))
    text += '\nVariance-Covariance Matrix:\n'
    text += '{}'.format(var_cov_matrix)
    plt.text(1.4 , -6, text, size=15)
    text = 'Risk-Free Rate\n'
    text += str(RISK_FREE)
    plt.text(0 , RISK_FREE-1.5, text, size=15)
    text = 'Optimal Risky Portfolio\n'
    for idx, tk in enumerate(CUS_TICKER_LIST):
        text += tk + ': ' + str(optimal_weights[idx]*100) + '%\n'
        plt.text(asset_sigmas[idx]-0.2 , asset_returns[idx], tk, size=15, zorder=7)
    text += 'Maximum Sharpe Ratio: ' + str(max_sharpe)
    plt.text(optimal_sigma+0.05 , optimal_return-1, text, size=15, zorder=7)


    ax.xaxis.set_major_locator(MultipleLocator((sigma_arr.max()-sigma_arr.min())/5))
    ax.set_xlabel(r'$\sigma_p$')
    ax.set_ylabel(r'$E(r_p)\ (\%)$')
    ax.grid(True, zorder=0)
    ax.legend()
    fig.tight_layout()
    fig.subplots_adjust(bottom=0.05, top=0.95)
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
        global NUM_OF_ASSETS, RISK_FREE
        NUM_OF_ASSETS = len(CUS_TICKER_LIST)
        closes = amup.get_closes(CUS_TICKER_LIST)
        print("Getting 13-weeks risk-free rate from the U.S. Treasury Department...")
        RISK_FREE = amup.get_risk_free_rate()
        return_matrix = amup.get_expected_returns(closes)
        var_cov_matrix = amup.get_var_cov_matrix(closes)

        print("Generating customer's random portfolio...")
        expected_return_arr, sigma_arr, max_sharpe, optimal_return, optimal_sigma, optimal_weights = generate_opportunity_set(return_matrix, var_cov_matrix)

        #print("Genreating the efficient frontier...")
        #target_range = np.linspace(expected_return_arr[np.argmin(sigma_arr)], expected_return_arr[np.argmax(sigma_arr)], 100)
        #efficients = find_efficient_frontier(return_matrix, var_cov_matrix, target_range)

        print("Optimizing Capital Allocation Line...")
        #optimize_CAL(return_matrix, var_cov_matrix)
        #optimal_weights, optimal_return, optimal_sigma = optimize_CAL(return_matrix, var_cov_matrix)

        plot_portfolio(expected_return_arr, sigma_arr, return_matrix, var_cov_matrix, optimal_weights, optimal_return, optimal_sigma, max_sharpe)
        print("Done \n")
