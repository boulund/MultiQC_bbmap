---
Name: BBMap
URL: http://jgi.doe.gov/data-and-tools/bbtools/bb-tools-user-guide/
Description: >
	BBMap is a suite of pre-processing, assembly, alignment, and statistics
	tools for DNA/RNA sequencing reads.
---

The BBMap module analyses summary statistics from the 
[BBMap](http://jgi.doe.gov/data-and-tools/bbtools/bb-tools-user-guide/) suite of tools. 
The module analyses data in these BBMap tools' output files:
    bhist=<file>        Base composition histogram by position.  
    qhist=<file>        Quality histogram by position.           
    qchist=<file>       Count of bases with each quality value.  
    aqhist=<file>       Histogram of average read quality.       
    bqhist=<file>       Quality histogram designed for box plots.
    lhist=<file>        Read length histogram.                   
    gchist=<file>       Read GC content histogram.          
	statsfile=<file>    Mapping statistics are printed here.

The expected filenames of these files should all end with `.<option_name>.txt`
or `.<option_name>.txt.gz`, e.g. `SAMPLE_NUMBER_1.bhist.txt` for the base
composition histogram.
Additional information on the BBMap tools is available on 
[SeqAnswers](http://seqanswers.com/forums/showthread.php?t=41057)
