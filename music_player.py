from __future__ import unicode_literals
import youtube_dl
import requests
import bs4

file_name=""


def search_song(song):
    global file_name
    url = "https://www.youtube.com/results?search_query="+str(song) 
    response =requests.get(url)
    html = str(response.text)
    i1=html.index('"title":{"runs":[{"text":"')
    i2=html.index('"',i1+26)
    song_name=html[i1+26:i2]
    i1=html.index('"url":"/watch?')
    i2=html.index('"',i1+15)
    href=html[i1+7:i2]

    href2=html[i1+16:i2]

    output_file_name=song_name
    file_name=output_file_name
    
    return ("https://www.youtube.com"+href)

def get_file_name():
  global file_name
  return file_name

    





def download_mp3(link,sng):
  ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl':"songs/" +sng+ ".mp3"
    
  }

  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
      ydl.download([link])


if __name__ == "__main__":
  download_mp3('https://www.youtube.com/watch?v=9VvmixeowNI')
