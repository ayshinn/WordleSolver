"""
### HOW TO USE ###
On the command line, you'd run
`python3 CurseWordCalculator.py`
and it'll prompt you:
`What is the author? (Only first letter capitalized):`
and
`What is the song name? (all lower case, replace spaces with '-'):`.

It'll generate a URL for genius.com, grab lyrics, and then parse through them for any matches to bad words.

(I personally haven't used jupyter but it should run in there I think?
You may need to figure how to do that, copy this code in a notebook or something)

"""

from bs4 import BeautifulSoup
import requests
# import pandas as pd

def checkforbadwords(lyrics):
  # List of bad words
  badwords = []

  # NOTE IF YOU WANT TO USE PANDAS, UNCOMMENT LINE 19, and 26-29, and comment out lines 32-38
  # read from badwords.csv
  # df = pd.read_csv('badwords.csv')
  # for word in df.values:
  #   badwords.append(word)

  # read from badwords.txt
  badwordsfile = open('badwords.txt', 'r')
  while True:
    badword = badwordsfile.readline()
    if not badword:
      break
    badwords.append(badword.strip())
  badwordsfile.close()

  # Goes through lyrics and sees if it contains any bad words as defined by badwords.txt
  for lyric in lyrics:
    for badword in badwords:
      if badword in lyric:
        print('This song has a bad word. It is not safe for work.')
        print('Bad word: ' + badword)
        return
  
  print('This song is ok and safe for work :)')
  return

def main():
  # Step 1: get artist and song title input. 
  # The input needs to be formatted in a way that it'll fit in a genius.com URL address
  # Basically you'll need what goes here: https://genius.com/{ARTIST}-{SONGTITLE}-lyrics
  # Example: [Billie-eilish] and [bitches-broken-hearts] -> https://genius.com/Billie-eilish-bitches-broken-hearts-lyrics
  artist = input("What is the author? (Only first letter capitalized): ")
  songtitle = input("What is the song name? (all lower case, replace spaces with '-'): ")

  # Step 2: get web URL from input
  baseURL = 'https://genius.com/'
  URLSuffix = '-lyrics'
  URL = baseURL + artist + '-' + songtitle + URLSuffix
  print('URL to parse: ' + URL)

  # Step 3: 
  # code from https://www.johnwmillr.com/scraping-genius-lyrics/
  page = requests.get(URL)
  htmlPage = BeautifulSoup(page.text, "html.parser")

  # Scrape the song lyrics from the HTML
  lyrics = htmlPage.find("div", class_="lyrics").get_text()

  print('Full song lyrics:')
  print(lyrics)
  lyricslist = lyrics.split()

  checkforbadwords(lyricslist)


if __name__ == '__main__':
  # CODE STARTS HERE AND EXECUTES main()
  main()
