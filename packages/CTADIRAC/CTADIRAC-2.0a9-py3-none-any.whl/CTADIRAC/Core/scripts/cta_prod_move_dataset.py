#!/usr/bin/env python
'''
Move a dataset distributed on a number of production disk SEs
('DESY-ZN-Disk', 'LPNHE-Disk', 'CNAF-Disk', 'CYF-STORM-Disk','LAPP-Disk', 'CEA-Disk', 'CC-IN2P3-Disk')
to a given SE (disk or tape) to be passed as an argument, e.g. CC-IN2P3-Tape

To do: evntual rename the script to : 'cta-prod-move-dataset'

    J. Bregeon, L. Arrabito November 2020
    bregeon@in2p3.fr, arrabito@in2p3.fr
'''

__RCSID__ = "$Id$"


import DIRAC
from DIRAC import gLogger
from DIRAC.Core.Base import Script
from DIRAC.Resources.Catalog.FileCatalogClient import FileCatalogClient
from DIRAC.TransformationSystem.Client.TransformationClient import TransformationClient
from DIRAC.TransformationSystem.Utilities.ReplicationTransformation import createDataTransformation


def get_dataset_info(dataset_name):
  """ Return essential dataset information
      Name, number of files, total size and meta query
  """
  fc = FileCatalogClient()
  res = fc.getDatasets(dataset_name)
  if not res['OK']:
    gLogger.error(res['Message'])
    DIRAC.exit(-1)
  dataset_dict = res['Value']
  res = dataset_dict['Successful'][dataset_name][dataset_name]
  number_of_files = res['NumberOfFiles']
  meta_query = res['MetaQuery']
  total_size = res['TotalSize']
  return (dataset_name, number_of_files, total_size, meta_query)


#########################################################
if __name__ == '__main__':
  Script.setUsageMessage(
      '\n'.join(
          [
              __doc__.split('\n')[1],
              'Usage:',
              '  %s <dataset name> <dest SE>' %
              Script.scriptName,
              'Optional arguments:',
              '  <group size>: size of the transformation (default=1)',
              '  <tag>: tag added to the transformation name',
              '\n\ne.g: %s Prod4_Paranal_gamma_North_20deg_SSTOnly_MC0 CC-IN2P3-Tape 100 v1' %
              Script.scriptName,
          ]))

  Script.parseCommandLine(ignoreErrors=True)
  argss = Script.getPositionalArgs()
  if len(argss) < 2:
    Script.showHelp()
  dataset_name = argss[0]
  dest_se = argss[1]
  extra_tag = ""
  group_size = 1
  if len(argss) > 2:
    group_size = argss[2]
  if len(argss) == 4:
    extra_tag = argss[3]

  tc = TransformationClient()

  # Check input data set information
  name, n_files, size, meta_query = get_dataset_info(dataset_name)
  gLogger.notice('Found dataset %s with %d files.' % (name, n_files))
  gLogger.notice(meta_query)
  # choose a metaKey
  meta_key = 'site'
  meta_value = meta_query['site']
  tag = dataset_name.replace(meta_value, extra_tag)

  do_it = True
  # To do: replace hard coded SE with SE read from CS
  se_list = ['DESY-ZN-Disk', 'LPNHE-Disk', 'CNAF-Disk', 'CYF-STORM-Disk',
             'LAPP-Disk', 'CEA-Disk', 'CC-IN2P3-Disk']

  # create Transformation
  data_ts = createDataTransformation(flavour='Moving',
                                     targetSE=dest_se,
                                     sourceSE=se_list,
                                     metaKey=meta_key,
                                     metaValue=meta_value,
                                     extraData=meta_query,
                                     extraname=tag,
                                     groupSize=int(group_size),
                                     plugin='Broadcast',
                                     tGroup=None,
                                     tBody=None,
                                     enable=do_it,
                                     )
