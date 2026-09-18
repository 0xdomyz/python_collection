convert mp4 to mp3::

    ffmpeg -i input.mp4 -q:a 0 -map a output.mp3
    ffmpeg -i input.mp4 -vn -c:a libmp3lame -q:a 2 output.mp3

list devices::

    ffmpeg -list_devices true -f dshow -i dummy

capture windows audio stream::

    ffmpeg -f dshow -i audio="Stereo Mix (Realtek High Definition Audio)" test2.mp3

    ffmpeg -f dshow -i audio="Stereo Mix (Realtek High Definition Audio)" -acodec libmp3lame -ab 128k -ac 2 -ar 44100 -f mp3 -y "test.mp3"

device options::

    ffmpeg -list_options true -f dshow -i audio="Stereo Mix (Realtek High Definition Audio)"
