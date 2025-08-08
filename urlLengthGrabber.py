import json
import urllib.request

video_id="mhbVUf3yyB0"
api_key="AIzaSyC5IV-ydGiGdDdb0SjjBFH0xLBKY772dVA"
searchUrl="https://www.googleapis.com/youtube/v3/videos?id="+video_id+"&key="+api_key+"&part=contentDetails"
response = urllib.request.urlopen(searchUrl).read()
data = json.loads(response)
print(data)
input()
all_data=data['items']
contentDetails=all_data[0]['contentDetails']
duration=contentDetails['duration']
print(duration)