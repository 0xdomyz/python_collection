"""
Use ffmpeg to cut the end of an audio file

cli::

    python cut_end.py "audio.mp3"

python::

    inp = ' "audio.mp3"'

direct usage::

    ffmpeg -i "audio.mp3" 2>&1 | grep "Duration" | cut -d " " -f 4
    ffmpeg -i "audio.mp3" -acodec mp3 -t 100 "audio_cut.mp3"

    ffmpeg -i "audio.mp3" -acodec mp3 -ss 10 -t 100 "audio_cut.mp3"

"""

from os import system
from subprocess import PIPE, Popen
from sys import argv

ffm = "ffmpeg -i"  # input file
aud = " -acodec mp3"  # add your quality preferences
dur = ' 2>&1 | grep "Duration" | cut -d " " -f 4'


def cutter(inp, t=0):
    out = inp[:-5] + "_cut" + inp[-5:]
    cut = " -t %s" % (duration(inp) - t)
    cmd = ffm + inp + aud + cut + out
    print(cmd)
    system(cmd)


def fader(inp, t=0):
    out = inp[:-5] + "_fade" + inp[-5:]
    fad = ' -af "afade=t=out:st=%s:d=%s"' % (duration(inp) - t, t)
    cmd = ffm + inp + fad + out
    print(cmd)
    system(cmd)


def duration(inp):
    cmd = ffm + inp + dur
    proc = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    if len(err) > 0:
        raise Exception(f"cmd faild: \n{cmd}")
    h, m, s = [float(x) for x in str(out[:-2], "UTF-8").split(":")]
    return (h * 60 + m) * 60 + s


if __name__ == "__main__":
    fname = ' "' + argv[1] + '"'
    t = int(argv[2])
    cutter(fname, t)
    # fader(fname, 5)
