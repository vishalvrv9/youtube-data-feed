# FROM python:3.6

# RUN apt-get update \
#     && apt-get install -y --no-install-recommends \
#     && rm -rf /var/lib/apt/lists/*

# WORKDIR /usr/src/app
# COPY requirements.txt ./
# RUN pip install -r requirements.txt
# COPY . .

# EXPOSE 8000
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.6

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /youtube_data_feed

# Set the working directory to /youtube_data_feed
WORKDIR /youtube_data_feed

# Copy the current directory contents into the container at /youtube_data_feed
ADD . /youtube_data_feed/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt