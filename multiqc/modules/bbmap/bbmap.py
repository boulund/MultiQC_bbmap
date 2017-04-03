#!/usr/bin/env python

""" MultiQC module to parse summary statistics output from BBMap tools """

from __future__ import print_function
from collections import OrderedDict
from itertools import chain
import json
import logging
import os
import re

from multiqc import config
from multiqc.modules.base_module import BaseMultiqcModule
from multiqc.plots import table, bargraph

# Import file parsers from submodules
from . import BaseComposition
from . import Quality
#from . import BaseQuality
#from . import AverageReadQuality
#from . import BoxQuality
#from . import ReadLength
#from . import ReadGCContent
from . import Statsfile

# Initialise the logger
log = logging.getLogger(__name__)

class MultiqcModule(BaseMultiqcModule):
    """ BBMap Tools is a suite of tools. This MultiQC module supports some
    outputs that these tools can produce but not all. BBMap output files are
    difficult to identify as there are no default filenames. These functions
    assume that anything up to the first dot in a filename that matches the
    MultiQC identification pattern constitutes the sample name. 
    """

    def __init__(self):

        # Initialise the parent object
        super(MultiqcModule, self).__init__(name='BBMap', anchor='bbmap',
                href='http://jgi.doe.gov/data-and-tools/bbtools/bb-tools-user-guide/',
                info="is a suite of RNA/DNA sequence pre-processing, assembly, alignment, and post-processing tools.")

        # Set up class objects to hold parsed data
        self.sections = list()
        self.general_stats_headers = OrderedDict()
        self.general_stats_data = dict()
        self.files_discovered = dict()

        # Parse BBMap output files
        self.files_discovered['bhist'] = BaseComposition.parse(self)
        self.files_discovered['qhist'] = Quality.parse(self)
        #self.files_discovered['qchist'] = BaseQuality.parse(self)
        #self.files_discovered['aqhist'] = AverageReadQuality.parse(self)
        #self.files_discovered['bqhist'] = BoxQuality.parse(self)
        #self.files_discovered['lhist'] = ReadLength.parse(self)
        #self.files_discovered['gchist'] = ReadGCContent.parse(self)
        self.files_discovered['statsfile'] = Statsfile.parse(self)

        num_samples = sum(self.files_discovered.values())
        if num_samples == 0:
            log.debug("Could not find any BBMap output files in {}".format(config.analysis_dir))
            raise UserWarning

        log.debug("Found %s BBMap output files", num_samples)
        #self.write_data_file(self.bbmap, 'multiqc_bbmap')

        # Add general stats to general stats table
        Statsfile.plot(self)

        # Create and add plots
        BaseComposition.plot(self)
        Quality.plot(self)
