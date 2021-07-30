def addConstraints(VT, VP, C, set_variable):  # them constraints
    for i in range(0, len(set_variable)-1):  # thiet lap AllDIff
        for j in range(i+1, len(set_variable)):
            C.append(f"{set_variable[i]} != {set_variable[j]}")
    C_index = 1
    lenLeft = [len(i) for i in VT]  # do dai cac phan tu ve trai
    lenRight = [len(i) for i in VP]  # do dai cac phan tu ve phai
    while len(lenLeft) != 0:  # lap den khi nao ve trai bang 0
        minValue = min(min(lenLeft), min(lenRight))  # tim phan tu nho nhat 2 ve
        for i in range(minValue):
            temp = ""
            for j in range(len(lenLeft)):  # duyet cac phan tu ben ve trai truoc
                temp += f"{VT[j][lenLeft[j]-1-i]}"
                if j != len(lenLeft) - 1:
                    temp += " + "
            for j in range(len(lenRight)):  # sau do duyet cac phan tu ben ve phai
                if j != len(lenRight) - 1:
                    temp += f" - {VP[j][lenRight[j]-1-i]}"
                else:  # neu la phan tu cuoi cung cua vong lap
                    maxLen = max(lenRight)
                    if maxLen == minValue and i == minValue-1:
                        if C_index == 1:
                            temp += f" == {VP[j][lenRight[j]-1-i]}"
                        else:
                            temp += f" + C{C_index-1} == {VP[j][lenRight[j]-1-i]}"
                    else:
                        if C_index == 1:
                            temp += f" - {VP[j][lenRight[j]-1-i]} == C{C_index} * 10"
                        else:
                            temp += f" - {VP[j][lenRight[j]-1-i]} + C{C_index-1} == C{C_index} * 10"
            C.append(temp)
            C_index += 1
        lenLeft = [i - minValue for i in lenLeft]
        lenRight = [i - minValue for i in lenRight]
        index = 0
        while index < len(lenLeft):
            if lenLeft[index] == 0:
                del lenLeft[index]
                del VT[index]
                continue
            index += 1
        index = 0
        while index < len(lenRight):
            if lenRight[index] == 0:
                del lenRight[index]
                del VP[index]
                continue
            index += 1
    while len(lenRight) != 0:
        minValue = min(lenRight)
        for i in range(minValue):
            temp = ""
            for j in range(len(lenRight)):
                if j != len(lenRight) - 1:
                    if len(temp) != 0:
                        temp += f" - {VP[j][lenRight[j]-1-i]}"
                    else:
                        temp += f"-{VP[j][lenRight[j]-1-i]}"
                else:
                    maxLen = max(lenRight)
                    if maxLen == minValue and i == minValue-1:
                        if len(temp) != 0:
                            temp += f" + C{C_index-1} == {VP[j][lenRight[j]-1-i]}"
                        else:
                            temp += f"C{C_index-1} == {VP[j][lenRight[j]-1-i]}"
                    else:
                        if len(temp) != 0:
                            temp += f" - {VP[j][lenRight[j]-1-i]} + C{C_index-1} == C{C_index} * 10"
                        else:
                            temp += f"-{VP[j][lenRight[j]-1-i]} + C{C_index-1} == C{C_index} * 10"
            C.append(temp)
            C_index += 1
        lenRight = [i-minValue for i in lenRight]
        index = 0
        while index < len(lenRight):
            if lenRight[index] == 0:
                del lenRight[index]
                del VP[index]
                continue
            index += 1


def handleInput(lhsString):
    words = []
    wordsAndOperators = []
    tmpWord = ""
    for i in range(len(lhsString)):
        if (
                lhsString[i] != "+"
                and lhsString[i] != "-"
                and lhsString[i] != "("
                and lhsString[i] != ")"
                and lhsString[i] != "="
        ):
            tmpWord += lhsString[i]
        else:
            if tmpWord != "":
                words.append(tmpWord)
                wordsAndOperators.append(tmpWord)
            wordsAndOperators.append(lhsString[i])
            tmpWord = ""

    words.append(tmpWord)
    wordsAndOperators.append(tmpWord)

    for i in range(len(wordsAndOperators)):
        if wordsAndOperators[i] == "-" and wordsAndOperators[i + 1] == "(":
            for j in range((i + 1), len(wordsAndOperators)):
                if wordsAndOperators[j] == ")":
                    break
                if wordsAndOperators[j] == "-":
                    wordsAndOperators[j] = "+"
                elif wordsAndOperators[j] == "+":
                    wordsAndOperators[j] = "-"
    length = len(wordsAndOperators)
    for i in range(len(wordsAndOperators)):
        if wordsAndOperators[i] == '(' or wordsAndOperators[i] == ')':
            length = length - 1
    for index in range(length):
        if wordsAndOperators[index] == '(':
            length = length - 1
            wordsAndOperators.pop(index)
    for index in range(length):
        if wordsAndOperators[index] == ')':
            length = length - 1
            wordsAndOperators.pop(index)
    VT = wordsAndOperators[0]
    VP = wordsAndOperators[len(wordsAndOperators) - 1]
    for i in range(len(wordsAndOperators) - 2):
        if wordsAndOperators[i] == "+":
            VT = VT + wordsAndOperators[i] + wordsAndOperators[i + 1]
        elif wordsAndOperators[i] == '-':
            VP = VP + '+' + wordsAndOperators[i + 1]
    result = VT + '=' + VP
    return result


def initCSP():  # mo phong CSP
    f = open("input.txt", "r")  #  doc file input
    temp = f.read()
    f.close()
    res = handleInput(temp)
    lst = res.split("=")  # tien hanh tach input
    VT = lst[0].split("+")  # tach phan tu ve trai
    VP = lst[1].split("+")  # tach phan tu ve phai
    X = {}  # tao dictionary luu variable and domain
    set_variable = []  # tao list chi luu variable
    C = []  # tao list luu cac constraints
    for i in range(len(VT)):  # them vao cac phan tu dau cua ve trai
        if VT[i][0] not in X:
            if len(VT[i]) != 1:
                X[VT[i][0]] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                set_variable.append(VT[i][0])
            else:
                flag = True
                for j in range(i+1, len(VT)):
                    if VT[j][0] == VT[i][0] and len(VT[j]) != 1:
                        X[VT[i][0]] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                        set_variable.append(VT[i][0])
                        flag = False
                        break
                if not flag:
                    continue
                for j in range(0, len(VP)):
                    if VP[j][0] == VT[i][0] and len(VP[j]) != 1:
                        X[VT[i][0]] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                        set_variable.append(VT[i][0])
                        flag = False
                        break
                if flag:
                    X[VT[i][0]] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
                    set_variable.append(VT[i][0])
    for i in range(len(VP)):  # them vao cac phan tu dau cua ve phai
        if VP[i][0] not in X:
            if len(VP[i]) != 1:
                X[VP[i][0]] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                set_variable.append(VP[i][0])
            else:
                flag = True
                for j in range(i+1, len(VP)):
                    if VP[j][0] == VP[i][0] and len(VP[j]) != 1:
                        X[VP[i][0]] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                        set_variable.append(VP[i][0])
                        flag = False
                        break
                if flag:
                    X[VP[i][0]] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
                    set_variable.append(VP[i][0])
    for element in VT:
        for index in range(0, len(element)):
            if element[index] not in X and index != 0:  # neu chua co trong variable va khong dung dau
                X[element[index]] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
                set_variable.append(element[index])
    for element in VP:
        for index in range(0, len(element)):
            if element[index] not in X and index != 0:  # neu chua co trong variable va khong dung dau
                X[element[index]] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
                set_variable.append(element[index])
    maxLeft = 0  # xac dinh do dai cua phan tu lon nhat ben trai
    maxRight = 0  # xac dinh do dai cua phan tu lon nhat ben phai
    for element in VT:
        if len(element) > maxLeft:
            maxLeft = len(element)
    for element in VP:
        if len(element) > maxRight:
            maxRight = len(element)
    if maxLeft > maxRight:
        VT, VP = VP, VT
        maxLeft, maxRight = maxRight, maxLeft
    addConstraints(VT, VP, C, set_variable)
    for i in range(0, maxRight-1):  # cac bien carry
        X[f"C{i+1}"] = []
        set_variable.append(f"C{i+1}")
    return set_variable, X, C


def chooseVariable(assignment, X, C):  # chon bien de gan gia tri (theo R.H.S)
    for constraints in C:  # duyet qua tung constrains
        if "!" in constraints:  # duyet cac constraints khong là allDiff
            continue
        lst = constraints.split()
        for element in lst:  # kiem tra cac gia tri trong constraints
            if element not in assignment and element in X and len(element) == 1:  # neu chua nam trong assignment
                return element


def findCarry(assignment, X, C):  # tim bien trong constraint
    countLoop = 0  # dem so lan thuc hien tim bien
    for constraints in C:  # duyet constraint
        if "!" in constraints:  # duyet cac constraints khong là allDiff
            continue
        lst = constraints.split(" == ")  # tach ra ve trai va ce phai constraint
        count = 0  # dem so luong bien trong assignment nam trong ve trai
        count1 = 0  # dem so luong bien trong assignment nam trong constraint
        count2 = 0  # dem so luong bien trong X nam trong ve trai
        for element in assignment:  # duyet qua cac bien da gan gia tri nam trong ve trai constraint
            if element in lst[0]:
                count += 1
        for element in assignment:  # duyet qua cac bien da gan nam trong constraint
            if element in constraints:
                count1 += 1
        for element in X:  # duyet qua cac bien nam ben ve trai constraint
            if element in lst[0]:
                count2 += 1
        if count == count1 and count == count2:  # neu thoa dieu kien thi tien hanh tim bien
            RHS = lst[1].split()
            value = eval(lst[0], {}, assignment)  # tinh gia tri ve trai
            if len(RHS[0]) != 1:  # neu bien trong ve phai la bien carry thi chia value cho 10
                value /= 10
            if value != int(value):  # neu value khong la so nguyen
                while countLoop != 0:  # thuc hien pop cac bien suy luan duoc va tra ve suy luan sai
                    countLoop -= 1
                    assignment.popitem()
                return -1
            else:
                if len(RHS[0]) == 1 and value in X[RHS[0]]:  # neu bien khong la carry thi phai nam trong mien gia tri
                    assignment[RHS[0]] = int(value)
                elif len(RHS[0]) != 1:  # neu la bien carry
                    assignment[RHS[0]] = int(value)
                else:  # nguoc lai tien hanh pop va tra ve that bai
                    while countLoop != 0:
                        countLoop -= 1
                        assignment.popitem()
                    return -1
            countLoop += 1
    return countLoop  # tra ve so luong bien suy luan duoc thanh cong


def checkConsistent(assignment, X, C):  # kiem tra tinh dung dan
    for constraints in C:  # xet cac constraint
        arr = []
        for element in assignment:  # duyet qua cac bien da gan gia tri
            if element in constraints:  # neu bien do trong constraint
                arr.append(True)
        count = 0
        for element in X:  # duyet qua cac bien trong tat ca cac bien
            if element in constraints:
                count += 1
        if len(arr) == count:  # neu constraint da co day du bien
            if not eval(constraints, {}, assignment):  # vi pham dieu kien
                return False
    return True


def backtrackingSearch(assignment, X, C):  # duyet qua tat ca cac truong hop
    countLoop = 0
    if len(assignment) == len(X):  # truong hop tim ra loi giai
        if checkConsistent(assignment, X, C):  # neu thoa dieu kien
            return True
        return False
    var = chooseVariable(assignment, X, C)  # chon bien de gan gia tri
    for element in X[var]:
        assignment[var] = element  # gan gia tri cho bien
        if checkConsistent(assignment, X, C):  # kiem tra tinh dung dan
            countLoop = findCarry(assignment, X, C)  # tien hanh suy luan bien
            if countLoop == -1:  # neu suy luan that bai thi tiep tuc loop
                continue
            result = backtrackingSearch(assignment, X, C)  # neu dung thi tiep tuc gan bien khac
            if result:  # neu co ket qua thi tra ve ngay
                return True
            while countLoop != 0:  # quay lui neu suy luan that bai va pop cac bien da suy luan duoc
                assignment.popitem()
                countLoop -= 1
    assignment.popitem()  # quay lui pop bien da gan truoc do
    return False


def writeOutput(assignment, flag):  # ghi ket qua vao file output.txt
    f = open("output.txt", "w")
    if flag:
        assignment = dict(sorted(assignment.items()))
        for element in assignment:
            if len(element) == 1:
                f.write(str(assignment[element]))
                f.write("")
    else:
        f.write("NO SOLUTION")
    f.close()
