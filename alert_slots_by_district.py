import datetime
import pandas as pd
from pypac import PACSession
import time
import beepy as beep
from pytelegram import send_message
from config.config import COWIN_URL, PIN_CODE_LIST, DIST_ID, COWIN_HEADERS, EXCLUDE_LOCATIONS

pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 1000)

def alert(text=None):
    if text:
        for _ in range(20):
            beep.beep(5)
        print('Waiting 4 minutes. Snoozing.')
        time.sleep(4 * 60)
        print("Starting again.")
    else:
        while True:
            beep.beep(7)

def get_texts(df):
    styles = {18: "Age Group 18-44:\n",
              45: "Age Group 45+:\n"}
    texts = []
    df.date = pd.to_datetime(df.date).dt.strftime('%d-%m')
    for age_group in [18, 45]:
        text = styles[age_group]
        data = df[df.min_age_limit == age_group]
        ind = 1
        for index, groupby_df in data.groupby('center_name'):
            text = text + str(ind) + ". " + index + " (" + str(groupby_df.pin_code.iloc[0]) + ")" + ":\n"
            for i, row in groupby_df.iterrows():
                text = text + str(row.available_capacity_dose1) + " slots on " + str(row.date) + "\n"
            ind += 1
            text = text + '\n'
        if styles[age_group] != text:
            texts.append(text)
    return texts

def run_process():
    iteration = 0
    while (True):
        base = datetime.datetime.today()
        start_date = base.strftime("%d-%m-%Y")
        url = COWIN_URL.format(DIST_ID, start_date)
        session = PACSession()
        response = session.get(url, headers=COWIN_HEADERS)
        if response.ok:
            resp_json = response.json()
            df = pd.DataFrame()
            i = 0
            for center in resp_json["centers"]:
                for session in center["sessions"]:
                    if center["name"] not in EXCLUDE_LOCATIONS:
                        df.at[i, "center_name"] = center["name"]
                        df.at[i, "pin_code"] = int(center["pincode"])
                        df.at[i, "available_capacity_dose1"] = session['available_capacity_dose1']
                        df.at[i, "min_age_limit"] = session["min_age_limit"]
                        df.at[i, 'date'] = session['date']
                        df.at[i, 'fee_type'] = center['fee_type']
                        i += 1
            df.pin_code = df.pin_code.astype(int)
            df.available_capacity_dose1 = df.available_capacity_dose1.astype(int)
            df.min_age_limit = df.min_age_limit.astype(int)
            if PIN_CODE_LIST:
                df = df[df.pin_code.isin(PIN_CODE_LIST)]
            df = df[(df.available_capacity_dose1 > 0)]
            # df = df[df.fee_type == 'Free']
            if df.shape[0]:
                print(df)
                texts = get_texts(df)
                for text in texts:
                    send_message(text)
                    # print(text)
                alert('successful')


        if response.status_code in [404, 403, 500, 400]:
            alert()

        if iteration % 50 == 0:
            print(iteration)
        time.sleep(10)
        iteration += 1


if __name__ == '__main__':
    run_process()
