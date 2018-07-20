'''
Entry point of the investment information feed system
'''

import sys
import module_path as mp
sys.path.append(mp.dir_ta)

from ta_indicators import analyze

def select_operation(i):
    {'1': 'hi', '2': analyze(), '3': 'he'}.get(i)

if __name__ == "__main__":
    print('Welcome to the investment information feed(iif) system!')
    print('*******************************************************')
    print('Please select your identity:')
    print('1) RM')
    print('2) client')
    iden = input()
    if iden == '1':
        print('*******************************************************')
        print('Choose an operation:')
        print('1) Assets Management')
        print('2) Technical Analysis')
        print('3) Market News')
        select_operation(input())
