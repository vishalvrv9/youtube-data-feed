from django.shortcuts import render
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q
from background_task import background
from .models import Video
import requests
import datetime

# Create your views here.
def index(request):

    # async process repeats every 10 seconds
    fetch_feed(repeat=10)

    # list all videos from model
    query = request.GET.get("q", None)
    videos_list = Video.objects.all().order_by('-published_at')
    if query is not None:
        videos_list = videos_list.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) 
                )

    # setup paginator for 6 per page
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
    d = datetime.datetime.utcnow()
    time_yt_format= d.isoformat("T") + "Z"

    params = {
        'part':'snippet',
        # 'publishedAfter': time_yt_format,
        'maxResults':12,
        'order':'date',
        'q':'cricket',
        'type':'video',
        'key': settings.YOUTUBE_DATA_API_KEY
    }

    # to store new fetched videos after every interval
    fetched_video_ids = []
    # storing existing video ids to flush previously fetched data upon new fetch
    existing_vid_ids = get_existing_vid_id()

    response = requests.get(search_url, params=params)
    
    fetched_videos = response.json()['items']
    
    # videos = []

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


def get_existing_vid_id():
    
    existing_vid_ids = []
    videos = Video.objects.all()

    for record in videos.iterator():
        existing_vid_ids.append(record.video_id)

    return existing_vid_ids


