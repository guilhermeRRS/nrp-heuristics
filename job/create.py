import json, io, sys, os

description = "solver"
time = 900

description = f"{description}_{time}"

for i in range(1,25):
	instance = str(i)
	fileName = f"{instance}_{description}.job"
	content = f"#PBS -N {instance}_{description}\n#PBS -l select=1:ncpus=4:nodetype=n40\n#PBS -l walltime=240:00:00\n\nmodule load python/3.6.8-gurobi\nmodule load gurobi/9.0.1\npython main.py "
	content += f"{instance} {time} {description}"
	try:
		arquivo = io.open(fileName, "w+", encoding = "utf8")
		arquivo.write(content)
	except:
		print("Erro",i)