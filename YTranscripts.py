import googleapiclient.discovery
from urllib.parse import parse_qs, urlparse
import urllib.request
import json
import urllib

def get_playlist_items(playlist_url, developer_key):
    """Function returns a list of links contained by a
    playlist on YouTube. If you do not have a developer key
    you may obtain one in the API section of Google Cloud
    Platform. Be sure to specify Youtube V3 during generation."""

    # We first extract playlist id from url
    query = parse_qs(urlparse(playlist_url).query, keep_blank_values=True)
    playlist_id = query['list'][0]

    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=developer_key)

    # Define our request and limit results if necessary
    request = youtube.playlistItems().list(
        part = 'snippet',
        playlistId = playlist_id,
        maxResults = 50
    )

    response = request.execute()

    playlist_items = []
    while request is not None:
        response = request.execute()
        playlist_items += response['items']
        request = youtube.playlistItems().list_next(request, response)

    video_list = []
    url_list = []
    for t in playlist_items:
        video_list.append(f'{t["snippet"]["resourceId"]["videoId"]}')
        url_list.append([f'https://www.youtube.com/watch?v={t["snippet"]["resourceId"]["videoId"]}&list={playlist_id}&t=0s'])

    return video_list

def get_title(video_id):
    # change to yours VideoID or change url inparams

    params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % video_id}
    url = "https://www.youtube.com/oembed"
    query_string = urllib.parse.urlencode(params)
    url = url + "?" + query_string

    with urllib.request.urlopen(url) as response:
        response_text = response.read()
        data = json.loads(response_text.decode())
        title = data['title']
    return title