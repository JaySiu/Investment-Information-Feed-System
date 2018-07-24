'''
Entry point of the investment information feed system

Dependent-modules/packages:
    - Anaconda Python
    -
'''

import sys
import module_path as mp
sys.path.append(mp.dir_ta)

from ta_indicators import analyze

if __name__ == '__main__':
    print("Welcome to the investment information feed(iif) system!")
    print("*******************************************************")
    print("Please select your identity:")
    print("1) RM")
    print("2) client")
    iden = input()
    if iden == '1':
        while True:
            print("*******************************************************")
            print("Choose an operation:")
            print("1) Assets Management")
            print("2) Technical Analysis")
            print("3) Market News")
            ope = input()
            if ope == '1':
                print('1')
            elif ope == '2':
                analyze()
            elif ope == '3':
                print('3')
            else:
                print("Please enter a valid input")
