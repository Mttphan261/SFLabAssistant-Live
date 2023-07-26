from googleapiclient.discovery import build


api_key = 'AIzaSyAjK_ZZ7riJxHDISl_OLUMDP3DrZpi2tYg'

youtube = build('youtube', 'v3', developerKey=api_key)

# request = youtube.videos().list(
#     part='player',
#     id = ['jRAAaDll34Q', 'idYUy3hf3D0']
# )

# response = request.execute()

# print(response)


def fetch_videos(video_ids):
    videos = []
    request = youtube.videos().list(
    part='snippet, player',
    id = video_ids
)

    response = request.execute()
    for item in response['items']:
        video_id = item['id']
        embed_html = item['player']['embedHtml']
        snippet = item['snippet']
        title = snippet['title']
        description = snippet['description']

        videos.append({
            'video_id': video_id,
            'embed_html': embed_html,
            'title': title,
            'description': description
        })

    return videos
