# -*- coding: utf-8 -*-
import os
import json, requests
from sys import argv

#import model

api_key = os.environ.get("ECHO_NEST_API_KEY")

# calls Echonest API with artist name and song title (strings);
# returns a dictionary of song data
def get_song_data(artist, title):


	r = requests.get("http://developer.echonest.com/api/v4/song/search?api_key=" + api_key + "&format=json&results=1&artist=" + artist + "&title=" + title + "&bucket=audio_summary")

	status_code = r.status_code
	results = json.loads(r.content)

	song_data = {}

	# get general song info
	song_general = results["response"]["songs"][0]
	
	for key, value in song_general.iteritems():
		# skip audio_summary, which we're getting in the next for loop
		if key == "audio_summary":
			continue
		# rename "id" key for clarity purposes
		if key == "id":
			key = "song_id"
		song_data[key] = value


	# get detailed song info	
	audio_summary = song_general["audio_summary"]

	for key, value in audio_summary.iteritems():
		song_data[key] = value

	return song_data

# get info on song sections and add to song_data dictionary
def add_sections(artist, title):

	song_data = get_song_data(artist, title)
	
	analysis_url = str(song_data["analysis_url"])	
	r1 = requests.get(analysis_url)

	status_code = r1.status_code
	r1 = json.loads(r1.content)

	#TO DO: Build in handler in the case that sections data is limited.
	sections = r1["sections"]
	song_data["sections"] = sections


	song_data["num_sections"] = len(sections)

	return song_data

# takes and artist/title combo, gets the song data, gets the section data
# then collapses the sections into similar groups (those with the same key and mode)
def collapse_sections(artist, title):
	song_data = add_sections(artist, title)
	sections = song_data["sections"]

	collapsed = {}

	for i in range(len(sections)):
		key = sections[i]["key"]
		mode = sections[i]["mode"]
		collapsed[(key, mode)] = collapsed.setdefault((key, mode), [])
		collapsed[(key, mode)].append(sections[i])
	
	for key, value in collapsed.iteritems():
		print "Key: %r, Value: %r\n" % (key, value)
	print song_data["num_sections"]

def main():
	script, artist, title = argv
	print collapse_sections(artist, title)

if __name__ == "__main__":
	main()





