from mutagen.easyid3 import EasyID3
from mutagen.easymp4 import EasyMP4, error as MP4Error
import os
import sys

music_dir = sys.argv[1] + os.path.sep
# music_dir = '..' + os.path.sep

if __name__ == "__main__":
    # "C:\\Users\\paul_\\Source\pgiles\covergirl"
    file_list = os.listdir(music_dir)

    for file_name in file_list:
        audio_file = None
        full_file_path = music_dir + file_name
        if file_name.endswith('m4a'):
            audio_file = EasyMP4(full_file_path)
        elif file_name.endswith('mp3'):
            audio_file = EasyID3(full_file_path)
        else:
            continue

        print("processing", file_name)
        artist = str(audio_file['artist'][0])

        album = None
        dest_dir = None
        try:
            album = str(audio_file['album'][0])
            dest_dir = music_dir + artist + os.path.sep + album
        except KeyError, e:
            dest_dir = music_dir + artist

        # dest_dir = music_dir + artist + os.path.sep + album
        dest = dest_dir + os.path.sep + file_name.split(os.path.sep)[-1]
        print(dest)
        try:
            os.makedirs(dest_dir)
        except OSError, e:
            print(e)
        os.rename(full_file_path, dest)
