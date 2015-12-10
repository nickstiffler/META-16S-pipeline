#! /usr/bin/env python3

# Run comparison between negative controls and all other sequences to filter 
# sequences that may represent background contamination.

# John Conery / Nicholas Stiffler
# University of Oregon
# 2015-12-09

import sqlite3
import multiprocessing

from common import *

controls_file = "controls.fasta"
sequences_file = "sequences.fasta"
output_file = "results.uc"

def map_sample_ids(db, args):
    fetch_sids = "SELECT sample_id FROM samples WHERE name = ?"
    record_metadata(db, 'query', fetch_sids)
    sids = ()
    
    if args.controls is not None:
        for line in open(args.controls):
            sample = line.rstrip()
            sample_id = db.execute(fetch_sids, (sample,)).fetchone()
            if sample_id:
                sids.append(sample_id[0])
    
    return sids               


def flag_controls(db, args):
    sids = map_sample_ids(db, args)
    update_controls = 'UPDATE merged SET filtered = 8 WHERE sample_id = ?'
    for sid in sids:
        db.execute(update_controls, (sid,))
                    
def print_sequences(db, args):
    sids = map_sample_ids(db, args)
    fetch_merged = 'SELECT merged_id, sample_id, sequence FROM merged WHERE filtered = 0'
    record_metadata(db, 'query', fetch_merged)
    cf = open(os.path.join(args.workspace, controls_file), 'w')
    ff = open(os.path.join(args.workspace, sequences_file), 'w')
    for id, sample_id, sequence in db.execute(fetch_merged):
        if sample_id in sids:
            print('>{}'.format(id), file=cf)
            print(sequence, file=cf)
        else:
            print('>{}'.format(id), file=ff)
            print(sequence, file=ff) 
    ff.close()

def run_comparison(args): 
       
    cmnd = 'usearch -search_exact ' + os.path.join(args.workspace, sequences_file)
    cmnd += ' -strand plus '
    cmnd += ' -db ' + os.path.join(args.workspace, controls_file)
    cmnd += ' -uc ' + os.path.join(args.workspace, output_file)
    #cmnd += ' -threads {}'.format(multiprocessing.cpu_count())
    print(cmnd)
    record_metadata(db, 'exec', cmnd, commit=True)
    res = os.system(cmnd)
    
def import_results(db, args):
    update_record = 'UPDATE merged SET filtered = 8 WHERE merged_id = ?'
    for line in open(os.path.join(args.workspace, output_file)):
        res = line.rstrip().split('\t')
        
        if res[0] == 'H':
            db.execute(update_record, (res[8],))
    
def filter_controls(db, args):
    init_workspace(args)
    flag_controls(db, args)
    print_sequences(db, args)
    run_comparison(args)
    import_results(db, args)

###
# Parse the command line arguments, call the top level function...
    
if __name__ == "__main__":
    
    args = init_api(
        desc = "Run comparison between negative controls and all other sequences to flag sequences that may represent background contamination.",
        specs = [
            ('workspace',    { 'metavar': 'dir', 'help' : 'working directory', 'default' : 'contaminate' } ),
            ('controls',    { 'required': True, 'metavar': 'fn', 'help' : '(required) File containing a list of the sample names that are negative controls' } ),
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

    filter_controls(db, args)
    record_metadata(db, 'end', '')

    db.commit()
