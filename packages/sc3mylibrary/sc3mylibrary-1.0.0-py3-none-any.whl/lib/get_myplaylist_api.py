import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# spotify api
cid = '591812685f3f4a16bac164011f7f3e33'
secret = 'cec92bbc981b41d49fc7dadcbce0d0f6'

class SpotipyObj():
    def __init__(self, cid=cid, secret=secret):
        self.cid = cid
        self.secret = secret
    
    def sp(self):
        client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)

        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        return sp


# 플레이 리스트의 트랙과 트랙들의 정보를 얻어온다.
class GetMyPlaylistTracks(SpotipyObj):

    def __init__(self, username, playlist_id, liked:bool):
        self.username = username
        self.playlist_id = playlist_id
        self.liked = liked
        
    def get_playlist_tracks(self):
        """
        나의 추천 플레이리스트를 list형태로 반환합니다.
        return: [[artist_1, song_1], [artist_2, song_2], ...]
        """
        sp = super().sp()
        results = sp.user_playlist_tracks(self.username, self.playlist_id, fields='items, uri, name, id, next', limit = 100, market='kr')
        tracks = results['items']
        # 플레이 리스트에 100곡이 넘어가도 계속 불러오기
        while results['next']:
            results = sp.next(results)
            tracks.extend(results['items'])
        
        artist_song_list = [[tracks[i]['track']['artists'][j]['name'], tracks[i]['track']['name'], tracks[i]['track']['id']] for i in range(len(tracks)) for j in range(len(tracks[i]['track']['artists']))]

        return artist_song_list

    def get_features(self, track_id):
        """
        음악의 feature를 추출합니다.
        return: dict list
        """ 
        sp = super().sp()
        # get audio_feature
        features = sp.audio_features(tracks=[track_id])

        danceability = features[0]["danceability"]
        energy = features[0]["energy"]
        key = features[0]["key"]
        loudness = features[0]["loudness"]
        mode = features[0]["mode"]
        speechiness = features[0]["speechiness"]
        acousticness = features[0]["acousticness"]
        instrumentalness = features[0]["instrumentalness"]
        liveness = features[0]["liveness"]
        valence = features[0]["valence"]
        tempo = features[0]["tempo"]
        duration_ms = features[0]["duration_ms"]
        time_signature = features[0]["time_signature"]

        tracks_features = {
                "id" : str(track_id),
                "danceability" : danceability,
                "energy" : energy,
                "key" : key,
                "loudness" : loudness,
                "mode" : mode,
                "speechiness" : speechiness,
                "acousticness" : acousticness,
                "instrumentalness" : instrumentalness,
                "liveness" : liveness,
                "valence" : valence,
                "tempo" : tempo,
                "duration_ms" : duration_ms,
                "time_signature": time_signature,
                "liked" : int(self.liked)
                }
        return tracks_features

class SongArtist(SpotipyObj):
    def __init__(self):
        pass
    
    def get_song_artist(self, tracks_id):
        """
        track id를 입력하면 노래 제목과 아티스트 이름을 반환합니다.

        Args:
            tracks_id ([list]): track id 의 list
        """
        sp = super().sp()
        songs = [sp.track(t)['name'] for t in tracks_id]
        artists = [sp.track(t)['artists'][0]['name'] for t in tracks_id]
        lst = [pair for pair in zip(artists, songs)]

        return lst