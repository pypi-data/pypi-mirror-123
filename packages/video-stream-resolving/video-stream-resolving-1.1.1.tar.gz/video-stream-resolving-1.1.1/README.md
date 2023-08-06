# Introduction

This project includes some video stream platform video stream resolver


# Install

```bash
pip install video-stream-resolver
```


# Usgae

```Python
from video_stream_resolver import resolve_streamtape

# Synchronous resolving 
# Function resolve_xxx always return requests.models.Response object,
# if everything goes well, the response represent video source.
response = resolve_streamtape()
```