import re
import time
import requests
import pandas as pd
import module_path as mp
from selenium import webdriver
from bs4 import BeautifulSoup

SLEEP_TIME = 1
COLS = ['Date', 'Time', 'Link', 'Title', 'Content']
URL_HEAD = 'http://www.aastocks.com'

##### helpers ##################################################################

def check_time(new_datetime, latest_update):
    if latest_update == []:
        return False
    else:
        if new_datetime[0] < latest_update[0] or (new_datetime[0] == latest_update[0] and new_datetime[1] < latest_update[1]):
            return True
        elif new_datetime[0] == latest_update[0] and new_datetime[1] == latest_update[1]:
            return True
        else:
            return False


def print_progress(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')

    if iteration == total:
        print()


def parse_content(text):
    code_patt = re.compile(r'\([a-z]{2}/[a-z]{1,2}\)')
    soup = BeautifulSoup(text, 'lxml')
    try:
        soup.span.extract()
    except:
        pass
    try:
        soup.a.extract()
    except:
        pass
    sub_index = [i for i, char in enumerate(soup.text) if char == '。']
    if len(sub_index) > 0:
        content = soup.text[:sub_index[-1]+1]

        end_index = content.find('(報價延遲')
        if end_index == -1:
            pass
        else:
            content = content[:end_index]

        end_index = content.find('免責聲明：')
        if end_index == -1:
            pass
        else:
            content = content[:end_index]

        end_index = content.find('本文件由香港上海匯豐銀行有限公司')
        if end_index == -1:
            pass
        else:
            content = content[:end_index]

        end_index = content.find(' 阿思達克財經新聞網址: ')
        if end_index == -1:
            pass
        else:
            content = content[:end_index]

        has_code = code_patt.search(content)
        if has_code == None:
            pass
        else:
            content = content[:has_code.span()[0]]

        return content
    else:
        return ''


def get_content(df):
    print("Parsing {} news content...".format(len(df)))
    df['Content'] = ''
    if len(df) == 0:
        return df
    else:
        print_progress(0, len(df), prefix = 'Progress:', suffix = 'Complete', length = 50)
        for i, row in df.iterrows():
            page = requests.get(row.Link)
            time.sleep(SLEEP_TIME/2)
            if page.status_code == 200:
                print_progress(i+1, len(df), prefix = 'Progress:', suffix = 'Complete', length = 50)
                content = page.content.decode()
                start_index = content.find('<p>') + 3
                end_index = content.find('</p>', start_index)
                content = content[start_index:end_index]
                content = parse_content(content)
                if content == '':
                    df.loc[i, 'Content'] = 'No Content'
                else:
                    df.loc[i, 'Content'] = content
        return df


def parse_mega_data(text, latest_update):
    df = pd.DataFrame(columns=COLS[0:4])
    soup = BeautifulSoup(text, "lxml")
    for div in soup.find_all('div'):    # this would replicates the <a> tags
        # get date and time: e.g. [<div class="newstime4">2018/07/19 14:29</div>, <div class="newstime4"></div>]
        datetime_tag = div.find_all(name='div', attrs={'class': 'newstime4'})
        if len(datetime_tag) == 0:
            continue
        else:
            date, time = datetime_tag[0].get_text().split(' ')
            if check_time([date, time], latest_update):
                break
            for a in div.find_all('a'):
                link = URL_HEAD + a.attrs['href']
                if link in df.iloc[:,2].unique():      # handle the replicates created before
                    pass
                else:
                    title = a.attrs['title']
                    df.loc[len(df)] = [date, time, link, title]
    return df


def crawl_aastocks_news(latest_update):
    driver = webdriver.Chrome()
    driver.set_page_load_timeout(20)
    driver.get('http://www.aastocks.com/tc/stocks/news/aafn/latest-news')
    for j in range(3):                 # the larger the range, the more the news will be crawled
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)") # scroll to the bottom
        time.sleep(SLEEP_TIME)
    source_code = driver.page_source
    start_index = source_code.find('ref="NOW.') - 5
    end_index = source_code.find('正在加載', start_index) + 47
    if start_index > 0 and end_index > start_index:
        driver.quit()
        txt = source_code[start_index:end_index]
        return parse_mega_data(txt, latest_update)
    else:
        print('Cannot find any news!')


################################################################################

def get_aastocks_news():
    print("*******************************************************")
    try:
        old_df = pd.read_csv(mp.DIR_DATA_NEWS + 'aastocks_news.csv')
        latest_update = [str(old_df.loc[0, 'Date']), old_df.loc[0, 'Time']]
        print("The latest news is up to:", latest_update[0], latest_update[1])
    except:
        print("No existing data!")
        latest_update = []
    print("Fetching news updates from Aastocks.com...")

    new_df = crawl_aastocks_news(latest_update)
    new_df = get_content(new_df)
    if latest_update == []:
        pass
    else:
        print("Merging data...")
        new_df = new_df.append(old_df, ignore_index=True)

    print("Saving news...")
    new_df.to_csv(mp.DIR_DATA_NEWS + 'aastocks_news.csv', index=False, encoding='utf_8_sig')
    time.sleep(SLEEP_TIME)
    print("Done")
