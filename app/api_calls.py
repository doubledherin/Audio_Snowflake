# -*- coding: utf-8 -*-

import os
import json, requests
from sys import argv

api_key = os.environ.get("ECHO_NEST_API_KEY")

# calls Echonest API with artist name and song title and
# returns a dictionary of song data
def get_song_data(artist, title):

	song_data = {}

	# get general song info
	###########################################
	r = requests.get("http://developer.echonest.com/api/v4/song/search?api_key=" + api_key + "&format=json&results=1&artist=" + artist + "&title=" + title + "&bucket=audio_summary&bucket=id:spotify")

	if r.status_code != 200:
		return "Error accessing Echonest API for 1st get_song_data call. Status code %d" % r.status_code
	
	results = json.loads(r.content)

	song_general = results["response"]["songs"][0]
	
	if len(song_general) == 0:
		return "Error. No song data returned from Echonest API."

	for key, value in song_general.iteritems():
		# skip audio_summary, which we're getting in the next for loop
		if key == "audio_summary":
			continue
		
		# rename "id" key for clarity purposes
		if key == "id":
			key = "song_id"

		song_data[key] = value
	
	# get detailed song info
	###########################################	
	try:
		audio_summary = song_general["audio_summary"]
	except:
		"ERROR: No audio summary for %s" % song_data["title"]

	for key, value in audio_summary.iteritems():
		song_data[key] = value

	# call echonest to get spotify track id
	###########################################
	r1 = requests.get("http://developer.echonest.com/api/v4/song/search?api_key=" + api_key + "&format=json&results=1&artist=" + artist + "&title=" + title + "&bucket=tracks&bucket=id:spotify")

	if r1.status_code != 200:
		return "Error accessing Echonest API. Status code %d" % r1.status_code

	results = json.loads(r1.content)

	spotify_track_uri = results["response"]["songs"][0]["tracks"][0]["foreign_id"]
	song_data["spotify_track_uri"] = spotify_track_uri
	
	# get analyses of song sections
	###########################################
	analysis_url = str(song_data["analysis_url"])

	r2 = requests.get(analysis_url)

	if r2.status_code != 200:
		return "Error accessing analysis url. Status code %d" % r2.status_code

	results = json.loads(r2.content)

	#TO DO: Build in handler in the case that sections data is limited.
	sections = results["sections"]

	# collapse song sections
	###########################################

	collapsed = {}
	for i in range(len(sections)):
		key = sections[i]["key"]
		mode = sections[i]["mode"]
		time_sig = sections[i]["time_signature"]
		collapsed[(key, mode, time_sig)] = collapsed.setdefault((key, mode, time_sig), [])
		collapsed[(key, mode, time_sig)].append(sections[i])

	new_collapsed = {}
	# get total duration for each collapsed section
	for key, value in collapsed.iteritems():
		total_duration = 0
		
		for item in value:
			total_duration += item["duration"]
		
		total_duration = int(round(total_duration))
		
		# recreate key so that it starts with total duration
		key = list(key)
		key.insert(0, total_duration)
		key = tuple(key)

		# key is now (total_duration, key, mode, time sig)
		new_collapsed[key] = value

	# for each collapsed section, collapse list of values into averages
	newer_collapsed = {}


	items = new_collapsed.items()

	for key, value in items:
		newer_collapsed[key] = {}

		# get totals for each item in a collapsed section's values
		total_confidence = 0 
		total_key_confidence = 0 
		total_mode_confidence = 0 
		total_time_signature_confidence = 0 
		total_tempo = 0 
		total_loudness = 0

		for item in value:
			total_confidence +=  item["confidence"]
			total_key_confidence += item["key_confidence"]
			total_mode_confidence += item["mode_confidence"]
			total_time_signature_confidence += item["time_signature_confidence"]
			total_tempo += item["tempo"]
			total_loudness += item["loudness"]
		
		# put the totals in a list to use map function for averages
		totals = [total_confidence, total_key_confidence, total_mode_confidence, total_time_signature_confidence, total_tempo, total_loudness]

		averages = map(lambda x: round(x / len(value), 3), totals)

		# add the averaged values to the newer_collapsed dictionary
		newer_collapsed[key]["avg_confidence"] = averages[0]
		newer_collapsed[key]["avg_key_confidence"] = averages[1]
		newer_collapsed[key]["avg_mode_confidence"] = averages[2]
		newer_collapsed[key]["avg_time_signature_confidence"] = averages[3]
		newer_collapsed[key]["avg_tempo"] = averages[4]
		newer_collapsed[key]["avg_loudness"] = averages[5]

	# shrink to 5 or fewer sections
	while len(newer_collapsed) > 5:
		
		# remove item with the shortest duration
		sorted_keys = sorted(newer_collapsed.keys())
		shortest_duration = sorted_keys.pop(0)
		del newer_collapsed[shortest_duration]

	for key, value in newer_collapsed.iteritems():
		print "Key: %s, Value: %r" % (key, value)


def main():
	script, artist, title = argv
	get_song_data(artist, title)
	# add_sections(artist, title)
	# collapse_sections(artist, title)
	# get_echonest_track_id(artist, title)
	# get_spotify_track_uri(artist, title)
	# get_music_player(artist, title)

if __name__ == "__main__":
	main()