# -*- coding: utf-8 -*-
import os
import json, requests

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


	# get info on song sections
	analysis_url = str(song_data["analysis_url"])	
	r1 = requests.get(analysis_url)

	status_code = r1.status_code
	r1 = json.loads(r1.content)

	sections = r1["sections"]

	song_data["num_sections"] = len(sections)


	#return song_data