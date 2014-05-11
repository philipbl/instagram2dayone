instagram2dayone
================

This script will convert an Instagram image into a Day One journal entry using [Google App Engine][gae] and [IFTTT][if]. IFTTT downloads Instagram images into a specific folder in your Dropbox. This script watches that folder and when an image is added, will convert it into a Day One journal entry.

## Steps to Setup

First, you need to set up two rules on ifttt.com. The first rule will download the image into a specific folder in Dropbox and the other rule will download the images caption into the same folder as a text file. Both the image and the caption text file need to have the same file name, the creation date.

Next, this script needs to be deployed onto Google App Engine.


[gae]: https://developers.google.com/appengine/?csw=1
[if]: http://ifttt.com
