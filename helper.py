from urlextract import URLExtract
import nltk
from nltk.corpus import stopwords
import pandas as pd
from collections import Counter
import emoji

#from wordcloud import WordCloud
extract = URLExtract()

def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    # else
    # 1. fetch number os messages
    num_messages = df.shape[0]

    # 2. fetch number of words
    words = []
    for i in df['message']:
        words.extend(i.split())

    # 3.fetch number of media messages
    num_media_messages = df[df['message'] == "<Media omitted>\n"].shape[0]

    # 4.fetch number of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages,len(links)


def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name/number','user':'percent'})
    return x,df

# def create_wordcloud(selected_user,df):
#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]
#
#     wc = WordCloud(width=500, height=500, min_font_size=10, background_color='black')
#     df_wc = wc.generate(df[df['message'] == selected_user].str.cat(sep = " "))
#     return df_wc

def most_common_words(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    stop = ['-', 'pm', '+91', '👍🏻', '<media', 'omitted', '23/02/22,', 'am', 'omitted> ', 'joshi(data', '(data']

    stops = set(stopwords.words('english'))
    words1 = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stops:
                if word not in stop:
                    words1.append(word)

    most_common_df = pd.DataFrame(Counter(words1).most_common(20))
    return most_common_df

def emoji_count(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['Year', 'Month_num', 'Month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i] + "-" + str(timeline['Year'][i]))
    timeline['time'] = time
    return  timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['Day_name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['Month'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    user_heatmap = df.pivot_table(index='Day_name', columns='Period', values='message', aggfunc='count').fillna(0)

    return user_heatmap

    # if selected_user == 'Overall':
    #     # 1. fetch number os messages
    #     num_messages = df.shape[0]
    #     # 2. fetch number of words
    #     words = []
    #     for i in df['message']:
    #         words.extend(i.split())
    #     return num_messages,len(words)
    # else:
    #     new_df = df[df['user'] == selected_user]
    #     num_messages = new_df.shape[0]
    #     words = []
    #     for i in df['message']:
    #         words.extend(i.split())
    #     return num_messages,len(words)
