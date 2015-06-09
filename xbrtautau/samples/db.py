# stdlib imports
import os
import atexit

# # pytables imports
# import tables

# rootpy imports
from rootpy.io import root_open, TemporaryFile

# local imports
from .. import NTUPLE_PATH, DEFAULT_STUDENT
from . import log; log = log[__name__]


FILES = {}
TEMPFILE = TemporaryFile()

PILEUP_FILES = {}


def get_file(ntuple_path=NTUPLE_PATH, file_name = None,  student=DEFAULT_STUDENT, hdf=False, suffix='', force_reopen=False, **kwargs):
   
    if file_name is None : 
        ext = '.h5' if hdf else '.root'
        filename = student + suffix + ext
        if filename in FILES and not force_reopen:
            return FILES[filename]
        file_path = os.path.join(ntuple_path, filename)
    #     file_path = os.path.join(ntuple_path, student + suffix, filename)
        log.info("opening {0} ...".format(file_path))
        if hdf:
            #         student_file = tables.open_file(file_path)#, driver="H5FD_CORE")
            log.error('Not Implemented yet')
            raise RuntimeError('Not Implemented yet')
        else:
            student_file = root_open(file_path, 'READ')
            FILES[filename] = student_file

    else:
        file_path = os.path.join(ntuple_path, file_name)
        log.info("opening {0} ...".format(file_path))
        student_file = root_open(file_path, 'READ')
        FILES[filename] = student_file
    
    return student_file

@atexit.register
def cleanup():
    if TEMPFILE:
        TEMPFILE.close()
    for filehandle in FILES.values():
        if filehandle:
            filehandle.close()
    for filehandle in PILEUP_FILES.values():
        if filehandle:
            filehandle.close()
