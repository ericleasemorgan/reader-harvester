"""
a command-line tool
"""

# configure
ETC            = 'etc'
HTML           = 'html'
RSS            = 'rss'
VERSION        = '0.0.1'
BIBLIOGRAPHICS = 'bibliographics.tsv'
FILL           = 4

# require
import click


# read bibliographics and get corresponding HTML
def bibliographics2Html() :

	# configure
	EXTENSION = '.html'

	# require
	from pathlib import Path
	import pandas as pd
	import requests
	import sys

	# initialize
	cwd            = Path.cwd()
	bibliographics = pd.read_csv( cwd/ETC/BIBLIOGRAPHICS, sep='\t' )
	items          = len( bibliographics )

	# process each bibliographic item
	for index, row in bibliographics.iterrows() :

		# re-initialize output filename
		file = cwd/HTML/( row[ 'file' ] )
		
		# don't redo the work
		if not file.exists() :
	
			# re-initialize
			url = row[ 'url' ]
		
			# get the article
			message  = ( 'Getting %s (item #%s of %s)\r' % ( url, index, items ) )
			sys.stderr.write( message )
			response = requests.get( url )
	
			# check for success
			if response.ok : 
	
				# save the result
				with open( file, 'w' ) as handle : handle.write( response.text )


# read RSS and save bibliographics
def rss2Bibliographics() :

	# configure
	NAMESPACES = { 'dc': 'http://purl.org/dc/elements/1.1/' }
	HEADER     = [ 'item', 'file', 'author', 'title', 'date', 'abstract', 'url' ]
	MONTHS     = { 'Jan': '01','Feb': '02','Mar': '03','Apr': '04', 'May': '05','Jun': '06','Jul': '07','Aug': '08', 'Sep': '09','Oct': '10','Nov': '11','Dec': '12' }
	DATE       = 'Wed, 15 Apr 2015 10:54:50 +0000'
	PATTERN    = '*.xml'
	EXTENSION  = '.html'

	# require
	from pathlib import Path
	import glob
	import xml.etree.ElementTree as ET
	
	# initialize
	cwd            = Path.cwd()
	files          = glob.glob( str( cwd/RSS/( PATTERN ) ) )
	bibliographics = '\t'.join( HEADER ) + '\n'
	index          = 0

	# process each found file
	for file in files :
		
		# open and re-initialize
		tree = ET.ElementTree( file=file )
		root = tree.getroot()

		# process each item
		for item in root.findall( './channel/item' ) :

			# parse
			author   = item.find( './dc:creator', NAMESPACES ).text
			title    = item.find( './title' ).text
			date     = item.find( './pubDate' ).text
			abstract = item.find( './description' ).text
			url      = item.find( './link' ).text

			# create a key
			index += 1
			item   = str( index ).zfill( FILL )
		
			# create a file name
			file = item + EXTENSION
			
			# normalize the abstract
			abstract = abstract.replace( '\n', ' ' )
			abstract = abstract.replace( '\t', ' ' )
		
			# normalize the date; make the date sortable
			if not date : date = DATE
			parts = date.split()
			year  = parts[ 3 ]
			month = MONTHS[ parts[ 2 ] ]
			day   = parts[ 1 ]
			date  = '-'.join( [ year, month, day ] )
				
			# update
			bibliographics = bibliographics + '\t'.join ( [ str( item ), file, author, title, date, abstract, url ] ) + '\n'

		# save
		with open( cwd/ETC/BIBLIOGRAPHICS, 'w' ) as handle : handle.write( bibliographics )


# cache RSS
def harvestRSS( url, prefix ) :

	# configure
	FEED      = '/feed/?paged=##NUMBER##'
	EXTENSION = '.xml'
	LIMIT     = 10
	
	# require
	from pathlib import Path
	import requests
	import sys
	
	# initialize
	index = 0
	cwd   = Path.cwd()
		
	# repeat forever
	while ( True ) :

		# increment
		index += 1

		# re-initialize
		feed = url + FEED
		feed = feed.replace( '##NUMBER##', str( index ) )
		file = prefix + '-' + str( index ).zfill( FILL ) + EXTENSION
		file = cwd/RSS/file
				
		# debug
		sys.stderr.write( '\t'.join( [ feed, str( file ) ] ) + '\n' )

		# request the url
		response = requests.get( feed )

		# check for error; done
		if not response.ok : break

		# save response
		with open( file, 'w' ) as handle : handle.write( response.text )
		
		# conditionally continue
		if index >= LIMIT : break


# initialize the file system
def initialize() :

	# require
	from pathlib import Path
	
	# initialize
	cwd  = Path.cwd()
	
	# do the work, or at least try
	try :
		Path.mkdir( cwd/ETC,  exist_ok=True )
		Path.mkdir( cwd/RSS,  exist_ok=True )
		Path.mkdir( cwd/HTML, exist_ok=True )
		return True
	except : return False


# describe this library
def about() :

	message = '''
  This is Reader Harvester, a set of Python libraries and a
  command-line tool for locally caching content from the 'Net in a
  way that it can be easily used by another tool -- the Reader
  Toolbox
'''

	return message

	
# get version number
def version() : return VERSION

