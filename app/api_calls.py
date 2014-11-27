# -*- coding: utf-8 -*-

import json, os, requests
from sys import argv

api_key = os.environ.get("ECHO_NEST_API_KEY")

def get_song_data(artist=None, title=None):
	"""
	Takes up to two optional strings (artist name, song title) and returns a dictionary of song information.
	"""

	# Get general song info
	#######################

	if not artist:

		params = {"api_key":api_key, "results":10, "limit": True, "title":title, "bucket":["audio_summary", "id:spotify", "tracks"]}

	if not title:

		params = {"api_key":api_key, "results":10, "limit": True, "artist":artist, "bucket":["audio_summary", "id:spotify", "tracks"]}
	else:

		params = {"api_key":api_key, "results":10, "limit": True, "artist":artist, "title":title, "bucket":["audio_summary", "id:spotify", "tracks"]}

	try:
		r = requests.get("http://developer.echonest.com/api/v4/song/search", params=params)

	except requests.exceptions.RequestException as e:
		return "I'm sorry, that song is not available. Please try a different one."

	results = json.loads(r.content)
  
	songs = results["response"].get("songs", [])

	song_data = {}

	# Filter for a result that has track info and a Spotify track uri (used in web player)
	for song in songs:
		tracks = song["tracks"]
		if tracks == []:
			continue
		else:
			for track in tracks:

				if "foreign_id" in track:
					song_data["spotify_track_uri"] = track["foreign_id"]
					break
				else:
					continue
		

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

			# Lowercase artist name and song title
			song_data["artist_name"] = song_data["artist_name"].lower()
			song_data["title"] = song_data["title"].lower()

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

			######COMMENT THIS OUT?#######
			break


	if not song_data:
		return {}

	return song_data

def collapse_sections(artist=None, title=None):

	song_data = get_song_data(artist, title)

	if not song_data:
		return None

	# Get analyses of song sections
	###########################################
	analysis_url = str(song_data["analysis_url"])
	print 0, analysis_url

	r = requests.get(analysis_url)

	if r.status_code != 200:
		return "Error accessing analysis url. Status code %d" % r.status_code

	results = json.loads(r.content)

	# print 0, results.url

	#TO DO: Build in handler in the case that sections data is limited.
	sections = results["sections"]


	# Collapse song sections
	###########################################

	collapsed = {}
	for i in range(len(sections)):
		key = sections[i]["key"]
		mode = sections[i]["mode"]
		time_sig = sections[i]["time_signature"]
		collapsed[(key, mode, time_sig)] = collapsed.setdefault((key, mode, time_sig), [])
		collapsed[(key, mode, time_sig)].append(sections[i])

	new_collapsed = {}
	# Get total duration for each collapsed section
	for key, value in collapsed.iteritems():
		total_duration = 0
		
		for item in value:
			total_duration += item["duration"]
		
		total_duration = int(round(total_duration))
		
		# Recreate key so that it starts with total duration
		key = list(key)
		key.insert(0, total_duration)
		key = tuple(key)

		# Key is now (total_duration, key, mode, time sig)
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

def scaler(x, a, b, c, d):
	"""
	Takes a number x within range [a, b] and scales it according to the desired range [c, d]
	"""

	scaled = c * (1 - ((x - a) / (b - a))) + d * (((x - a) / (b - a)))

	return scaled

def algorithm(artist=None, title=None):
	
	song_data = collapse_sections(artist, title)
	
	if not song_data:
		
		return None

	song_energy = song_data["energy"]

	song_valence = song_data["valence"]

	
	sections = []
	

	patterns = []
	
	###########################################################
	# Scale tempo to rotation duration (inversely proportional)
	###########################################################

	unscaled_rotation_duration = song_data["tempo"]

	# Set min/mix
	if unscaled_rotation_duration < 70:
		unscaled_rotation_duration = 70
	if unscaled_rotation_duration > 200:
		unscaled_rotation_duration = 200

	rotation_duration = scaler(unscaled_rotation_duration, 70, 200, 100, 5)

	song_data["rotation_duration"] = rotation_duration


	###########################################################
	# Scale song duration to radius of large circle (a)
	###########################################################

	unscaled_a = float(song_data["duration"]) 
	
	# Set mix/max
	if unscaled_a < 100:
		unscaled_a = 100
	if unscaled_a > 600:
		unscaled_a = 600

	a = scaler(unscaled_a, 100, 600, 500, 900)


###


	value_list = song_data["value_list"]
	# print value_list

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


		sections_dict = {}

		sections_dict["duration"] = section_duration
		sections_dict["loudness"] = section_avg_loudness 
		sections_dict["mode"] = section_mode
		sections_dict["key"] = section_key





		# Duration of section determines radius of smaller circle ("b")
		unscaled_b = section_duration

		# Set minimum and maximum section duration (5 min; a-10 max)
		if unscaled_b < 5:
			unscaled_b = 5
		if unscaled_b > (unscaled_a - 10):
			unscaled_b = (unscaled_a - 10)		

		# Scale as follows: # [5, (unscaled_a-10)] => [275, 675]
		b = 275 * (1 - ((unscaled_b - 5) / ((unscaled_a - 10) - 5))) + 675 * ((unscaled_b - 5) / ((unscaled_a - 10) - 5))

		# Difference between "a" and "b" determines distance between center of smaller circle and point P ("h")
		h = a - b

		# Section key determines hue
		unscaled_hue = section_key

		# Scale as follows [0, 11] => [0, 330]
		
		# hue = 0 * (1 - (unscaled_hue / 11.0)) + 330 * (unscaled_hue / 11.0 )
		hue = 330 * (unscaled_hue / 11.0 )
		hue = int(hue)



		# [0, 2] to [0, 50]
		unscaled_saturation = song_energy + song_valence

		saturation = 40 * ((unscaled_saturation) / 2)

		brightness = 100
		
		unscaled_transparency = section_avg_loudness
		# Scale [-20, 0] to [50, 100]
		transparency = 50 * (1 - ((unscaled_transparency + 20) / 20)) + 100 * ((unscaled_transparency + 20) / 20)
		transparency = int(round(transparency))

		patterns_dict = {}

		patterns_dict["a"] = a
		patterns_dict["b"] = b 
		patterns_dict["h"] = h
		patterns_dict["hue"] = hue
		patterns_dict["saturation"] = saturation
		patterns_dict["brightness"] = brightness
		patterns_dict["transparency"] = transparency

		patterns.append(patterns_dict)

		# Convert colors to hex value for use in HTML

		def hsv2hsl(hue,sat,val):

			l = int(round((2 - sat / 100.0) * val / 2))
			
			# Avoid division by zero
			if l == 0:
				l == 0.1
			elif l == 100:
				l = 99.9
	
			if l < 50:
				temp = l * 2.0
				print "TEMP", temp
	
			else:
				temp = 200 - l * 2.0
				print "TEMP", temp
			h = hue
			s = int(round(sat * val / temp))
			return [h, s, l]

		hsla = hsv2hsl(hue, saturation, brightness)
		hsla.append(transparency/100.0)

		sections_dict["hsla"] = hsla
		
		sections.append(sections_dict)

	song_data["sections"] = sections
	song_data["patterns"] = patterns


	return song_data


def main():
	script, artist, title = argv
	algorithm(artist, title)
	# get_song_data(artist, title)
	# collapse_sections(artist, title)

if __name__ == "__main__":
	main()