from googleapiclient.discovery import build
from video import Video


class VideoRequest:

    API_KEY = ''  # Add the API Key here

    def __init__(self, channelId, uploadsId, maxNum):
        self.channelId = channelId
        self.uploadsId = uploadsId
        self.data = []
        self.maxNum = maxNum
        self.response = None

    def request_videos(self, maxNum=None):
        if maxNum is None:
            maxNum = self.maxNum
        # set up the API service
        service = build('youtube', 'v3', developerKey=self.API_KEY)
        # Work with the search collection
        collection = service.search()
        # Create the request and restrict it to returning the title and videoId
        request = collection.list(part='snippet', channelId=self.channelId, maxResults=maxNum, order='date',
                                  fields='items(id/videoId,snippet/title)')
        self.response = request.execute()

    def parse_response(self):
        for item in self.response['items']:
            title = item['snippet']['title']
            videoId = item['id']['videoId']
            vid = Video(videoId, title)
            self.data.append(vid)
        return self.data
