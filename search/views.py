from django.shortcuts import render
from django.conf import settings
from background_task import background
import requests

# Create your views here.
def index(request):

    fetch_feed(repeat=10)
    return render(request, 'search/index.html')

@background
def fetch_feed():
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'part':'snippet',
        'maxResults':5,
        'order':'date',
        'q':'cricket',
        'type':'video',
        'key': settings.YOUTUBE_DATA_API_KEY
    }

    response = requests.get(search_url, params=params)
    print(response.text)


