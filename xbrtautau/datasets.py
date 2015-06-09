import os
import logging
import copy
import yaml
import re

from . import UNMERGED_NTUPLE_PATH
from . import log; log = log[__name__]

#log = logging.getLogger(os.path.basename(__file__))

PATTERN = re.compile('flat_(?P<mode>gg|VBF)(?P<mass>\d+)_seed(?P<seed>\d+)')

def create_samples():
    log.info('Building samples using regular expressions ...')
    SAMPLES_RAW = {}
    KEYS = []
    for rfile in os.listdir(UNMERGED_NTUPLE_PATH):
        abs_rfile = os.path.join(UNMERGED_NTUPLE_PATH, rfile)
        match = re.match(PATTERN, rfile)
        if match:
            mode = match.group('mode')
            mass = int(match.group('mass'))
            if mode in SAMPLES_RAW.keys():
                if mass in SAMPLES_RAW[mode].keys():
                    SAMPLES_RAW[mode][mass].append(abs_rfile)
                else:
                    SAMPLES_RAW[mode][mass] = [abs_rfile]
            else:
                SAMPLES_RAW[mode] = {}

    # Build final dictionnary
    SAMPLES = {}
    for mode, sample_masses in SAMPLES_RAW.items():
        SAMPLES[mode] = {}
        for mass, samples in sample_masses.items():
            SAMPLES[mode][mass] = {
                'all': samples, 
                'train': samples[:len(samples) / 2],
                'test': samples[len(samples) / 2:]}
    return SAMPLES


def create_database(db_name='datasets.yml'):
    SAMPLES = create_samples()
    with open(os.path.join(os.path.dirname(__file__), db_name), 'w') as fdb:
        yaml.dump(SAMPLES, fdb)

def read_database(db_name='datasets.yml'):
    if os.path.exists(os.path.join(
            os.path.dirname(__file__), db_name)):
        log.info('Load %s ...' % db_name)
        with open(os.path.join(os.path.dirname(__file__), db_name)) as fdb:
            return yaml.load(fdb)
    else:
        raise Exception('The database %s does not exists' % db_name)
