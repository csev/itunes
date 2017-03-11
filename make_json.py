import os
import re
import datetime
import time
from email import utils

files = list()
for file in os.listdir():
    if file.startswith('.') : continue
    if file.endswith('.mov') or file.endswith('mp4') or file.endswith('mp3') :
        files.append(file)

files.sort()

glob = ['site_title', 'site_url', 
'site_podcast_owner_name',
'site_description',
'site_podcast_explicit',
'site_podcast_keywords',
'site_podcast_image',
'site_podcast_url',
'site_podcast_copyright',
'site_email',
'post_base']

print("{")
for field in glob:
    print('"'+field+'" : "Z_'+field+'",');

# https://help.apple.com/itc/podcasts_connect/#/itc9267a2f12
# These categories are actually kind of limited / tricky
print('"category_note" : "See: https://help.apple.com/itc/podcasts_connect/#/itc9267a2f12",')
print('"categories" :[')
print('    "Education/Training",')
print('    "Technology/Software How-To"')
print('],')

items = [ 'post_title', 'post_excerpt']

# https://lists.apple.com/archives/syndication-dev/2005/Nov/msg00002.html

# post_explicit
# post_duration
# post_file
# post_date

print()
print('"items" : {')
first = True
for file in files:
    tmp = os.popen("afinfo "+file).read()
    durs = re.findall('estimated duration: ([0-9.]+)',tmp, re.MULTILINE)
    if len(durs) == 1 : 
        dur = float(durs[0])
    else: 
        dur = 0
    tt = os.path.getmtime(file)

    # http://stackoverflow.com/questions/3453177/convert-python-datetime-to-rfc-2822
    dt = datetime.date.fromtimestamp(tt)
    nowtuple = dt.timetuple()
    nowtimestamp = time.mktime(nowtuple)
    dat = utils.formatdate(nowtimestamp)

    if ( not first ) : print("},")
    first = False
    print('"'+file+'" : {')
    for field in items:
        print('   "'+field+'" : "Z_'+field+'",');
    print('   "post_file" : "'+file+'",');
    print('   "post_date" : "'+dat+'",');
    print('   "post_duration" : '+str(int(dur))+',');
    print('   "post_explicit" : "no"');

print("}")
print("}") #items

print("}")

