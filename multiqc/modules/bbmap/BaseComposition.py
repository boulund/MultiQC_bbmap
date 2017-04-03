#!/usr/bin/env python

""" MultiQC submodule to parse output from BBMap BaseComposition statistics. """ 

# TODO:
# - Handle compressed files, some pointers:
#   https://github.com/ewels/MultiQC/blob/master/multiqc/modules/fastqc/fastqc.py#L47
#   Full file path would be `os.path.join(f['root'], f['fn'])`

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
    """ Find and parse BBMAP BaseComposition statistics files (bhist).
    """

    # Set up dictionaries to store results
    self.bbmap_BaseComposition_data = defaultdict(partial(defaultdict, dict))

    # Identify logs and parse data
    for f in self.find_log_files(config.sp['bbmap']['bhist'], filehandles=True):
        # Get sample name
        sample_name = f['fn'].split(".bhist")[0]

        firstline = f['f'].readline()
        if not firstline.startswith("#Pos\tA\tC\tG\tT\tN"):
            # Skip to the next file, this appears to be something else
            log.debug("Parse error for: %s, first line does not match bhist format.", f['fn'])
            continue

        for line in f['f']:
            try:
                splitline = line.split()
                pos = int(splitline[0])
                A, C, G, T, N = map(float, splitline[1:])
            except ValueError:
                log.warning("Parsing error for %s, the offending line was: %s", f['fn'], line)
                break
            self.bbmap_BaseComposition_data[sample_name]["A"][pos] = A
            self.bbmap_BaseComposition_data[sample_name]["C"][pos] = C
            self.bbmap_BaseComposition_data[sample_name]["G"][pos] = G
            self.bbmap_BaseComposition_data[sample_name]["T"][pos] = T
            self.bbmap_BaseComposition_data[sample_name]["N"][pos] = N
        else:
            self.add_data_source(f)

    return len(self.bbmap_BaseComposition_data.keys())
    

def plot(self):
    """ Plot the data using line plots.
    """

    data = defaultdict(dict)
    for sample_name, nucleotide_data in self.bbmap_BaseComposition_data.items():
        for nucleotide, pos in nucleotide_data.items():
            for x, y in pos.items(): 
                data[sample_name + "." + nucleotide][x] = y

    config = {"id": "bbmap_basecomposition_plot"}

    self.sections.append({
        'id': 'bbmap_basecomposition',
        "name": "Base Composition",
        "anchor": "bbmap-base-composition",
        "content": linegraph.plot(data, config)
        })
