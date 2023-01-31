import nrv

out_file = './unitary_tests/results/outputs/105_SimParameters.json'

param = nrv.SimParameters(D=3, mesh_file="./unitary_tests/sources/3cylinder")
param.add_domain(mesh_domain=0,mat_file="M1.mat")
param.add_domain(mesh_domain=100,mat_file="M1.mat")
param.add_domain(mesh_domain=200,mat_file="M1.mat", ID=5)

param.add_boundary(mesh_domain=11, btype='Dirichlet', value=0, variable=None, ID=1)
param.add_boundary(mesh_domain=22, btype='Neuman', value=None, variable='jstim', ID=2)

p1 = param.save_SimParameters(save=True, fname=out_file)
#print(p1)

param.add_domain(mesh_domain=200,mat_file="M2.mat", ID=5)
param.add_boundary(mesh_domain=22, btype='Neuman', value=None, variable='jstim', ID=2)
p2 = param.save_SimParameters(save=False)
#print(p2)

param2 = nrv.SimParameters(data=out_file)
p3 = param2.save_SimParameters(save=False)
#print(p3)

