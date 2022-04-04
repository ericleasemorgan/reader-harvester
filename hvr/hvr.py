
# require
from hvr import *
from hvr.commands import cmdAbout
from hvr.commands import cmdVersion
from hvr.commands import cmdInitialize
from hvr.commands import cmdHarvestRss
from hvr.commands import cmdRss2Bibliographics
from hvr.commands import cmdBibliographics2Html


# initialize 
@click.group()
def hvr() : pass

# update the list of commands
hvr.add_command( cmdAbout,      name='about' )
hvr.add_command( cmdVersion,    name='version' )
hvr.add_command( cmdInitialize, name='initialize' )
hvr.add_command( cmdHarvestRss, name='harvest' )
hvr.add_command( cmdRss2Bibliographics, name='bibliographics' )
hvr.add_command( cmdBibliographics2Html, name='html' )

# do the work
if __name__ == '__main__' : hvr()
