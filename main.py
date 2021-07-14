import function


set_variable, X, C = function.initCSP()
assignment = {}
PQ = []
flag = function.backtrackingSearch(PQ, assignment, X, C)
print(assignment)
function.writeOutput(assignment, flag)
