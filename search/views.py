from django.shortcuts import render
from django.conf import settings
from datetime import datetime, timezone
from django.core.paginator import Paginator
from background_task import background
from .models import Video
import requests

# Create your views here.
def index(request):

    # async process repeats every 10 seconds
    fetch_feed(repeat=10)

    videos_list = Video.objects.all()
    paginator = Paginator(videos_list, 6)
    page = request.GET.get('page', 1)

    videos = paginator.page(page)
    context ={
        'videos' : videos
    }
    return render(request, 'search/index.html',context)

@background
def fetch_feed():
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    local_time = datetime.now(timezone.utc).astimezone()
    params = {
        'part':'snippet',
        # 'publishedAfter': local_time.isoformat(),
        'maxResults':12,
        'order':'date',
        'q':'cricket',
        'type':'video',
        'key': settings.YOUTUBE_DATA_API_KEY
    }

    fetched_video_ids = []
    existing_vid_ids = get_existing_vid_id()
    response = requests.get(search_url, params=params)
    
    print(response.text)
    fetched_videos = response.json()['items']
    # print(fetched_videos)
    videos = []

    for video in fetched_videos:
        fetched_video_ids.append(video['id']['videoId'])

    for video in fetched_videos:
        vid_id = video['id']['videoId']

        if (vid_id not in existing_vid_ids):

            Video_id = video['id']['videoId']
            Title = video['snippet']['title']
            Published_at = video['snippet']['publishedAt']
            Description = video['snippet']['description']
            Thumbnail = video['snippet']['thumbnails']['high']['url']
                    
            new_video_feed = Video(video_id=Video_id, title=Title, description=Description, published_at=Published_at, thumbnail=Thumbnail)
                    
            new_video_feed.save()

    current_videos = Video.objects.all()

    for record in current_videos.iterator():
        if record.video_id not in fetched_video_ids:
            record.delete()



        # fetched_video_ids.append(video['id']['videoId'])
        # video_data = {
        #     'title': video['snippet']['title'],
        #     'thumbnail' : video['snippet']['thumbnails']['high']['url'],
        #     'publishedAt' : video['snippet']['publishedAt'],
        #     'description' : video['snippet']['description']
        # }
        # videos.append(video_data)
    # return videos


    # fetched_vid_id = set()
    # for feed in data['items']:
    #     try:
    #         fetched_vid_id.add(feed['id']['videoId'])
    #     except:
    #         print("exception")

    # existing_vid_ids = get_existing_vid_id()
    # for fetched_feed in data['items']:
    #         try:
    #             vid_id = fetched_feed['id']['videoId']

    #             if (vid_id not in existing_vid_ids):

    #                 Video_id = fetched_feed['id']['videoId']
    #                 snippet = fetched_feed['snippet']
    #                 Title = snippet['title']
    #                 Published_at = snippet['publishedAt']
    #                 Description = snippet['description']
    #                 Thumbnail = snippet['thumbnails']['default']
    #                 Thumbnail_url = Thumbnail['url']
                    
    #                 new_video_feed = Video(video_id=Video_id, title=Title, description=Description, published_at=Published_at, thumbnail_url=Thumbnail_url)
    #                 
    #                 new_video_feed.save()
    #         except:
    #             pass
    # print(response.text)

def get_existing_vid_id():
    
    existing_vid_ids = []
    videos = Video.objects.all()

    for record in videos.iterator():
        existing_vid_ids.append(record.video_id)

    return existing_vid_ids


