from lxml import objectify
import jsonpickle as json
import os
import re


class Logs:
	def __init__(self, log, final):
		self.log = log
		self.final = final


def load(logDir):
	print("Loading logs...")

	records = []
	for (dirpath, dirnames, filenames) in os.walk(logDir):
		for file in filenames:
			if file != "final.json":
				records.append(dirpath + os.sep + file)

	log = []
	for record in records:
		record_file = open(record, "r")
		dump = record_file.read()
		sim = json.loads(dump)
		log.append(sim)

	log.sort(key=lambda x: x['time_ms'])

	print("Loading logs...done")

	# return Logs(log, loadFinal(logDir))
	return Logs(log, None)

	# def loadFinal(logDir):
	#	final = objectify.parse(logDir + os.sep + "final.xml").getroot()
	#	return final
