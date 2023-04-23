import json, io, sys, os

descriptionRoot = "relax"

weeks = [2,2,2,4,4,4,4,4,4,4,4,4,4,6,6,8,8,12,12,26,26,52,52,52]
nurses = [8,14,20,10,16,18,20,30,36,40,50,60,120,32,45,20,32,22,40,50,100,50,100,150]

for time in [600, 1800, 3600, 43200]:
	description = f"{descriptionRoot}_{time}"

	for timeApproach in [0, 1]:
		for iPartition in ["ALL", "UNITARY", "COUPLE", "QUARTER", "HALF"]:
			for dPartition in ["ALL", "UNITARY", "COUPLE", "QUARTER", "HALF"]:
				if not (iPartition == "ALL" and dPartition == "ALL"):
					for i in range(1,25):
						mayRun = True

						if nurses[i-1] == 8:
							if iPartition == "COUPLE":
								mayRun = False

						if weeks[i-1] == 2:
							if not (dPartition in ["ALL", "HALF"]):
								mayRun = False

						if weeks[i-1] == 4:
							if not (dPartition in ["ALL", "HALF", "QUARTER"]):
								mayRun = False

						if weeks[i-1] == 8:
							if dPartition == "COUPLE":
								mayRun = False

						if(mayRun):
							instance = str(i)
							fileName = f"{instance}_{description}_{iPartition}_{dPartition}_{timeApproach}.job"
							content = f"#PBS -N {instance}_{description}_{iPartition}_{dPartition}_{timeApproach}\n#PBS -l select=1:ncpus=4:nodetype=n40\n#PBS -l walltime=240:00:00\n\nmodule load python/3.6.8-gurobi\nmodule load gurobi/9.0.1\npython relax.py "
							content += f"{instance} {time} {description} {iPartition} {dPartition} {timeApproach}"
							try:
								arquivo = io.open(fileName, "w+", encoding = "utf8")
								arquivo.write(content)
							except:
								print("Erro",i)