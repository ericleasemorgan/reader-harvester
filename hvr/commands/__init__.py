# require
from hvr import *


# harvest html
@click.command()
def cmdBibliographics2Html() : bibliographics2Html()


# make bibliographics
@click.command()
def cmdRss2Bibliographics() : rss2Bibliographics()


# harvest rss
@click.command()
@click.argument( 'url' )
@click.argument( 'prefix' )
def cmdHarvestRss( url, prefix ) : harvestRSS( url, prefix )


# initialize
@click.command()
def cmdInitialize() :

	# configure
	success = '''
  The current working directory (%s) has been initialized.
'''
	failure = '''
  Something went wrong. Call Eric.
'''
	# require
	from pathlib import Path
	
	# initialize
	cwd = Path.cwd()
	
	# do the work
	if initialize() : click.echo( success % cwd, err=True ) 
	else : click.echo( failure, err=True )


# about
@click.command()
def cmdAbout() : 

	message = about()
	click.echo( message )

# version
@click.command()
def cmdVersion() : click.echo( version() )


