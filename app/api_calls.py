# -*- coding: utf-8 -*-

import json, os, requests
from math import pi
from sys import argv


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

	print "RESULTS: ", results
	spotify_track_uri = results["response"]["songs"][0]["tracks"][0]["foreign_id"]
	song_data["spotify_track_uri"] = spotify_track_uri
	
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

	# create list of dictionaries, each dictionary stores one section's data
	value_list = []
	sorted_keys = sorted(newer_collapsed.keys())
	for i in range(len(sorted_keys)):
		d = {}
	
		d["hypo%d" % i] = {}
		d["hypo%d" % i]["duration"] = sorted_keys[i][0]
		d["hypo%d" % i]["key"] = sorted_keys[i][1]
		d["hypo%d" % i]["mode"] = sorted_keys[i][2]
		d["hypo%d" % i]["time_signature"] = sorted_keys[i][3]

		v = newer_collapsed[sorted_keys[i]]

		for key, value in v.iteritems():
			d["hypo%d" % i][key] = value

		value_list.append(d)

	song_data["value_list"] = value_list
	return song_data

def algorithm(artist, title):
	song_data = collapse_sections(artist, title)

	patterns = []

	# for the epitrochoid (outer ring)
	epi_duration = song_data["duration"]
	epi_tempo = song_data["tempo"]
	epi_key = song_data["key"]
	epi_mode = song_data["mode"]
	epi_time_signature = song_data["time_signature"]
	epi_energy = song_data["energy"]
	epi_loudness = song_data["loudness"]
	epi_valence = song_data["valence"]

	# TO DO: Uncomment the below out and create epitrochoid object for outer ring
	# a = None
	# b = None
	# h = None
	# hue = None
	# saturation = None
	# brightness = None
	# transparency = None

	# d = {}

	# d["a"] = a
	# d["b"] = b 
	# d["h"] = h
	# d["hue"] = hue
	# d["saturation"] = saturation
	# d["brightness"] = brightness
	# d["transparency"] = transparency

	# patterns.append(d)


	# for hypotrochoids (inner rings)
	value_list = song_data["value_list"]

	print "VALUE_LIST: ", value_list
	section_durations = []

	for section in value_list:
		v = section.values()
		section_durations.append(v[0]["duration"])
	min_section_duration = float(min(section_durations))
	max_section_duration = float(max(section_durations))

	for section in value_list:

		v = section.values()

		section_duration = v[0]["duration"]
		section_avg_tempo = v[0]["avg_tempo"]
		section_key = v[0]["key"]
		section_mode = v[0]["mode"]
		section_time_signature = v[0]["time_signature"]
		section_avg_loudness = v[0]["avg_loudness"]

		section_avg_confidence = v[0]["avg_confidence"]
		section_avg_key_confidence = v[0]["avg_key_confidence"]
		section_avg_mode_confidence = v[0]["avg_mode_confidence"]
		section_avg_time_signature_confidence = v[0]["avg_time_signature_confidence"]


		# TO DO: Rescale according to window sizes


		"""
		Linear scaling section:

		uses the following formula:
		
		Where [A, B] is the current range and [C, D] is the desired range:
		
		f(x) = C*(1 - ((x - A) / (B - A))) + D*(((x - A) / (B - A)))
		"""
		# Duration determines size of hypotrochoid

		unscaled_a = float(section_duration) 

		# Get min section_duration and max section duration for each section and 
		# Scale from 200 to min(browser.height, browser.width); approx 700 for now
		# [min_section_duration, max_section_duration] => [200, 700]
		a = 200 * (1 - ((unscaled_a - min_section_duration) / (max_section_duration - min_section_duration) )) + 700 * ((unscaled_a - min_section_duration) / (max_section_duration - min_section_duration))

		b = (a - (section_avg_tempo/section_time_signature))/section_time_signature

		# Relates to loopiness -- the higher the energy and valence, the loopier

		# TO DO: Rescale so that it's tied to the section--right now the h doesn't change
		unscaled_h = epi_energy + epi_valence
		# Scale [-2, 2] to [0, (2*b)]
		h = 0 * (1 - ((unscaled_h + 2)) / 4) + 2 * b * ((unscaled_h + 2) / 4)
		


		"""
		Linear scaling section:

		uses the following formula:
		
		Where [A, B] is the current range and [C, D] is the desired range:
		
		f(x) = C*(1 - ((x - A) / (B - A))) + D*(((x - A) / (B - A)))
		"""

		# TO DO: scale hue to key and mode
		unscaled_hue = section_key
		# [0, 11] to [0, 330]
		# hue = 0 * (1 - (unscaled_hue / 11.0)) + 330 * (unscaled_hue / 11.0 )
		hue = 330 * (unscaled_hue / 11.0 )
		hue = int(hue)


		print "SECTION KEY: ", section_key
		print "unscaled_hue: ", unscaled_hue
		print "unscaled_hue/11.0", (unscaled_hue/11.0)
		print "HUE: ", hue


		# TO DO: Scale to energy or valence; brightness too
		# major mode is fully saturated, minor mode is less saturated
		if section_mode == 0:
			saturation = 100
		else:
			saturation = 75
		
		# TO DO: scale from 50 to 100
		brightness = 60
		
		unscaled_transparency = section_avg_loudness
		# Scale [-20, 0] to [50, 100]
		transparency = 50 * (1 - ((unscaled_transparency + 20) / 20)) + 100 * ((unscaled_transparency + 20) / 20)
		transparency = int(transparency)

		d = {}

		d["a"] = a
		d["b"] = b 
		d["h"] = h
		d["hue"] = hue
		d["saturation"] = saturation
		d["brightness"] = brightness
		d["transparency"] = transparency

		patterns.append(d)

	song_data["patterns"] = patterns

	return song_data


def main():
	script, artist, title = argv
	algorithm(artist, title)
	# get_song_data(artist, title)
	# collapse_sections(artist, title)

if __name__ == "__main__":
	main()