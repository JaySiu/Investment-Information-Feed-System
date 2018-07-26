'''
Entry point of the investment information feed system

Dependent-modules/packages:
    - Anaconda Python
    - talib: $conda install -c quantopian ta-lib
    - selenium: $conda install -c anaconda selenium
    - fix_yahoo_finance: $pip install fix_yahoo_finance --upgrade --no-cache-dir
    - chromeDriver:
        macOS: place it in /usr/local/table_index
        Windows: put it under the ~main.py~'s directory

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
        ope = ''
        while ope != 'q':
            print("*******************************************************")
            print("To quit: type 'q'")
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
            elif ope == 'q':
                break
            else:
                print("Please enter a valid input")
