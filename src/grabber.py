# Import requests, shutil python module.
import requests
import shutil
import os
import logging
log = logging.getLogger(__name__)


def store_file(url, storage_location, filename):
    # This is the image url.
    image_url = url  # "https://www.dev2qa.com/demo/images/green_button.jpg"

    # Open the url image, set stream to True, this will return the stream content.
    resp = requests.get(image_url, stream=True)

    # Open a local file with wb ( write binary ) permission.
    path_of_file = "%s%s%s" % (storage_location, os.path.sep, filename)
    log.debug(path_of_file)
    local_file = open(path_of_file, 'wb')

    # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
    resp.raw.decode_content = True

    # Copy the response stream raw data to local image file.
    shutil.copyfileobj(resp.raw, local_file)

    # Remove the image url response object.
    local_file.close()
    del resp
