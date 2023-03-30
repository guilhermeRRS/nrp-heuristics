import json, io, sys, os

descriptionRoot = "relax"

for time in [600, 900, 3600]:
	description = f"{descriptionRoot}_{time}"

	for fast in [0, 1]:
		for iPartition in ["ALL", "UNITARY", "COUPLE", "QUARTER", "HALF"]:
			for dPartition in ["ALL", "UNITARY", "COUPLE", "QUARTER", "HALF"]:

				for i in range(1,25):
					instance = str(i)
					fileName = f"{instance}_{description}_{iPartition}_{dPartition}_{fast}.job"
					content = f"#PBS -N {instance}_{description}_{iPartition}_{dPartition}_{fast}\n#PBS -l select=1:ncpus=4:nodetype=n40\n#PBS -l walltime=240:00:00\n\nmodule load python/3.6.8-gurobi\nmodule load gurobi/9.0.1\npython relax.py "
					content += f"{instance} {time} {description} {iPartition} {dPartition} {fast}"
					try:
						arquivo = io.open(fileName, "w+", encoding = "utf8")
						arquivo.write(content)
					except:
						print("Erro",i)