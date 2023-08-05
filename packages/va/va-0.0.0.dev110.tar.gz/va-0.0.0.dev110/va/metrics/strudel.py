import subprocess
import sys
import os
from distutils.spawn import find_executable


def create_folder(output_path):
    """
        create strudel output folder inside va directory

    :return: model related path of strudel folder
    """

    fullname = '{}'.format(output_path)

    if not os.path.isdir(fullname):
        os.mkdir(fullname, mode=0o777)
    else:
        print('{} is exist'.format(fullname))


def run_strudel(full_modelpath, full_mappath, motif_libpath, output_path, platform=None):
    """
        full_modelpath: full path of the model with name
        full_mappath: full path of the map with name
        motif_libpath: full path of the motif lib for its resolution
        output_path: output directory
    :return:
    """

    create_folder(output_path)
    num_processors = int(os.cpu_count() / 2)
    bsub_bin = find_executable('bsub')
    strudel_cmd = 'strudel_mapMotifValidation.py -p {} -m {} -l {} -o {} -np {}'.format(full_modelpath,
                                                                                            full_mappath, motif_libpath,
                                                                                            output_path, num_processors)
    if platform == 'emdb' and bsub_bin:
        strudel_cmd = 'bsub -e {}/strudel_stderr.txt -o {}/strudel_stdout.txt -n 16 -M 32G ' \
                      'strudel_mapMotifValidation.py -p {} -m {} -l {} -o {} -np 16 -log ' \
                      '{}/strudel.log'.format(output_path,
                                              output_path,
                                              full_modelpath,
                                              full_mappath,
                                              motif_libpath,
                                              output_path, output_path)
    errlist = []
    print(strudel_cmd)
    process = subprocess.Popen(strudel_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True,
                               cwd=output_path)

    output = process.communicate('n\n')[0]
    errstrudelscore = 'error'
    if sys.version_info[0] >= 3:
        for item in output.decode('utf-8').split('\n'):
            print(item)
            if errstrudelscore in item.lower():
                errline = item.strip()
                errlist.append(errline)
                assert errstrudelscore not in output.decode('utf-8'), errline

    else:
        for item in output.split('\n'):
            print(item)
            if errstrudelscore in item.lower():
                errline = item.strip()
                errlist.append(errline)
                assert errstrudelscore not in output.decode('utf-8'), errline
    # If needed here will do the post processing of strudel score
    # posts_trudlescore()
    # if output:
    #     strerr = ' '.join([t for t in output.decode('utf-8').split('\n') if t])

    return errlist


def strudel_tojson(self):
    """
        Process strudel score related files

    :return:
    """

    pass
