import unittest
import os
from src import grabber


class TestGrabber(unittest.TestCase):

    download_location = 'C:\\tmp'

    def setUp(self):
        downloaded_file = self.download_location + os.path.sep + 'cover.jpg'
        if os.path.exists(downloaded_file):
            os.remove(downloaded_file)

    def test_store_file(self):
        url = 'https://i.scdn.co/image/8101a4744a4012328ce6d4c7e78fa67f1195a86d'

        grabber.store_file(url, self.download_location, 'cover.jpg')
        actual = os.path.exists(self.download_location + os.path.sep + 'cover.jpg')
        self.assertTrue(actual)


if __name__ == '__main__':
    unittest.main()
