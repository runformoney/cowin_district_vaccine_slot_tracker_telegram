from dotenv import load_dotenv
import os, sys

try:
    load_dotenv('config/ENV')
except:
    sys.exit("Create a file 'ENV' in config directory and add the Telegram BOT_TOKEN and CHAT_ID.")

TELEGRAM_ROOT = 'https://api.telegram.org/bot'
TELEGRAM_END_POINT = '/sendMessage'
try:
    BOT_TOKEN = os.environ["BOT_TOKEN"]
    CHAT_ID = os.environ["CHAT_ID"]
except:
    sys.exit("BOT_TOKEN or CHAT_ID missing in ENV.")
TELEGRAM_URL = TELEGRAM_ROOT + BOT_TOKEN + TELEGRAM_END_POINT


""""
The DIST_ID can be found inside utils/district_mapping.csv
A district might have too many centers that are far away. So filtering with respect to pincodes would be better.
Provide a list of pincodes nearer to you in PIN_CODE_LIST. Get it from Cowin website.
"""
DIST_ID = 457  # Cuttack
PIN_CODE_LIST = []
PIN_CODE_LIST = [753008, 753001, 753007, 753014]


SEP = "\t"

COWIN_URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}"
COWIN_HEADERS = {
    'User-Agent': "User-Agent:Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
EXCLUDE_LOCATIONS = ['Odiyabazar UPHC (18-44)', 'Thoria Sahi UPHC (18-44)', 'UCHC CDA 18-44', 'MANJULATA UPHC (18-44)']
# EXCLUDE_LOCATIONS = []
