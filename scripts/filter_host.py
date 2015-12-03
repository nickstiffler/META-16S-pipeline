#! /usr/bin/env python3

# Run bowtie to filter host genome contamination

# John Conery / Kevin Xu Junjie / Nicholas Stiffler
# University of Oregon
# 2015-09-24

import sqlite3
import argparse
import os
import os.path
import re
import sys
import multiprocessing

from common import *

# Define filenames (may be referenced by more than one function)

result_file = 'output.sam'
input_file = 'merged.fasta'

###
# Print the sequences to check; they're the centroids in the clusters saved in the clusters table

# Should it check for a "merged" folder and use those sequence instead to save time?

def print_sequences(db, args):
    fetch_clusters = 'SELECT merged_id, sequence FROM merged WHERE filtered = 0'
    record_metadata(db, 'query', fetch_clusters)
    ff = open(os.path.join(args.workspace, input_file), 'w')
    for id, sequence in db.execute(fetch_clusters):
        print('>{}'.format(id), file=ff)
        print(sequence, file=ff)    
    ff.close()

###
# Run the app

def run_bowtie(args):
    cmnd = 'bowtie2 -p {} '.format(multiprocessing.cpu_count())
    cmnd += ' --no-unal ' # Suppress unaligned reads from SAM file
    cmnd += ' -f ' # Fasta as input instead of fatsq
    cmnd += ' --no-hd ' # Suppress header
    cmnd += ' -S ' + os.path.join(args.workspace, result_file)
    cmnd += ' -x ' + args.reference
    cmnd += ' -U ' + os.path.join(args.workspace, input_file)
    print(cmnd)
    record_metadata(db, 'exec', cmnd, commit=True)
    res = os.system(cmnd)
    
###
# Parse the output file, update merged table to indicate the sequence matches host
# Use "2" for filtered column

update_record = 'UPDATE merged SET merged_id = ?, filtered = 2'

def import_results(db, args):
    #mmap = make_mmap(db)
    for line in open(os.path.join(args.workspace, result_file)):
        res = line.split('\t')
        defspec = res[0]
        #host = res[-1].strip()
        #db.execute(update_record, (mmap[defspec]))
        #print (merged_from_defline(defspec))
        #print (defspec)
        db.execute(update_record, (defspec,))

# Is this nessecary or can we just have merged_id in the FASTA and skip this step?
# Found this step takes too long. Replacing with individual queries
def make_mmap(db):
    mmap = { }
    for mid, name in db.execute('SELECT merged_id, defline FROM merged'):
        mmap[name] = mid
    return mmap

def merged_from_defline(defline):
    if db.execute('SELECT merged_id, defline FROM merged WHERE defline = ?', defline):
        return db.fetchone()[0]

###
# Top level function: initialize the workspace directory, run the app

def filter_host(db, args):
    init_workspace(args)
    print_sequences(db, args)
    run_bowtie(args)
    import_results(db, args)

###
# Parse the command line arguments, call the top level function...
    
if __name__ == "__main__":
    
    args = init_api(
        desc = "Run bowtie2 to filter host sequences using a reference sequence.",
        specs = [
            ('workspace',    { 'metavar': 'dir', 'help' : 'working directory', 'default' : 'host' } ),
            ('reference',    { 'metavar': 'fn', 'help' : 'FASTA file containing reference sequences', 'default' : path_to_resource('zebrafish') } ),
        ]
    )
        
    db = sqlite3.connect(args.dbname)
    record_metadata(db, 'start', ' '.join(sys.argv[1:]))

    #try:
    #    chimera_spec = [('cluster_id', 'foreign', 'clusters'), ('chimeric', 'CHAR(1)')]
    #    init_table(db, 'chimeras', 'chimera_id', chimera_spec, args.force)
    #except Exception as err:
    #    print('Error while initializing output tables:', err)
    #    argparse.ArgumentParser.exit(1, 'Script aborted')

    filter_host(db, args)
    record_metadata(db, 'end', '')

    db.commit()
