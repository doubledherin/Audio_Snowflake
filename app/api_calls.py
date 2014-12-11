# -*- coding: utf-8 -*-

import json, os, requests
from sys import argv

api_key = os.environ.get("ECHO_NEST_API_KEY")

def get_matching_songs(artist=None, title=None):
	"""
	Takes one or two strings (artist name, song title) and returns a list of songs that match.

	(If neither artist or title are passed in, this function does not get called.)
	"""

	# Only the artist is passed in
	if not title:
		params = {"api_key":api_key, "results":100, "limit": True, "artist":artist, "bucket":["audio_summary", "id:spotify", "tracks"]}

	# Only the title is passed in
	elif not artist:
		params = {"api_key":api_key, "results":100, "limit": True, "title":title, "bucket":["audio_summary", "id:spotify", "tracks"]}

	# Both artist and title are passed in
	else:
		params = {"api_key":api_key, "results":100, "limit": True, "artist":artist, "title":title, "bucket":["audio_summary", "id:spotify", "tracks"]}

	try:
		r = requests.get("http://developer.echonest.com/api/v4/song/search", params=params)

	except requests.exceptions.RequestException as e:
		return "I'm sorry, that song is not available. Please try a different one."

	results = json.loads(r.content)



	songs = results["response"].get("songs", [])

	return songs


def get_song_data(songs):
	"""
	Takes a list of songs and returns a dictionary of song data 
	for the 1st song that meets the criteria.
	"""

	# Displays "no song available" message if songs is an empty list
	if not songs:
		
		song_data = None
		return song_data

	song_data = {}
	
	# Filter for a song that has track info 
	for song in songs:

		tracks = song["tracks"]

		if tracks == []:
			continue

		# Filter for a track that has a Spotify track uri (used for the web player)	
		else:
			for track in tracks:

				if "foreign_id" in track:
					song_data["spotify_track_uri"] = track["foreign_id"]
					break
				
				else:
					continue
		
			###########################################
			# Get general song info
			###########################################
			

			for key, value in song.iteritems():

				# Skip unneeded items
				if key == "tracks" or key == "artist_foreign_ids":
					continue

				# Skip audio_summary, which we're getting in the next for loop
				if key == "audio_summary":
					continue
				
				# Rename "id" key for clarity purposes
				if key == "id":
					key = "song_id"

				song_data[key] = value

			# Lowercase artist name and song title for database storage
			song_data["artist_name"] = song_data["artist_name"].lower()
			song_data["title"] = song_data["title"].lower()

			###########################################
			# Get detailed song info
			###########################################	
			try:
				audio_summary = song["audio_summary"]
				
			except:
				"ERROR: No audio summary for %s" % song_data["title"]

			for key, value in audio_summary.iteritems():

				# round to no more than 3 decimal places
				if type(value) == float:
					value = round(value, 3)

				song_data[key] = value

	# Add sections to song_data
	section_list = get_sections(song_data)
	song_data["section_list"] = section_list

	if not song_data:

		return {}

	for key, value in song_data.iteritems():

		return song_data

def get_sections(song_data):
	"""
	Takes a dictionary of song data and returns a list of data on sections.
	"""

	if not song_data or not song_data["analysis_url"]:
		
		return None

	analysis_url = str(song_data["analysis_url"])

	r = requests.get(analysis_url)

	if r.status_code != 200:
		return "Error accessing analysis url. Status code %d" % r.status_code

	results = json.loads(r.content)

	#TO DO: Build in handler in the case that sections data is limited.
	section_results = results["sections"]


	song_data["collapsed_sections"] = collapse_sections(section_results)
	
	return song_data

def collapse_sections(section_results):
	"""
	Takes a list of sections returns a collapsed/refined list of section data
	"""

	collapsed = {}

	# Get relevant attributes from each section in the section results
	for i in range(len(section_results)):

		key = section_results[i]["key"]
		mode = section_results[i]["mode"]
		time_sig = section_results[i]["time_signature"]
		
		# Dedupe sections that have the same key, mode, and time signature
		collapsed[(key, mode, time_sig)] = collapsed.setdefault((key, mode, time_sig), [])
		
		# Add deduped section to list
		collapsed[(key, mode, time_sig)].append(section_results[i])


	new_collapsed = {}

	# Get sum-total duration for each collapsed section
	for key, value in collapsed.iteritems():
		total_duration = 0
		
		for item in value:
			total_duration += item["duration"]
		
		total_duration = int(round(total_duration))
		
		# Recreate key so that it starts with the total duration
		key = list(key)
		key.insert(0, total_duration)
		key = tuple(key)

		# Key will now be (total_duration, key, mode, time sig)
		new_collapsed[key] = value

	# For each collapsed section, collapse list of values into averages
	newer_collapsed = {}

	items = new_collapsed.items()

	for key, value in items:
		newer_collapsed[key] = {}

		# Get totals for each item in a collapsed section's values
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
		
		# Put the totals into a list
		totals = [total_confidence, total_key_confidence, total_mode_confidence, total_time_signature_confidence, total_tempo, total_loudness]

		# Yay list comprehension
		averages = map(lambda x: round(x / len(value), 3), totals)

		# Add the averaged values to the newer_collapsed dictionary
		newer_collapsed[key]["avg_confidence"] = averages[0]
		newer_collapsed[key]["avg_key_confidence"] = averages[1]
		newer_collapsed[key]["avg_mode_confidence"] = averages[2]
		newer_collapsed[key]["avg_time_signature_confidence"] = averages[3]
		newer_collapsed[key]["avg_tempo"] = averages[4]
		newer_collapsed[key]["avg_loudness"] = averages[5]

	# Shrink to 5 or fewer sections
	while len(newer_collapsed) > 5:
		
		# Remove item with the shortest duration
		sorted_keys = sorted(newer_collapsed.keys())
		shortest_duration = sorted_keys.pop(0)
		del newer_collapsed[shortest_duration]

	# Create list of dictionaries, each dictionary stores one section's data
	final_collapsed = []
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

		final_collapsed.append(d)

	return final_collapsed


def algorithm(artist=None, title=None):
	"""
	Takes an artist name and song title and returns a complete dictionary of song data
	"""
	songs = get_matching_songs(artist, title)
	song_data = get_song_data(songs)

	if not song_data:
		
		return None

	song_energy = song_data["energy"]

	song_valence = song_data["valence"]

	# This list will be passed to index.html through Jinja2 to create the legend
	sections = []
	
	# This list will be passed to processing to render the images
	patterns = []
	
	###########################################################
	# Scale tempo to rotation duration (inversely proportional)
	###########################################################

	unscaled_rotation_duration = song_data["tempo"]

	# Set min/max tempo (70, 200)
	if unscaled_rotation_duration < 70:
		unscaled_rotation_duration = 70
	if unscaled_rotation_duration > 200:
		unscaled_rotation_duration = 200

	rotation_duration = scaler(unscaled_rotation_duration, 70, 200, 100, 5)

	song_data["rotation_duration"] = rotation_duration


	###########################################################
	# Scale song's duration to radius of large circle (a)
	###########################################################

	unscaled_a = float(song_data["duration"]) 
	
	# Set mix/max song duration (100, 600)
	if unscaled_a < 100:
		unscaled_a = 100
	if unscaled_a > 600:
		unscaled_a = 600

	a = scaler(unscaled_a, 100, 600, 500, 900)

	# Extract relevant section information from song_data dictionary
	collapsed_sections = song_data["collapsed_sections"]

	for section in collapsed_sections:

		v = section.values()

		section_duration = v[0]["duration"]
		section_key = v[0]["key"]
		section_mode = v[0]["mode"]
		section_avg_loudness = v[0]["avg_loudness"]

		###########################################################
		# Scale section's duration to radius of small circle (b)
		###########################################################
		
		unscaled_b = float(section_duration)

		# # Set mix/max section duration (in seconds; 5 min, (a-10) max)
		if unscaled_b < 5:
			unscaled_b = 5
		if unscaled_b > (unscaled_a - 10):
			unscaled_b = (unscaled_a - 10)		

		b = scaler(unscaled_b, 5, unscaled_a - 10, 275, 675)
		
		###########################################################
		# Map difference between a and b to distance h
		###########################################################
		
		h = a - b

		###########################################################
		# Scale section's key to hue 
		###########################################################
		
		# Key is an int from 0 to 11 that maps to the chromatic scale (C to B)
		unscaled_hue = section_key

		# Max hue is 330 to avoid two reds
		hue = int(round(scaler(unscaled_hue, 0, 11.0, 0, 330.0)))
		
		###########################################################
		# Scale sum of song's energy and valence to saturation
		###########################################################

		# Min/max of energy + valence is [0, 2]
		unscaled_saturation = song_energy + song_valence

		# Max saturation set at 40 for aesthetics
		saturation = scaler(unscaled_saturation, 0, 2, 0, 40.0)

		###########################################################
		# Keep brightness at a constant max 
		###########################################################

		brightness = 100
		
		###########################################################
		# Scale section's loudness to opacity 
		###########################################################

		unscaled_opacity = section_avg_loudness

		# Set min/max loudness [-20, 0]
		if unscaled_opacity < -20:
			unscaled_opacity = -20
		if unscaled_opacity > 0:
			unscaled_opacity = 0

		# Min opacity set at 40 for visibility
		opacity = int(round(scaler(unscaled_opacity, -20, 0, 50, 100.0)))


		###########################################################
		# Add section's image-rendering information to patterns list 
		###########################################################
		patterns_dict = {}

		patterns_dict["a"] = a
		patterns_dict["b"] = b 
		patterns_dict["h"] = h
		patterns_dict["hue"] = hue
		patterns_dict["saturation"] = saturation
		patterns_dict["brightness"] = brightness
		patterns_dict["opacity"] = opacity

		patterns.append(patterns_dict)

		###########################################################
		# Add section's legend information to patterns list 
		###########################################################
		sections_dict = {}

		sections_dict["duration"] = section_duration
		sections_dict["loudness"] = section_avg_loudness 
		sections_dict["mode"] = section_mode
		sections_dict["key"] = section_key

		# Convert HSVa to HSLa for use in HTML/CSS
		hsla = hsv2hsl(hue, saturation, brightness)
		hsla.append(opacity/100.0)
		sections_dict["hsla"] = hsla
		
		sections.append(sections_dict)

	song_data["sections"] = sections
	song_data["patterns"] = patterns

	return song_data

def scaler(x, a, b, c, d):
	"""
	Takes a number x within range [a, b] and scales it according to the desired range [c, d]
	"""

	scaled = c * (1 - ((x - a) / (b - a))) + d * (((x - a) / (b - a)))

	return scaled

def hsv2hsl(hue,sat,val):
	"""
	Takes 3 numbers representing an HSV color and returns a list of 3 numbers representing the equivalent color as HSL
	"""


	l = int(round((2 - sat / 100.0) * val / 2))
	
	# Avoid division by zero
	if l == 0:
		l == 0.1
	elif l == 100:
		l = 99.9

	if l < 50:
		temp = l * 2.0
	else:
		temp = 200 - l * 2.0
	
	h = hue
	
	s = int(round(sat * val / temp))
	
	return [h, s, l]

def main():
	script, artist, title = argv
	algorithm(artist, title)
	# get_matching_songs(artist, title)
	# get_sections(artist, title)

if __name__ == "__main__":
	main()