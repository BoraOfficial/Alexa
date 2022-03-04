from pydub import AudioSegment
from pydub.playback import play
from os import remove, getpid

pid = open("music.stop", "w")
pid.write(str(getpid()))
pid.close()

song = AudioSegment.from_wav("song.wav")
play(song - 4)
remove("song.mp3")
remove("song.mp4")

