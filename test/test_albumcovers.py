import unittest
import os
import json
from src import albumcovers


class TestAlbumCovers(unittest.TestCase):

    def test_is_music_file(self):
        # response = self.read_file(os.path.join(os.path.abspath('.'), 'AUD_USD_5m.json'))

        # TODO return an array of sql statements that can be tested using assertions
        # actual = oanda.transform_candles(response)
        # self.assertTrue(actual.startswith('INSERT'))
        # self.assertEquals(actual.date, '20/d/d...')
        self.assertTrue(albumcovers.is_music_file('somename.mp3'))
        self.assertTrue(albumcovers.is_music_file('somename.m4a'))

    def test_scan_folder(self):
        misc = 'C:\\Users\\paul_\\Source\\pgiles\\covergirl\\test\\opt\\_Misc'
        albums, artists = albumcovers.scan_folder(misc)
        self.assertEqual(len(albums), 1)
        self.assertEqual(len(artists), 2)
        self.assertTrue({'artist': 'Barefoot Truth',
                         'album': 'Carry Us On',
                         'location': misc + '\\Barefoot Truth\\Carry Us On'} in albums)

        bob = tuple({'artist': 'Bob Seager', 'location': misc + '\\Bob Seager'}.items())
        self.assertTrue(artists.__contains__(bob))

    def test_extract_image(self):
        json_str = self.read_file(os.path.join(os.path.abspath('.'), 'artist_info.json'))
        self.assertEqual(json_str['artists']['items'][0]['name'], 'Citizen Cope')

    @staticmethod
    def read_file(file_path):
        path = os.path.abspath('.')
        ret = {}

        if file_path:
            path = file_path
        if os.path.isfile(path):
            with open(path, 'r') as handle:
                ret = json.load(handle)
        return ret


if __name__ == '__main__':
    unittest.main()
