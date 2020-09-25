# Assignment Goal

To make an API to fetch latest videos sorted in reverse chronological order of their publishing date-time from YouTube for a given tag/search query in a paginated response.

- Server calls the YouTube API continuously in background (async) with some interval (10 seconds default, can be altered) for fetching the latest videos for a predefined search query and stores the data of videos (Video title, description, publishing datetime, thumbnails URLs) in a database with proper indexes.
- A GET API which returns the stored video data in a paginated response sorted in descending order of published datetime.
- Dockerizes the app.

To start the app

- clone the repo
- start the container using cli: ```docker-compose up```