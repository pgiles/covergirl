import unittest
from src.spotify import Spotify


class TestSpotify(unittest.TestCase):

    def test_artist_info(self):
        client = Spotify()
        payload = client.album_info('Blues Traveler', 'Bridge')
        if isinstance(payload, dict) is not None:
            result = (str(payload['artists']['items'][0]['images'][0]['url']))
            self.assertTrue(result.endswith('g'))

    def test_album_info(self):
        client = Spotify()
        #payload = client.album_info('Blues Traveler', 'Bridge')
        payload = client.album_info('Tristan Prettyman', 'Hello...x')
        if isinstance(payload, dict) is not None:
            result = str(payload['albums']['items'][0]['images'][0]['url'])
            self.assertTrue(result.startswith('http'))


if __name__ == '__main__':
    unittest.main()
