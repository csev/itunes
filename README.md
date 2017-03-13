# Simple iTunes Podcast Maker

This is a simple set set of steps to take a folder full of videos or audios and turn them into a decent looking podcast.  This only
works on a Macintosh and in the command line as it used the `afinfo` to determine the file duration.  I am sure a Linux version could be made - I just did not do it yet.

Steps
-----

Go into the folder containing the videos and pull down `make_json.py` and `make_xml.py`  First produce the JSON file

    python3 make_json.py > podcast.json

Then edit the JSON file - replace all of the missing bits with the correct bits.  Make sure the urls are 'http:' and
not 'https:' - weird but seems to be necessary in the open RSS world.   The contents with 'Z\_' in front of them
must be replaced.

    "00-Python3-Mac-2016-12-30-3400.mov" : {
       "post_title" : "Z_post_title",
       "post_excerpt" : "Z_post_excerpt",
       "post_file" : "00-Python3-Mac-2016-12-30-3400.mov",
       "post_date" : "Fri, 30 Dec 2016 05:00:00 -0000",
       "post_duration" : 262,
       "post_explicit" : "no"
    },

Also the items are in srted order by name, you can reorder them in this json file to your heart's content if the naming
of the files ends up with an oder you don't like. 

The `make_json.py` code already put the file name, last modified date, and duration 
in automatically.  You can override these when you edit the file.

You might want to validate the JSON after you edit it it.

Once you have the `podcasts.json` file to your liking convert it to XML:

    python3 make_xml.py > podcasts.xml

If all went well, you should be able to validate that file at https://validator.w3.org/feed/ - 
This is the time to fix every little thing.

Other Validators
----------------

When you have a file in place on your web server like http://media.py4e.com/media/video.xml then you can 
try the various validators which are quite nice:

* https://podba.se/
* http://castfeedvalidator.com/

Once you like your podcasts url you can submit it to iTunes at https://podcastsconnect.apple.com/

Updates
-------

If you add some video files, you don't want to wipe out your `podcasts.json` file - you probably want to do something
like:

    python3 make_json.py > new.json
    
Then carefully merge the new bits into your old `podcasts.json` file before re-running `make_xml.py` again.

