#!/usr/bin/env python

""" MultiQC submodule to parse output from BBMap Statsfile statistics. """ 

from collections import OrderedDict, defaultdict
from functools import partial
import logging
import os
import re

from multiqc import config
from multiqc.plots import linegraph

# Initalize logger
log = logging.getLogger(__name__)

def parse(self):
    """ Identify and parse BBMap Statsfile files (statsfile).
    """

    # Set up dictionaries to store results
    self.bbmap_Statsfile_data = defaultdict(dict)

    # Identify logs and parse data
    for f in self.find_log_files(config.sp['bbmap']['statsfile'], filehandles=True):
        # Get sample name
        sample_name = f['fn'].split(".statsfile")[0]

        lines = f['f'].readlines()
        if not lines[0].startswith("Reads Used:"):
            # Skip to the next file, this appears to be something else
            log.debug("Parse error for: %s, first line does not match statsfile format.", f['fn'])
            continue
        reads_total = int(lines[0].strip().split('\t')[1])
        self.bbmap_Statsfile_data[sample_name]["Reads_total"] = reads_total
        
        read1_mapped = float(lines[21].strip().split('\t')[1].strip(" %"))
        read1_unambiguous = float(lines[22].strip().split('\t')[1].strip(" %"))
        read1_low_quality = float(lines[24].strip().split('\t')[1].strip(" %"))
        self.bbmap_Statsfile_data[sample_name]["Read1_mapped"] = read1_mapped
        self.bbmap_Statsfile_data[sample_name]["Read1_unambiguous"] = read1_unambiguous
        self.bbmap_Statsfile_data[sample_name]["Read1_low_quality"] = read1_low_quality

        try:
            read2_mapped = float(lines[40].strip().split('\t')[1].strip(" %"))
            read2_unambiguous = float(lines[41].strip().split('\t')[1].strip(" %"))
            read2_low_quality = float(lines[43].strip().split('\t')[1].strip(" %"))
            self.bbmap_Statsfile_data[sample_name]["Read2_mapped"] = read2_mapped
            self.bbmap_Statsfile_data[sample_name]["Read2_unambiguous"] = read2_unambiguous
            self.bbmap_Statsfile_data[sample_name]["Read2_low_quality"] = read2_low_quality
        except IndexError:
            pass #  No paired end data; file probably from single reads 

        self.add_data_source(f)

    return len(self.bbmap_Statsfile_data.keys())
    

def plot(self):
    """ Visualize the data using a table.
    """

    self.general_stats_addcols(self.bbmap_Statsfile_data)

