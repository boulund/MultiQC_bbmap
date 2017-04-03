#!/usr/bin/env python

""" MultiQC submodule to parse output from BBMap Quality statistics. """ 

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
    """ Find and parse BBMAP Quality statistics files (qhist).
    """

    # Set up dictionaries to store results
    self.bbmap_Quality_data = defaultdict(partial(defaultdict, dict))

    # Identify logs and parse data
    for f in self.find_log_files(config.sp['bbmap']['qhist'], filehandles=True):
        # Get sample name
        sample_name = f['fn'].split(".qhist")[0]

        firstline = f['f'].readline()
        headers = "#BaseNum\tRead1_linear\tRead1_log".split()
        if not firstline.startswith('\t'.join(headers)):
            # Skip to the next file, this appears to be something else
            log.debug("Parse error for: %s, first line does not match qhist format.", f['fn'])
            continue
        actual_headers = firstline.strip()[1:].split()
        for line in f['f']:
            try:
                splitline = line.split()
                basenum = int(splitline[0])
                data_values = list(map(float, splitline[1:]))
            except ValueError:
                log.warning("Parsing error for %s, the offending line was: %s", f['fn'], line)
                break

            for idx, column in enumerate(actual_headers[1:]):
                self.bbmap_Quality_data[sample_name][column][basenum] = data_values[idx]
        else:
            self.add_data_source(f)

    return len(self.bbmap_Quality_data.keys())
    

def plot(self):
    """ Plot the data using line plots.
    """

    data = defaultdict(dict)
    for sample_name, nucleotide_data in self.bbmap_Quality_data.items():
        for nucleotide, pos in nucleotide_data.items():
            for x, y in pos.items(): 
                data[sample_name + "." + nucleotide][x] = y

    config = {"id": "bbmap_quality_plot"}

    self.sections.append({
        "id": "bbmap_quality",
        "name": "Quality",
        "anchor": "bbmap-quality",
        "content": linegraph.plot(data, config)
        })

