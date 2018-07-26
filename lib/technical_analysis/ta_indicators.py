'''
RMs can select different indicators for doing the technical analysis
for the clients
'''

import time
from macd import macd

indicators = {'1': 'MACD', '2':'RSI', '3': 'B-Bands', '4': 'KD', '5':'KDJ'}

def analyze():
    print("*******************************************************")
    print("Enter your client\'s id:")
    id = input()
    print("*******************************************************")
    print("Select indicators:(choices separated by \',\')")
    keys = list(indicators.keys())
    keys.sort()
    for k in keys:
        print("{}) {}".format(k, indicators.get(k)))
    choices = input().split(',')
    if len(choices) > len(indicators) or len(list(set(choices)-set(indicators.keys()))) > 0:
        print("Invalid input!")
    else:
        for c in choices:
            c = c.strip()
            if indicators[c] == 'MACD':
                macd()
            elif indicators[c] == 'RSI':
                print('RSI')
            elif indicators[c] == 'BBAND':
                print('BBAND')


if __name__ == '__main__':
    analyze()
