from pymongo import MongoClient
import pandas as pd
from pathlib import Path
import sqlite3
import json
import sys

# sys.path.append('C:/Users/ylwhd/section-3-project/my_app/mylibrary')
from get_myplaylist_api import GetMyPlaylistTracks


class MyTracksInfoList():
    def __init__(self, username:str, playlist_id:str, liked:int):
        """
        Args:
            username (str): playlist의 유저명(본인의 유저명이 아닙니다!)
            playlist_id (str): https://open.spotify.com/playlist/{여기에 있는 값입니다.}?si=19b9132dd5ce4870
            liked (int): 좋아하는 곡들의 리스트면 1, 그렇지 않으면 0 
        """
        self.username = username
        self.playlist_id = playlist_id
        self.liked = liked

    def get_info(self):
        """

        Returns:
            트랙의 정보 리스트가 list형태, dataframe형태 두개로 반환됩니다.
        """

        my_playlist = GetMyPlaylistTracks(username=self.username, playlist_id=self.playlist_id, liked=self.liked)
        tracks = my_playlist.get_playlist_tracks()
        # 각 노래 정보가 dict의 list 형태로 저장되어있음
        tracks_info_list = [my_playlist.get_features(tracks[i][2]) for i in range(len(tracks))]

        dataframe = pd.DataFrame(tracks_info_list).drop_duplicates(['id'], keep='first').reset_index(drop=True)
        
        return tracks_info_list, dataframe


class Mongo():
    def __init__(self):
        pass

    def connect_info(self, HOST='cluster0.abl5f.mongodb.net', USER='project_3rd', PASSWORD='p333', DATABASE_NAME='Section3Project'):

        MONGO_URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"
        # &ssl=true&ssl_cert_reqs=CERT_NONE : ServerSelectionTimeoutError 해결
        
        return DATABASE_NAME, MONGO_URI


class MongoCollection(Mongo):
    def __init__(self):
        pass

    def your_collection(self, your_name):
        """
        DB와 콜렉션을 반환합니다.
        """
        COLLECTION_NAME = f'{your_name}_collection'
        DATABASE_NAME, MONGO_URI = super().connect_info()

        client = MongoClient(MONGO_URI)
        database = client[DATABASE_NAME]
        collection = database[COLLECTION_NAME]

        return database, collection


class Features:
    def __init__(self) -> None:
        pass

    def featrues_col(self):
        features_col = ['mode',
                        'energy',
                        'key',
                        'speechiness',
                        'danceability',
                        'valence',
                        'liveness',
                        'time_signature',
                        'duration_ms',
                        'acousticness',
                        'loudness',
                        'tempo',
                        'instrumentalness']
        return features_col

    def target_col(self):
        target_col = 'liked'
        return target_col

    def total_features(self):
        total_features = ['liked',
                        'mode',
                        'energy',
                        'key',
                        'speechiness',
                        'danceability',
                        'valence',
                        'liveness',
                        'time_signature',
                        'duration_ms',
                        'acousticness',
                        'loudness',
                        'tempo',
                        'instrumentalness']
        return total_features


class SaveToMongoDB(MongoCollection, MyTracksInfoList):

    def __init__(self, your_name, username, playlist_id, liked):
        super().__init__()
        self.your_name = your_name
        self.username = username
        self.playlist_id = playlist_id
        self.liked = liked

    def save_to_mongo(self):
        """
        mongoDB collection에 내 트랙리스트 데이터를 저장합니다.
        """
        _, collection = super().your_collection(self.your_name)
        _, df = super().get_info()
        records= json.loads(df.to_json(orient='records'))

        collection.insert_many(documents=records)
        


class GetFromMongoDB(MongoCollection):
    def __init__(self):
        super().__init__()
    
    def get_from_mongo(self, your_name):
        """
        mongoDB에 저장된 collection을 DataFrame으로 불러옵니다.
        """
        _, collection = super().your_collection(your_name)
        doc = collection.find({})
        df = pd.DataFrame(doc)
        result_df = df.sample(frac=1).reset_index(drop=True)

        return result_df

def transform_df(dataframe):
    # 오브젝트 - > 문자형
    dataframe['_id'] = dataframe['_id'].astype(str)
    dataframe['id'] = dataframe['id'].astype(str)
    dataframe['your_name'] = dataframe['your_name'].astype(str)
    # 오브젝트 - > 숫자형
    dataframe['key'] = pd.to_numeric(dataframe['key'])
    dataframe['duration_ms'] = pd.to_numeric(dataframe['duration_ms'])
    dataframe['time_signature'] = pd.to_numeric(dataframe['time_signature'])

    return dataframe


class MergeMongoDB(GetFromMongoDB):
    def __init__(self):
        pass

    def merge_all_data(self):
        dir = str(Path(__file__).parent.parent)
        database, _ = super().your_collection('JY')
        COLLECTION_NAME = 'total_userdata'

        your_names = [s.replace('_collection', '') for s in database.list_collection_names()]
        your_names.remove('my_playlist')
        cols = super().get_from_mongo(your_name='JY').columns.tolist()

        df_concat = pd.DataFrame(columns=cols)

        for name in your_names:
            df = super().get_from_mongo(your_name=name)
            df['your_name'] = name
            df_concat = pd.concat([df_concat, df])

        df_concat = df_concat.reset_index(drop=True)
        df_result = df_concat.drop(['type', 'uri', 'track_href', 'analysis_url'], axis=1)
        df_result['liked'] = pd.to_numeric(df_result['liked'])

        df_result.to_csv(f'{dir}/my_app/total_userdata/total_userdata.csv')

        #mongoDB에 저장
        collection = database[COLLECTION_NAME]
        records = json.loads(df_result.to_json(default_handler=str, orient='records'))

        if database[COLLECTION_NAME]:
            database[COLLECTION_NAME].drop()

        collection.insert_many(documents=records)

        # DB에 저장
        df_sql = transform_df(df_result)
        conn = sqlite3.connect(f'{dir}/my_app/total_userdata/fake.db')
        df_sql.to_sql(f'{dir}/my_app/total_userdata/total_userdata.db', conn, if_exists='replace')

        return df_result


class DeleteUser(MergeMongoDB):
    def __init__(self):
        super().__init__()

    def delete_yourname(self, your_name):
        COLLECTION_NAME = f'{your_name}_collection'
        database, _ = super().your_collection(your_name=your_name)
        database[COLLECTION_NAME].drop()

        # DB에 덮어씌우기
        super().merge_all_data()