#!/usr/bin/python3

import bibtexparser
import argparse #parse command line arguments

def run(args):
	print (args.FileInput)
	print (args.FileOutput)
	print (args.OutputName)

	#Load and parse .bib file
	with open(args.FileInput) as bibtex_file:
		bib_database = bibtexparser.load(bibtex_file)

	entries = bib_database.entries
	
	(mapping,mKeywords) = generateMap(entries)
	#print(mapping)
	#Maybe before generating the result verify if every entrie has
	#the tag title and keyword
	generateResultFile(entries, mapping, mKeywords,
					   args.OutputName, args.FileOutput)



def generateResultFile(entries, mapping, mKeywords, name, path):

	with open(path+name+'.csv', mode='w', encoding='utf-8') as csv:
		writeHeader(csv,mapping)
		for entrie in entries:
			csv.write(entrie['title']+";")

			#creates a list containing the numbers of the keywords
			keywords = map(str.strip,entrie['keyword'].split(','))
			keywordPos = []

			for keyword in keywords:
				keywordPos.append(mapping[keyword])

			for i in range(0, mKeywords):
				if i in keywordPos:
					csv.write('1;')
				else:
					csv.write('0;')

			csv.write('\n')


def writeHeader(csv, mapping):
	csv.write(';')
	for k,_ in sortMapByValues(mapping):
		csv.write(k+';')
	csv.write('\n')

def generateMap(entries):
	"""
		Receives as input the entries available on the .bib file
		and returns a mapping from Keyword to a number.
		Additionaly the total number of keywords is also returned.
		The number represents the keyword position in the final csv file
		return (resMap, maxKeywords)
	"""
	pos = 0
	resMap = {}

	for entrie in entries:
			#If the entrie contains a keyword tag
		if "keyword" in entrie:
			#create a list of keywords
			keywords = map(str.strip,entrie["keyword"].split(","))

			#For each keyworc check if it is in the dictionary, if not
			# then add it
			for keyword in keywords:
				if keyword not in resMap:
					resMap[keyword] = pos
					pos += 1

	return (resMap,pos)



def sortMapByValues(entries):
	return ((k, entries[k]) for k in sorted(entries, key=entries.get))

def cmdLineArguments():
	desc = """Converts a .bib file to a .csv to be used by conexp.
              It acepts a .bib file input path and an ouput path directory 
              and name for the result csv.
              e.g.:
              conexpfrombib.py ~/dissertation/dissertation.bib output 
              	~/dissertation/

			"""
	parser = argparse.ArgumentParser(description=desc)

	parser.add_argument("FileInput",  help=".bib input file path")
	parser.add_argument("OutputName", help=".csv output file name")
	parser.add_argument("FileOutput", help=".csv output file path")
	return parser.parse_args()




if __name__ == '__main__':
	print("This program is being run by itself")
	args = cmdLineArguments()
	run(args)
else:
	print("This program is being imported from another module")
