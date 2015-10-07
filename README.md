META 16S rRNA Analysis Pipeline
===============================

John Conery  
META Center for Systems Biology  
University of Oregon

http://meta.uoregon.edu/

This project contains a set of Python scripts for managing applications 
used in an analysis pipeline for 16S rRNA genes.  The software was 
originally developed for microbial communities sampled from zebrafish 
but should be easily adapted for other microbial communities.

The distinguishing feature of this pipeline is the use of SQLite to 
manage the workflow.  After the first few stages reduce the data via
quality filtering and dereplication the sequence data and all the
derived information is saved in a single SQLite database file.  

Pipeline Stages
---------------
*db_setup.py*&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;initialize a new project  
*import_reads.py*&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;specify locations of .fastq files  
*assemble_pairs.py*&nbsp;&nbsp;&nbsp;&nbsp;combine paired ends into single sequences  
*remove_duplicates.py*&nbsp;&nbsp;dereplication  
*filter_host.py*&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;filter host sequences from assembled pairs  
*map_reference.py*&nbsp;&nbsp;&nbsp;&nbsp;find known sequences to seed clusters  
*form_otus.py*&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;clustering  
*filter_chimeras.py*&nbsp;&nbsp;&nbsp;identify chimeric sequences  
*map_otus.py*&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;assign sequences to clusters  
*classify.py*&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;taxonomic classification of clusters    

Data Analysis
-------------
*abundance.py*&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;group data by taxonomic classifications  
*print_abundance.py*&nbsp;&nbsp;&nbsp;print abundances in CSV format  
*summarize.py*&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;print table sizes  

Scripts for Comparing Databases
-------------------------------
*compare_clusters.py*&nbsp;&nbsp;&nbsp;find clusters identified in two databases  
*compare_members.py*&nbsp;&nbsp;&nbsp;find sequences assigned to different clusters  
*compare_otus.py*&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;compare taxonomic classes in two databases  

Python Modules and Other Scripts 
--------------------------------
*FASTA.py*&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;class definition for FASTA sequences  
*FASTQ.py*&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;class definition for FASTQ sequences  
*fstats.py*&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;print statistics about FASTA or FASTQ file  
*common.py*&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;functions used by most scripts  
*config.py*&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;paths to external applications  
*gref.py*&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;print sequences matching a pattern  
*make_script.py*&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;generate a script to run the pipeline  
*print_as_fastq.py*&nbsp;&nbsp;&nbsp;&nbsp;print a sequence table in FASTQ format  

Deprecated
----------
*quality_filter.py*&nbsp;&nbsp;&nbsp;&nbsp;subsumed by assemble_pairs  

