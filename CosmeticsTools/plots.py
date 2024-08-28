# import libraries
import pandas as pd
import seaborn as sns
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
plt.style.use('ggplot')
from matplotlib.pyplot import figure
    
def event_type_dist(df):
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='event_type')
    plt.title('Event Type Distribution')
    plt.xlabel('Event Type')
    plt.ylabel('Count')
    plt.show()
    df['event_type'].value_counts()
    
def transaction_count_by_brand(df, top):
    temp = df[df['event_type']=='purchase'].groupby('brand')['event_type'].count().sort_values(ascending=False).head(top)
    plt.figure(figsize=(10, 6))
    temp.plot(kind='bar')
    plt.title('Top 10 Brands (excluding Unknown)')
    plt.xlabel('Brand')
    plt.ylabel('Count')
    plt.show()
    return temp
    
def general_metrics(df):
    avg_transaction_per_session = np.sum(df[df['event_type']=='purchase'].groupby('user_session')['price'].sum())/df['user_session'].nunique()
    real_bounce_rate = np.mean(df.groupby('user_session')['event_type'].apply(','.join)=='view')
    return pd.DataFrame({'metric': ['Avg Transaction per Session', 'Real Bounce Rate'], 'value': [avg_transaction_per_session, real_bounce_rate]})

def average_transaction_by_brand(df, top):
    temp = df[df['event_type']=='purchase'].groupby(['user_session', 'brand'])['price'].sum().reset_index()
    avg_trans = temp.groupby('brand')['price'].sum()/temp.groupby('brand')['user_session'].nunique()
    plt.figure(figsize=(10, 6))
    avg_trans.sort_values(ascending=False).head(top).plot(kind='bar')
    plt.title('Average transaction per session by brand')
    plt.xlabel('Brand')
    plt.ylabel('Average transaction')
    plt.show()

def num_users_by_day_weekday(df):
    plt.figure(figsize=(10, 6))
    df.groupby('event_date')['user_id'].nunique().plot(kind='bar')
    plt.title('Unique Users by Day')
    plt.xlabel('Day')
    plt.ylabel('Number of Unique Users')
    plt.show()
    
    df['weekday'] = pd.to_datetime(df['event_date']).dt.weekday
    plt.figure(figsize=(10, 6))
    df.groupby('weekday')['user_id'].nunique().plot(kind='bar')
    plt.title('Unique Users by Weekday')
    plt.xlabel('Weekday')
    plt.ylabel('Number of Unique Users')
    plt.show()
    
def conversion_rate(df):
    event_step = {'view': 1, 'cart': 2,'purchase': 3}
    df['step'] = df['event_type'].map(event_step)

    max_step = df.groupby(['user_id', 'product_id'])['step'].max().reset_index()

    view_users = max_step[max_step['step'] >= 1]['user_id'].nunique()
    cart_users = max_step[max_step['step'] >= 2]['user_id'].nunique()
    purchase_users = max_step[max_step['step'] >= 3]['user_id'].nunique()

    funnel = pd.DataFrame({
        'Stage': ['View', 'Cart', 'Purchase'],
        'Users': [view_users, cart_users, purchase_users]
    })

    funnel['Conversion Rate'] = funnel['Users']/funnel['Users'].shift(1)
    funnel.iloc[0,2]=1
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=funnel, x='Stage', y='Users')
    plt.title('Funnel Analysis: Number of Users at Each Stage')
    plt.xlabel('Stage')
    plt.ylabel('Number of Users')
    plt.show()

    plt.figure(figsize=(10, 6))
    sns.lineplot(x='Stage', y='Conversion Rate', data=funnel, marker='o')
    plt.title('Funnel Analysis: Conversion Rate at Each Stage')
    plt.xlabel('Stage')
    plt.ylabel('Conversion Rate (%)')
    plt.show()
    return funnel