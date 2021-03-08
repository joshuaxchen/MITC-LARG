import sys
import os
import os.path
import time
import subprocess
import argparse
import atexit


parser = argparse.ArgumentParser()
parser.add_argument('--base_dir', help='base directory of experiment')
parser.add_arguemnt('--gens', type=int, help='Number of generations')
parser.add_argument('--gensize', type=int, help='Size of generztions')
parser.add_argument('--param_file', help='path to parameter file being used')
parser.add_argument('--benchmark_name', help='benchmark to use')
parser.add_argument('--controller_name', help='controller to use')
args = parser.parser_args();

#base_dir = sys.argv[1]
base_dir = args.base_dir



#gens = int(sys.argv[2])
gens = args.gens

#gensize = int(sys.argv[3])
gensize = args.gensize


start_file = base_dir + "/paramswritten_{}.txt"
end_file = base_dir + "/valuationdone_{}.txt"
params_file = base_dir + "/params_{}_i_{}.txt"
results_file = base_dir + "/value_{}_i_{}.txt"

cma_p = None



def cleanup():
    if cam_p is not None:
        cma_p.kill()

atexit.register(cleanup)

def start_cma():
    cma_p = subprocess.Popen(['java', '-cp', 'condor/3dsim/cma/java' 'cma.CMAMain', args.base_dir, str(args.gens), str(args.gensize), args.param_file])


def read_params(fname):
    with open(fname, 'r') as f:
        lines = f.readlines()
    params = {}
    for l in lines:
        s = l.split('\t')
        params[s[0]] = str(float(s[-1][:-1]))
    print(params)
    return params




def check_done():
    out = subprocess.Popen(['condor_q'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = out.communicate()
    lines = str(stdout).split('\\n')
    #print(lines)
    last = lines[-4]
    terms = last.split()
    #print(terms)
    num_working = int(terms[3])
    return num_working == 0



start_cma()


for i in range(1, gens+1):
    while not os.path.isfile(start_file.format(i)):
        print("Waiting on file")
        time.sleep(5)
    for j in range(gensize):
        params = read_params(params_file.format(i, j))
        print(params)
        os.system(f'condor_submit create.sub --append arguments=\"{results_file.format(i, j)} \'{json.dumps(params)}\'\"') 
    while not check_done():
        print("Waiting on condor")
        time.sleep(5)

    with open(end_file.format(i), 'w') as f:
        f.write("done")




