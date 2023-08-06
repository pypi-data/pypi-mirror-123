# Pythief DJ

A semi-simple tool for... "borrowing"... audio from YouTube videos.

## Here's why I do this

It's common DJ etiquette (or really just like, person-etiquette) to purchase songs that you use for your craft. I wholeheartedly endorse this ideal and do it myself. However, I'm also a bedroom DJ who mixes a lot of stuff that people never hear, and very often, I want to try mixing a song before I use it in one of my [patented adorable newbie videos](https://www.youtube.com/watch?v=4VfiK_wxq3Y). YouTube is a great source for use cases like this, despite a little moral dubiousness. 

However, I also found YouTube ripping a very tedious process. You search, find your video, go to one of a million "YouTube to Mp3 FAST!" sites, click multiple times, download, save, and so on, so I wrote this tool to automate some of it. I don't have the search thing figured out yet (it can be tricky to identify the right video for a song - for example, some music videos edit the original audio for dramatic effect), but right now, you can use this to download audio from multiple YouTube videos by URL, which is a step up for _my_ workflow, anyway.

## Getting started

1. Install [Python 3.9+](https://www.python.org/downloads/)
2. Install [FFmpeg](https://www.ffmpeg.org/) and make sure it's in your system path by opening a command line/terminal and typing "ffmpeg"
3. Download this repository (or clone it)
4. (I'll explain the rest later, I'm in development)

## Acknowledgments

You can see `requirements.txt` for all of my dependencies, but I'm relying heavily on `pytube` and `pydub`, both of which are doing an incredible amount of heavy lifting in this script. Thanks to those projects.