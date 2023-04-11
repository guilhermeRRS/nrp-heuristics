def print_GurobiOptimizedOutput(obj):
    objVal = -1
    if obj.valid():
        objVal = obj.m.objVal
    output =  f"===== GUROBI_OPTIMIZE_OUTPUT =====\nInfos:\n"
    output += f"Status:      {obj.status}\n"
    output += f"SolCount:    {obj.solCount}\n"
    output += f"Valid:       {obj.valid()}\n"
    output += f"Obj:         {objVal}\n"
    output += "==============="
    return output

def print_NurseModel(obj):
    output =  f"===== MEMBER_OF_MODEL =====\nInfos:\n"
    output += f"Is there data:      {obj.data != None}\n"
    output += f"Success data:       {obj.s_data}\n"
    output += f"Is there model?     {obj.model != None}\n"
    output += f"Success model?      {obj.s_model}\n"
    output += f"Is there solution?  {obj.solution != None}\n"
    output += f"Success solution?   {obj.s_solution}\n"
    output += "==============="
    return output

def print_Solution(obj):
    output = f"===== MEMBER_OF_SOLUTION =====\nInfos:\n"
    output += f"I:      {len(obj.solution)}\n"
    output += f"D:      {len(obj.solution[0])}\n"
    output += f"T:      {len(obj.solution[0][0])}\n"
    output += f"Hash:   {hash(str(obj.solution))}\n"
    output += "==============="
    return output
