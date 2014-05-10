#!/usr/bin/env python

import webapp2
import os
import time
import datetime
import uuid
import plistlib
from StringIO import StringIO
from dropbox_login import get_client
from google.appengine.api import mail


WATCH_FOLDER = '/Photos/Instagram'
JOURNAL_FOLDER = '/Apps/Day One/Journal.dayone'


def run():
    client = get_client()
    instagram_folder = client.metadata(WATCH_FOLDER)
    contents = instagram_folder['contents']

    # Only get images
    images = [x['path'] for x in contents if x['path'][-3:] == 'jpg']

    for image in images:
        name = os.path.splitext(image)[0]
        _convert(name, contents, client)

    if len(images) > 0:
        mail.send_mail("philiplundrigan@gmail.com",
                       "trigger@ifttt.com",
                       "#instagram2dayone",
                       "{} {} were added to Day One.".format(len(images),
                                                             "images" if len(images) > 1 else "image"))


def _convert(name, folder_contents, client):
    text_file = name + ".txt"
    image_file = name + ".jpg"

    files = [x['path'].upper() for x in folder_contents]

    # Make sure there is both a text file and a image file
    if not text_file.upper() in files or not image_file.upper() in files:
        return

    entry_name = str(uuid.uuid4()).replace('-', '').upper()

    # Create entry and save
    entry = _create_entry(text_file, entry_name, client)
    response = client.put_file('{}/entries/{}.doentry'.format(JOURNAL_FOLDER, entry_name), StringIO(entry))

    # Delete old text file
    client.file_delete(text_file)

    # Move image
    client.file_move(image_file, '{}/photos/{}.jpg'.format(JOURNAL_FOLDER, entry_name))


def _is_dst():
    return True if time.localtime().tm_isdst == 1 else False


def _create_entry(text_file, entry_name, client):
    # Get creation time and format it
    time_str = text_file.split('/')[-1][:-4]
    format_time = time.strptime(time_str, "%B_%d__%Y_at_%I%M%p")
    format_time = datetime.datetime.fromtimestamp(time.mktime(format_time))
    format_time = format_time + datetime.timedelta(hours=6 if _is_dst() else 7)

    # Get entry text
    f, metadata = client.get_file_and_metadata(text_file)
    entry_text = f.read()

    entry = {}
    entry['Creation Date'] = format_time
    entry['Entry Text'] = entry_text
    entry['Starred'] = False
    entry['Tags'] = ['Bridget']
    entry['Time Zone'] = 'America/Denver'
    entry['UUID'] = entry_name

    return plistlib.writePlistToString(entry)


class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Nothing to see here.')

        run()


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)

