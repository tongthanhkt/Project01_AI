import function


set_variable, X, C = function.initCSP()
print(X)
print(C)
assignment = {}
flag = function.backtrackingSearch(assignment, X, C)
print(dict(sorted(assignment.items())))
function.writeOutput(assignment, flag)
