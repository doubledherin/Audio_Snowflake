# -*- coding: utf-8 -*-

import json, os, pickle, requests
from sys import argv

# from algorithm import algorithm



api_key = os.environ.get("ECHO_NEST_API_KEY")

# calls Echonest API with artist name and song title and
# returns a dictionary of song data
def get_song_data(artist, title):

	song_data = {}

	# get general song info
	###########################################
	
	# TO DO: See if I can replace the below dictionary format with the concatentated string format. Note that the fact that # "bucket" appears twice in the concat version could prove tricky.
	# params = {"api_key" : api_key, "format" : "json", "results" : "1", "artist": artist, "title" : title, "bucket" : "id:spotify"}
	# response_general_info = requests.get("http://developer.echonest.com/api/v4/song/search", params=params)
	
	response_general_info = requests.get("http://developer.echonest.com/api/v4/song/search?api_key=" + api_key + "&format=json&results=1&artist=" + artist + "&title=" + title + "&bucket=audio_summary&bucket=id:spotify")

	if response_general_info.status_code != 200:
		return "Error accessing Echonest API for 1st get_song_data call. Status code %d" % response_general_info.status_code
	
	results = json.loads(response_general_info.content)

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
		# round to no more than 3 decimal places
		if type(value) == float:
			value = round(value, 3)
		song_data[key] = value

	# call echonest to get spotify track uri
	###########################################
	response_spotify_track_uri = requests.get("http://developer.echonest.com/api/v4/song/search?api_key=" + api_key + "&format=json&results=1&artist=" + artist + "&title=" + title + "&bucket=tracks&bucket=id:spotify")

	if response_spotify_track_uri.status_code != 200:
		return "Error accessing Echonest API. Status code %d" % response_spotify_track_uri.status_code

	results = json.loads(response_spotify_track_uri.content)

	spotify_track_uri = results["response"]["songs"][0]["tracks"][0]["foreign_id"]
	song_data["spotify_track_uri"] = spotify_track_uri
	


	# print song_data
	return song_data

def collapse_sections(artist, title):
	song_data = get_song_data(artist, title)

	# get analyses of song sections
	###########################################
	analysis_url = str(song_data["analysis_url"])

	respose_analysis_url = requests.get(analysis_url)

	if respose_analysis_url.status_code != 200:
		return "Error accessing analysis url. Status code %d" % respose_analysis_url.status_code

	results = json.loads(respose_analysis_url.content)

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

	# for key, value in newer_collapsed.iteritems():
	# 	print key, ": ", value


	# create list of dictionaries, each dictionary stores one section's data
	value_list = []
	sorted_keys = sorted(newer_collapsed.keys())
	for i in range(len(sorted_keys)):
		d = {}
		# d["hypo%d" % i] = []
		# inner_d = {}
		# inner_d["duration"] = sorted_keys[i][0]
		# inner_d["key"] = sorted_keys[i][1]
		# inner_d["mode"] = sorted_keys[i][2]
		# inner_d["time_signature"] = sorted_keys[i][3]

		d["hypo%d" % i] = {}
		d["hypo%d" % i]["duration"] = sorted_keys[i][0]
		d["hypo%d" % i]["key"] = sorted_keys[i][1]
		d["hypo%d" % i]["mode"] = sorted_keys[i][2]
		d["hypo%d" % i]["time_signature"] = sorted_keys[i][3]


		v = newer_collapsed[sorted_keys[i]]

		for key, value in v.iteritems():
			d["hypo%d" % i][key] = value

		# for key, value in inner_d.iteritems():
		# 	print "INNER D:", key, value

		# d["hypo%d" % i].append(inner_d)
		value_list.append(d)

	song_data["value_list"] = value_list
	return song_data
	# print "VALUE LIST: ", value_list

	# patterns = algorithm(value_list)

	# print patterns

def algorithm(artist, title):
	song_data = collapse_sections(artist, title)
	# for item in song_data:
	# 	print item

	patterns = []


	# for the epitrochoid (outer ring)
	duration = song_data["duration"]
	tempo = song_data["tempo"]
	key = song_data["key"]
	mode = song_data["mode"]
	time_signature = song_data["time_signature"]
	energy = song_data["energy"]
	loudness = song_data["loudness"]
	valence = song_data["valence"]

	a = None
	b = None
	h = None
	hue = None
	saturation = None
	brightness = None
	transparency = None

	d = {}

	d["a"] = a
	d["b"] = b 
	d["h"] = h
	d["hue"] = hue
	d["saturation"] = saturation
	d["brightness"] = brightness
	d["transparency"] = transparency

	patterns.append(d)


	# for hypotrochoids (inner rings)
	value_list = song_data["value_list"]
	print "VALUE LIST: ", value_list
	for section in value_list:
		v = section.values()
		# print type(v)
		# print v

		duration = v[0]["duration"]
		avg_tempo = v[0]["avg_tempo"]
		key = v[0]["key"]
		mode = v[0]["mode"]
		time_signature = v[0]["time_signature"]
		avg_loudness = v[0]["avg_loudness"]

		avg_confidence = v[0]["avg_confidence"]
		avg_key_confidence = v[0]["avg_key_confidence"]
		avg_mode_confidence = v[0]["avg_mode_confidence"]
		avg_time_signature_confidence = v[0]["avg_time_signature_confidence"]

		a = None
		b = None
		h = None
		hue = None
		saturation = None
		brightness = None
		transparency = None

		d = {}

		d["a"] = a
		d["b"] = b 
		d["h"] = h
		d["hue"] = hue
		d["saturation"] = saturation
		d["brightness"] = brightness
		d["transparency"] = transparency

		patterns.append(d)

	# patterns_json = json.dumps(patterns)
	# song_data["patterns"] = patterns_json

	# patterns_str = pickle.dumps(patterns)

	# print "HEY", type(patterns_str)
	song_data["patterns"] = patterns
	# print song_data["patterns"]
	return song_data

# 	import json

# values = [{"a": 640, "b": 260, "h": 19}, {"a": 300, "b": 140, "h": 175}, {"a": 100, "b": 175, "h": 175}, {"a": 475, "b": 50, "h": 50}, {"a": 490, "b": 190, "h": 90}]

# values_json = json.dumps(values)

def main():
	script, artist, title = argv
	algorithm(artist, title)
	# get_song_data(artist, title)
	# add_sections(artist, title)
	# collapse_sections(artist, title)
	# get_echonest_track_id(artist, title)
	# get_spotify_track_uri(artist, title)
	# get_music_player(artist, title)

if __name__ == "__main__":
	main()