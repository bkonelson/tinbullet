from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser


channels = {}
DEVELOPER_KEY = "AIzaSyBCGHaWYhxwtDW2hHPbjh52Rm8I1-eGJ_k"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
  developerKey=DEVELOPER_KEY)

  search_response = youtube.search().list(
  q=options.q,
  part="id,snippet",
  maxResults=options.max_results
  ).execute()
  counter = 0
  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#channel":
      channels['channel'+str(counter)] =  search_result["id"]["channelId"]
      counter += 1
  print(channels['channel0'])
    

if __name__ == "__main__":
  argparser.add_argument("--q", help="Search Term", default="Linus Tech")
  argparser.add_argument("--max-results", help="Max Results", default=5)
  args = argparser.parse_args()

  try:
    youtube_search(args)
  except (HttpError, e):
    print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
    