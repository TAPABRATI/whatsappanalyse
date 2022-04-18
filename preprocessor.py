import re
import pandas as pd

def preprocess(data):
    pattern = "\d{2}[/-]\d{2}[/-]\d{2}[,]\s\d{1}[:]\d{2}\s[am,pm]{2}\s[-]\s"

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    date = list(map((lambda a: a.strip(" - ")), dates))
    df = pd.DataFrame({'user_message': messages, 'message_date': date})
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M %p')
    user = []
    messages = []
    pat = '([\w\W]+?):\s'
    for message in df['user_message']:
        entry = re.split(pat, message)
        if entry[1:]:
            user.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            user.append('group_notification')
            messages.append(entry[0])
    df['user'] = user
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['only_date'] = df['message_date'].dt.date
    df['Year'] = df['message_date'].dt.year
    df['Month'] = df['message_date'].dt.month_name()
    df['Month_num'] = df['message_date'].dt.month
    df['Day'] = df['message_date'].dt.day
    df['Day_name'] = df['message_date'].dt.day_name()
    df['Hour'] = df['message_date'].dt.hour
    df['Minute'] = df['message_date'].dt.minute

    period = []
    for hour in df[['Day_name', 'Hour']]['Hour']:
        if hour == 23:
            period.append(str(hour) + '-' + str('00'))
        elif hour == 0:
            period.append(str('00') + '-' + str(hour + 1))
        else:
            period.append(str(hour) + '-' + str(hour + 1))
    df['Period'] = period

    return df