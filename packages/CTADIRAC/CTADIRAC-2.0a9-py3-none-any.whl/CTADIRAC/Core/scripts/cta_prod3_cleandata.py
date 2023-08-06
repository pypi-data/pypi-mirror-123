#!/usr/bin/env python
""" Simple data management script for PROD3 MC
    create DFC MetaData structure
    put and register files in DFC
"""

__RCSID__ = "f7b25c8 (2021-08-20 16:47:35 +0200) ARRABITO Luisa <arrabito@in2p3.fr>"

# DIRAC imports
import DIRAC
from DIRAC.Core.Base import Script
 
Script.setUsageMessage( '\n'.join( [ __doc__.split( '\n' )[1],
                                     'Usage:',
                                     '  %s one two' % Script.scriptName,
                                     'Arguments:',
                                     '  one: one',
                                     '\ne.g: %s ?' % Script.scriptName
                                     ] ) )

Script.parseCommandLine()

# Specific DIRAC imports
from CTADIRAC.Core.Workflow.Modules.ProdDataManager import ProdDataManager

####################################################
def cleanDataPROD3( args ):
    """ simple wrapper to remove PROD3 local files
    
    Keyword arguments:
    args -- a list of arguments in order []
    """
    datadir = args[0]
    pattern = args[1]
    catalogs = ['DIRACFileCatalog']
    
    prod3dm = ProdDataManager( catalogs )

    # ## Remove local files
    res = prod3dm.cleanLocalFiles( datadir, pattern )
    if not res['OK']:
      return res

    return DIRAC.S_OK()

####################################################
if __name__ == '__main__':
  
  DIRAC.gLogger.setLevel('VERBOSE')
  args = Script.getPositionalArgs()
  try:    
    res = cleanDataPROD3( args )
    if not res['OK']:
      DIRAC.gLogger.error ( res['Message'] )
      DIRAC.exit( -1 )
    else:
      DIRAC.gLogger.notice( 'Done' )
  except Exception:
    DIRAC.gLogger.exception()
    DIRAC.exit( -1 )
