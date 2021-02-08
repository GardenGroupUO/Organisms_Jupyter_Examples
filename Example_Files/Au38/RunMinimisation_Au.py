'''
RunMinimisation.py, GRW, 1/3/17

This python program is designed to input the POSCAR file and use it
with Atomic Simulation Environment (ASE) to minimise the given structure
using an empirical potential.

The program will take the output translate it into a OUTCAR file which
the bpga will use.

Required inputs: POSCAR
Required to outputs: OUTCAR (However only the final positions and
"energy without entropy" values are required in this file)
Other outputs: Trajectory file.

'''
from ase import Atom, Atoms
from ase.io import read as ase_read
from ase.io import write as ase_write
#from ase.calculators.emt import EMT
#from asap3 import EMT
from asap3.Internal.BuiltinPotentials import Gupta
from ase.optimize import FIRE
import sys

from ase.visualize import view

####################################################################################################################
# Read the POSCAR file and record the elements, the
# number of each element in the cluster and their positions
cluster = ase_read("BeforeOpt",format='vasp')
cluster.pbc = False
#cluster = ase_read("Cu_Trun_Octa.traj")
#view(cluster)
#import pdb; pdb.set_trace()
#import pdb; pdb.set_trace()
####################################################################################################################
#Construct atoms using the ASE class "Atoms".
####################################################################################################################
# Perform the local optimisation method on the cluster.
#cluster.set_calculator(EMT(EMTRasmussenParameters()))
#cluster.set_calculator(EMT())
# Parameter sequence: [p, q, a, xi, r0]
Au_parameters = {'Au': [10.229, 4.0360, 0.2061, 1.7900, 2.884]}
#Cu_parameters = {'Cu': [10.960, 2.2780, 0.0855, 1.2240, 2.556]}
#AuPd_Gupta_Parameters = {'Pd': [10.867, 3.742, 0.1746, 1.718, 2.7485], 'Au': [10.229, 4.036, 0.2061, 1.79, 2.884], ('Au','Pd'): [10.54, 3.89, 0.19, 1.75, 2.816]}
#Gup_parameters = {
#	'Au': [10.229, 4.0360, 0.2061, 1.7900, 2.884],
#	'Cu': [10.960, 2.2780, 0.0855, 1.2240, 2.556],
#	}
cluster.set_calculator(Gupta(Au_parameters, cutoff=1000, debug=True))
#dyn = BFGS(cluster, trajectory='IndividClusterTraj.traj')
#view(cluster)
#import pdb; pdb.set_trace()
dyn = FIRE(cluster)
try:
	import time
	startTime = time.time()
	dyn.run(fmax=0.01,steps=5000)
	endTime = time.time()
	if not dyn.converged():
		import os
		name = os.path.basename(os.getcwd())
		errorMessage = 'The optimisation of cluster ' + name + ' did not optimise completely.'
		print >> sys.stderr, errorMessage
		print errorMessage
except:
	print('Local Optimiser Failed for some reason.')

ase_write('AfterOpt.traj',cluster)
####################################################################################################################
# Write information about the algorithm
Info = open("INFO.txt",'w')
Info.write("No of Force Calls: " + str(dyn.get_number_of_steps()) + '\n')
Info.write("Time (s): " + str(endTime - startTime) + '\n')
#Info.write("Cluster converged?: " + str(dyn.converged()) + '\n')
Info.close()

####################################################################################################################