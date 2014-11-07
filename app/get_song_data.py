# -*- coding: utf-8 -*-

import os
import json, requests
from sys import argv


api_key = os.environ.get("ECHO_NEST_API_KEY")

# calls Spotify API with artist and title to get a track id
def get_music_player(artist, title):
	
	r = requests.get("https://api.spotify.com/v1/search?q=artist%3A" + artist + "track%3A" + title + "&type=track")

	print r 

	print r.url
	r.json()

	print r

	# curl -X GET "https://api.spotify.com/v1/search?q=artist%3Aelliottsmithtrack%3Asouthernbelle&type=track" -H "Accept: application/json"

# calls Echonest API with artist name and song title (strings);
# returns a dictionary of song data
def get_song_data(artist, title):

	r = requests.get("http://developer.echonest.com/api/v4/song/search?api_key=" + api_key + "&format=json&results=1&artist=" + artist + "&title=" + title + "&bucket=audio_summary&bucket=id:spotify")

	# print r.url

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

	# # pretty print for development purposes
	# for key, value in song_data.iteritems():
	# 	print key, value
	# 	print "\n"

	# song_data now contains everything but the sections data
	return song_data

# get info on song sections from analysis_url
# and add sections to song_data dictionary
def add_sections(artist, title):
	
	song_data = get_song_data(artist, title)
	
	analysis_url = str(song_data["analysis_url"])

	r = requests.get(analysis_url)

	status_code = r.status_code
	results = json.loads(r.content)

	#TO DO: Build in handler in the case that sections data is limited.
	sections = results["sections"]
	song_data["sections"] = sections
 
 # 	# pretty print for development purposes
	# for key, value in song_data.iteritems():
	# 	print key, value
	# 	print "\n"

	return song_data

# collapses sections into groups with same key, mode, and time signature,
# then collapses further by averaging of data in each collapsed section;
# then reduces number of sections to no more than 5
def collapse_sections(artist, title):

	song_data = add_sections(artist, title)

	sections = song_data["sections"]

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

	# # for debugging
	# for key, value in new_collapsed.iteritems():
	# 	print "Key: %r, Value: %r\n" % (key, value)



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

	# # here for pretty printing/debugging only
	# for key, value in newer_collapsed.iteritems():
	# 	print "Key: ", key
	# 	print "Values: "
	# 	for key, value in value.iteritems():
	# 		print key, ": ", value


	# shrink to 5 or fewer sections
	while len(newer_collapsed) > 5:
		
		# remove item with the shortest duration
		sorted_keys = sorted(newer_collapsed.keys())
		shortest_duration = sorted_keys.pop(0)
		del newer_collapsed[shortest_duration]

	# # here for pretty printing/debugging only
	# print "\n\n\n\n\nReduced to five or fewer\n"
	# for key, value in newer_collapsed.iteritems():

	# 	print "Key: ", key
	# 	print "Values: "
	# 	for key, value in value.iteritems():
	# 		print key, ": ", value

def main():
	script, artist, title = argv
	# get_by_title_only("karma police")
	# collapse_sections(artist, title)
	# get_song_data(artist, title)
	get_music_player(artist, title)

if __name__ == "__main__":
	main()