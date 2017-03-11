
# https://lists.apple.com/archives/syndication-dev/2005/Nov/msg00002.html
import json

# http://stackoverflow.com/questions/3453177/convert-python-datetime-to-rfc-2822
import datetime
import time
from email import utils

# https://wiki.python.org/moin/EscapingXml
from xml.sax.saxutils import escape
# escape("< & >")

nowdt = datetime.datetime.now()
nowtuple = nowdt.timetuple()
nowtimestamp = time.mktime(nowtuple)
now2822 = utils.formatdate(nowtimestamp)

json_data=open('podcast.json').read()

data = json.loads(json_data)

top='''<?xml version="1.0" encoding="UTF-8"?>
<rss xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" 
    xmlns:dc="http://purl.org/dc/elements/1.1/" 
    xmlns:atom="http://www.w3.org/2005/Atom"
version="2.0">
<channel>
	<title>site_title</title>
	<link>site_url</link>
	<lastBuildDate>site_time</lastBuildDate>  <!-- rfc822 -->
	<language>en-US</language>
	<generator>Tsugi (http://www.tsugi.org)</generator>
	<itunes:author>site_podcast_owner_name</itunes:author>
	<itunes:subtitle>site_description</itunes:subtitle>
	<itunes:summary>site_description</itunes:summary>
	<description>site_description</description>
	<copyright>site_podcast_copyright</copyright>
	<itunes:explicit>site_podcast_explicit</itunes:explicit>
	<itunes:keywords>site_podcast_keywords</itunes:keywords>
	<itunes:owner>
		<itunes:name>site_podcast_owner_name</itunes:name>
		<itunes:email>site_email</itunes:email>
	</itunes:owner>
        <atom:link href="site_podcast_url" rel="self" type="application/rss+xml" />
	<itunes:image href="site_podcast_image"/>'''

glob = [
'site_title', 
'site_url',
'site_podcast_owner_name',
'site_description',
'site_podcast_keywords',
'site_podcast_image',
'site_podcast_url',
'site_podcast_copyright',
'site_email',
'post_base']

# site_time
# site_podcast_explicit

def global_fields(out, glob, data) :
    for field in glob:
        out = out.replace(field, data[field])
    out = out.replace('site_time',now2822)
    if ( 'site_podcast_explicit' in data and data['site_podcast_explicit'].find('site_podcast_explicit') < 0 ) :
        out = out.replace('site_podcast_explicit',data['site_podcast_explicit'])
    else :
        out = out.replace('site_podcast_explicit','no')
    return out

print(global_fields(top, glob, data))

# https://lists.apple.com/archives/syndication-dev/2005/Nov/msg00002.html#_Toc526931682
for category in data['categories'] :
    pieces = category.split('/')
    if len(pieces) == 1 :
        print('        <itunes:category text="'+escape(pieces[0])+'"/>')
    else:
        print('        <itunes:category text="'+escape(pieces[0])+'">')
        print('            <itunes:category text="'+escape(pieces[1])+'"/>')
        print('        </itunes:category>')


item_text='''        <item>
		<title>post_title</title>
		<dc:creator>site_podcast_owner_name</dc:creator>
		<pubDate>post_date</pubDate> <!-- rfc822 -->
		<link>post_base/post_file</link>
		<guid isPermaLink="true">post_base/post_file</guid>
		<description>post_excerpt</description>
		<itunes:author>site_podcast_owner_name</itunes:author>
		<itunes:summary>post_excerpt</itunes:summary>
		<itunes:explicit>post_explicit</itunes:explicit>
		<itunes:duration>post_duration</itunes:duration>
		<enclosure url="post_base/post_file" length="post_duration" type="audio/mpeg" />
	</item>'''

bottom=''' </channel>
</rss>'''

items = [ 'post_title', 
'post_explicit',
'post_duration',
'post_file',
'post_date',
'post_excerpt']

for (item, values) in data['items'].items() : 
    out = global_fields(item_text, glob, data)
    for field in items:
        out = out.replace(field, str(values[field]))
    print(out)

print(bottom)

