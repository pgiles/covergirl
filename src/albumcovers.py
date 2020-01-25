#!/usr/bin/env python

import argparse
import logging
import sys
import os
import requests
import grabber
from spotify import Spotify


log = logging.getLogger()
log.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler("{}.log".format(os.path.realpath(__file__)))
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
long_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
short_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(long_format)
ch.setFormatter(short_format)
log.addHandler(fh)
log.addHandler(ch)


# -------
def process_args():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input-dir', '-d',
        dest='music_dir',
        action='store',
        # default='C:\\Users\\paul_\\Tunes',
        default='C:\\Users\\paul_\\Source\\pgiles\\covergirl\\test\\opt\\_Misc',
        required=False,
        help='Directory to scan for album folders'
    )
    parser.add_argument(
        '--dry-run',
        dest='dry_run',
        action='store_true',
        default=False,
        help='Will not download artwork.'
    )
    parser.add_argument(
        '--verbose', '-v',
        dest='verbose',
        action='store_true',
        help='View debug output.'
    )
    # Process arguments
    return parser.parse_args()


all_args = process_args()
music_file_extensions = ['mp3', 'm4a', 'wma']


def main():
    artist_album_list, artists = scan_folder(all_args.music_dir)
    album_art(artist_album_list)
    artist_art(artists)


def scan_folder(music_dir):
    # breadth first search of folders (file type = folder); this_dir = os.path.dirname(os.path.realpath(__file__))
    artist_album = []
    artist = set()
    for root, dirs, files in os.walk(music_dir):
        path = root.split(os.sep)
        # print((len(path) - 1) * '--', os.path.basename(root))
        for filename in files:
            # skip_existing
            directory_listing = os.listdir(root)
            if directory_listing.__contains__('cover.jpg') or directory_listing.__contains__('artist.jpg'):
                continue
            # add to dicts based on file hierarchy convention (artist > album)
            if is_music_file(filename) and song_inside_album_folder(path):
                # print(len(path) * '--', filename)
                chunks = root.split(os.sep)
                # print("root '{}' has {} chunks.".format(root, len(chunks)))
                a_a = {'location': root, 'artist': chunks[(len(chunks)-2)], 'album': chunks[(len(chunks)-1)]}
                artist_album.append(a_a)
                chunks.pop()
                artist.add(tuple({'location': os.sep.join(chunks), 'artist': chunks[(len(chunks)-1)]}.items()))
                break
            elif song_inside_album_folder(path):
                log.debug("Remove %s %s" % (root, filename))
            else:
                hashable_element = tuple({'location': root, 'artist': root.split(os.sep)[-1]}.items())
                artist.add(hashable_element)
                log.debug("Album folder or artist art missing: {} {}".format(root, filename))

    return artist_album, artist


def album_art(artist_album_list):
    for artist_album in artist_album_list:
        log.debug("album_art {} {} {}".format(artist_album['artist'], artist_album['album'], artist_album['location']))

        image_url = "http://cover.jpg"
        if all_args.dry_run is False:
            image_url = extract_album_art_url(artist_album)
        # if image_path != null; then save_file(location, contents, file_name)
        if image_url:
            log.info("Adding album art to: %s", artist_album['location'])
            if all_args.dry_run is False:
                grabber.store_file(image_url, artist_album['location'], 'cover.jpg')
        else:
            log.error("Missing album art image URL: {}".format(artist_album))


def artist_art(artists):
    for artist in artists:
        d = dict(artist)
        log.debug("artist_art {} {}".format(d['location'], d['artist']))

        image_url = "http://artist.jpg"
        if all_args.dry_run is False:
            image_url = extract_artist_art_url(d['artist'])
        # if image_path != null; then save_file(location, contents, file_name)
        if image_url:
            log.info("Adding artist art to: %s", d['location'])
            if all_args.dry_run is False:
                grabber.store_file(image_url, d['location'], 'artist.jpg')
        else:
            log.error("Missing artist art image URL: {}".format(d))


def extract_album_art_url(artist_album):

    payload = client.album_info(artist_album["artist"], artist_album["album"])
    # if found return image path, else return None
    try:
        image = (str(payload['albums']['items'][0]['images'][0]['url']))
    except:
        return None
    return image


def extract_artist_art_url(artist):

    payload = client.artist_info(artist)
    # if found return image path, else return None
    try:
        image = (str(payload['artists']['items'][0]['images'][0]['url']))
    except:
        return None
    return image


def is_music_file(filename):
    return filename.split(".")[-1] in music_file_extensions


def song_inside_album_folder(path):
    return path[-2] != all_args.music_dir.split(os.sep)[-1]


def setup():

    r = requests.get('%s/v1' % all_args.vault_host)
    if not(100 <= int(r.status_code) < 500):
        print('Vault host is not reachable. %d' % r.status_code)
        exit(1)

    if all_args.verbose:
        print('Vault API available.')


if __name__ == "__main__":
    # setup()
    client = Spotify()
    main()
