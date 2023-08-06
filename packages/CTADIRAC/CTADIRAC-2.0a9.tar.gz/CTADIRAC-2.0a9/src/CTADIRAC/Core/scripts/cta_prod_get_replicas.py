#!/usr/bin/env python

__RCSID__ = "$Id$"

# generic imports
from multiprocessing import Pool

# DIRAC imports
from DIRAC.Core.Base import Script

Script.setUsageMessage("""
Bulk get replicas from a list of lfns
Usage:
   %s <ascii file with lfn list>

""" % Script.scriptName)

Script.parseCommandLine(ignoreErrors=True)

from DIRAC import gLogger
from DIRAC.Resources.Catalog.FileCatalog import FileCatalog
from CTADIRAC.Core.Utilities.tool_box import read_lfns_from_file

fc = FileCatalog()

def getReplicas(lfn):
  res = fc.getReplicas(lfn)
  if not res['OK']:
    gLogger.error('Failed to replicas for lfn', lfn)
    return res['Message']
  gLogger.notice(res['Value']['Successful'][lfn])

if __name__ == '__main__':

  args = Script.getPositionalArgs()
  if len(args) > 0:
    infile = args[0]
  else:
    Script.showHelp()

  infileList = read_lfns_from_file(infile)
  p = Pool(1)
  p.map(getReplicas, infileList)
