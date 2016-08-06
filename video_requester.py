from googleapiclient.discovery import build


class VideoRequest:

    API_KEY = ''  # Add the API Key here

    def __init__(self, channel_id, uploads_id, maxnum):
        self.channel_id = channel_id
        self.uploads_id = uploads_id
        self.data = []
        self.maxnum = maxnum
        self.response = None

    def request_videos(self, maxnum=None):
        if maxnum is None:
            maxnum = self.maxnum
        # Set up the API service
        service = build('youtube', 'v3', developerKey=self.API_KEY)
        # Work with the search collection
        collection = service.search()
        # Create the request and restrict it to returning the title and videoId
        request = collection.list(part='snippet', channelId=self.channel_id, maxResults=maxnum, order='date',
                                  fields='items(id/videoId,snippet/title)')
        self.response = request.execute()

    def parse_response(self):
        for item in self.response['items']:
            title = item['snippet']['title']
            video_id = item['id']['videoId']
            vid = Video(video_id, title)
            self.data.append(vid)
        return self.data


class Video:
    def __init__(self, video_id, title):
        self.videoID = video_id
        self.title = title
