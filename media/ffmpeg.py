"""

#capture windows audio stream
ffmpeg -f dshow -i audio="virtual-audio-capturer" -acodec libmp3lame -ab 128k -ac 2 -ar 44100 -f mp3 -y "test.mp3"

"""
