import logging
import time
import requests
import datetime
import pytz

# Telegram Bot Tokens
TOKEN = "6085709930:AAFGkBMD5ZXTYR9gx0vp-TGtYcwf7QRbNOY"
chat_id = "577013487"

# For logging into a file
logging.basicConfig(filename="main_log.log",format='%(asctime)s %(message)s',filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

g = 0
i = 1
while g == 0:

    # For calcuating the program execution time
    start1 = time.time()
    
    # Generate random query/params to help prevent caching
    queries = ["catalogId=48","type=1","pageNo=1",f"pageSize={str(i)}"]
    request_url = (f"https://www.binance.com/gateway-api/v1/public/cms/article/list/query"f"?{queries[0]}&{queries[1]}&{queries[2]}&{queries[3]}")
    logger.info(request_url)
    latest_announcement = requests.get(request_url)

    # Checking if site is working or not
    if latest_announcement.status_code == 200:
        # Checking if cached or not
        if latest_announcement.headers["X-Cache"] == 'Miss from cloudfront':
            latest_announcement = latest_announcement.json()
            news = latest_announcement["data"]["catalogs"][0]["articles"][0]["title"]
            date = latest_announcement["data"]["catalogs"][0]["articles"][0]["releaseDate"]
            logger.info(news)
            i = i + 1
            while (i > 50):
                i = 1                    
        else:
            i = 1
            logger.info(latest_announcement.headers["X-Cache"])        
            logger.info('Sleeping due to Caching')    
            tele_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text=Sleeping due to Caching"
            requests.get(tele_url).json()        
            time.sleep(30)                              
    else:
        print('Sleeping. Error Code: ',latest_announcement.status_code)
        tele_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text=Sleeping. IP Ban(429) or check log"
        requests.get(tele_url).json()
        time.sleep(30)
    
    nf = open('NEWS.txt', 'r', encoding="utf-8")
    news_file = nf.read()
    nf.close()
    
    if news not in news_file:

        tele_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={news}"
        requests.get(tele_url).json()

        n = open('NEWS.txt', 'a', encoding="utf-8")    
        n.write(news + '\n')
        n.close()
        
        # News Unix date to regular date format
        dt = datetime.datetime.fromtimestamp(date / 1000)
        formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        tele_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={formatted_time}"
        requests.get(tele_url).json()
        d = open('DATE.txt', 'a', encoding="utf-8")    
        d.write(formatted_time + '\n')
        d.close()

        # Syatem date to regular date format
        sys_time = str(datetime.datetime.now(pytz.timezone('Asia/Kolkata')))
        tele_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={sys_time}"
        requests.get(tele_url).json()
        sd = open('SYSTEM_TIME.txt', 'w', encoding="utf-8")
        sd.write(sys_time)
        sd.close()        
        
        if 'Binance Will List' in news:

            # Extract only the coin Symbol
            start = '('
            end = ')'
            coin = news[news.find(start)+len(start):news.rfind(end)]

            cf = open('COIN.txt', 'r', encoding="utf-8")
            coin_file = cf.read()
            cf.close()

            if coin not in coin_file:
                tele_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={coin}"
                requests.get(tele_url).json()

                c = open('COIN.txt', 'a', encoding="utf-8")    
                c.write(coin + '\n')
                c.close()

                logger.info('Buying Script Executed')
                tele_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text=New coin Listed"
                requests.get(tele_url).json()
            else:
                logger.info('Check Code')

    time.sleep(3.3)
    # For calcuating the program execution time
    end1 = time.time()
    total_time = end1 - start1
    logger.info(str(total_time))               
