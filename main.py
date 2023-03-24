from model import Model

PATH_DATA = "../instancias/"
PATH_MODEL = "../modelos/"

instance = "1"

nurse = Model()
nurse.setPathData(f"{PATH_DATA}Instance{instance}.txt")
nurse.setPathModel(f"{PATH_MODEL}modelo{instance}.lp")

nurse.getData()

print(nurse.data)