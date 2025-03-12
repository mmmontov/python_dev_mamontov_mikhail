import pandas as pd
from pandas.core.frame import DataFrame

from src.database.authors_database import authors_sync_engine
from src.database.logs_database import logging_sync_engine


def create_comments_dataset(login: str, to_json: bool = False) -> list[dict] | DataFrame:
    # данные из authors
    posts = pd.read_sql_query("SELECT id, header, author_id FROM post", authors_sync_engine)
    authors = pd.read_sql_query(f"SELECT id, login FROM user ", authors_sync_engine)

    # данные из logging
    logs = pd.read_sql_query("SELECT id, user_id, event_type_id, space_type_id, entity_id FROM logs", logging_sync_engine)
    event_type = pd.read_sql_query("SELECT * FROM event_type", logging_sync_engine)
    space_type = pd.read_sql_query("SELECT * FROM space_type", logging_sync_engine)

    # объединение таблиц logging
    logs = logs.merge(event_type, left_on='event_type_id', right_on='id', suffixes=('', '_et'))
    logs = logs.merge(space_type, left_on='space_type_id', right_on='id', suffixes=('', '_st'))

    # фильтрация по comment
    logs = logs[(logs['name'] == 'comment') & (logs['name_st'] == 'post')]
    
    # добавление логина комментатора поста
    df_comments = logs.merge(authors, left_on='user_id', right_on='id', suffixes=('', '_commenter'))
    df_comments = df_comments[(df_comments['login'] == login)]
    df_comments.rename(columns={'login': 'commenter_login'}, inplace=True)

    # добавление автора поста
    df_comments = df_comments.merge(posts, left_on='entity_id', right_on='id', suffixes=('', '_post'))
    df_comments = df_comments.merge(authors, left_on='author_id', right_on='id', suffixes=('', '_post_author'))
    df_comments.rename(columns={'login': 'post_author_login'}, inplace=True)
    
    # группировка датасета
    dataset = df_comments.groupby(['commenter_login',  'header', 'post_author_login']).size().reset_index(name='comment_count')

    if to_json:
        dataset = dataset.to_dict(orient='records')
        return dataset
    else:
        return dataset
    
    
def create_general_dataset(login: str, to_json: bool = False) -> list[dict] | DataFrame:
    # данные из authors
    authors = pd.read_sql_query(f"SELECT id, login FROM user ", authors_sync_engine)
    
    # данные из logging
    logs = pd.read_sql_query('SELECT datetime, user_id, event_type_id, space_type_id FROM logs', logging_sync_engine)
    event_type = pd.read_sql_query("SELECT * FROM event_type", logging_sync_engine)
    space_type = pd.read_sql_query("SELECT * FROM space_type", logging_sync_engine)
    
    # объединение таблиц logging
    logs = logs.merge(event_type, left_on='event_type_id', right_on='id', suffixes=('', '_et'))
    logs.rename(columns={'id': 'id_et', 'name': 'name_et'}, inplace=True)
    logs = logs.merge(space_type, left_on='space_type_id', right_on='id', suffixes=('', '_st'))
    logs.rename(columns={'id': 'id_st', 'name': 'name_st'}, inplace=True)
    
    # объединение таблицы с authors
    df_general = logs.merge(authors, left_on='user_id', right_on='id', suffixes=('', '_user'))
    df_general = df_general[(df_general['login'] == login)]
    
    try:
        # перевод datetime к date
        df_general['datetime'] = pd.to_datetime(df_general['datetime'])
        df_general['date'] = df_general['datetime'].dt.date
    except:
        raise ValueError('Incorrect datetime format')
    
    # определение действий в виде true или false
    df_general['is_login'] = ((df_general['name_et'] == 'login') & (df_general['name_st'] == 'global')).astype(int)
    df_general['is_logout'] = ((df_general['name_et'] == 'logout') & (df_general['name_st'] == 'global')).astype(int)
    df_general['is_blog_action'] = ((df_general['name_st'] == 'blog')).astype(int)
    # return df_general.head()
    dataset = df_general.groupby('date').agg({
        'is_login': 'sum',
        'is_logout': 'sum',
        'is_blog_action': 'sum'
    }).reset_index()
    
    dataset.rename(columns={
        'is_login': 'login_count',
        'is_logout': 'logout_count',
        'is_blog_action': 'blog_action_count'
    }, inplace=True)
    
    if to_json:
        dataset['date'] = dataset['date'].apply(lambda x: int(pd.Timestamp(x).timestamp() * 1000))
        dataset = dataset.to_dict(orient='records')
        return dataset
    else:
        return dataset
