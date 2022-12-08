import gurobipy as gp
import time
''' reading part of the program'''
t1 = time.time()
input_file = "deneme2_input.txt"
f = open(input_file, "r")
strr = f.readline()
line = strr.split(",")
num_people = eval(line[0])
num_day = eval(line[1])
num_actions = eval(line[2])
strr = f.readline()
line = strr.split(",")
action_constraints = []
for i in range(num_actions):
    action_constraints.append(eval(line[i]))
strr = f.readline()
line = strr.split(",")
action_costs = []
for i in range(num_actions):
    action_costs.append(eval(line[i]))
strr = f.readline()
line = strr.split(",")
num_paths = []
for i in range(num_people):
    num_paths.append(eval(line[i]))
strr = f.readline()
line = strr.split(",")
CLV = []
for i in range(num_people):
    CLV.append(eval(line[i]))
strr = f.readline()
line = strr.split(",")
debts = []
for i in range(num_people):
    debts.append(eval(line[i]))
paths = []
for i in range(num_people):
    person_paths = []
    for j in range(num_paths[i]):
        path = []
        strr = f.readline()
        line = strr[1:-2].split(",")
        for k in line:
            path.append(eval(k))
        person_paths.append(path)
    paths.append(person_paths)
f.close()
t2 = time.time()
print(f'Reading OK in {t2-t1} seconds')
''' optimization part starts'''
m = gp.Model()
'''variable definitions'''
cust_path_bin = {}
non_payment_cost = m.addVar(vtype='C')
churn_cost = m.addVar(vtype='C')
action_cost = m.addVar(vtype='C')
for i in range(num_people):
    for j in range(num_paths[i]):
        cust_path_bin[i, j] = m.addVar(vtype='B')
'''constraints'''
m.addConstr(non_payment_cost ==
    gp.quicksum(debts[i] * gp.quicksum(cust_path_bin[i, j] * paths[i][j][-2] for j in range(num_paths[i]))
                for i in range(num_people))
)
m.addConstr(churn_cost ==
    gp.quicksum(CLV[i] * gp.quicksum(cust_path_bin[i, j] * paths[i][j][-1] for j in range(num_paths[i]))
                for i in range(num_people))
)
m.addConstr(action_cost ==
    gp.quicksum(action_costs[i] *
                gp.quicksum(
                    gp.quicksum(cust_path_bin[j, k] *
                                gp.quicksum(1 for t in range(num_day) if paths[j][k][t] == i+1)
                                for k in range(num_paths[j]))
                    for j in range(num_people))
                for i in range(num_actions))
)
for i in range(num_people):
    m.addConstr(gp.quicksum(cust_path_bin[i, j] for j in range(num_paths[i])) == 1)

for i in range(num_day):
    for j in range(num_actions):
        m.addConstr(
            gp.quicksum(gp.quicksum(cust_path_bin[k, t] *
                                    1 for t in range(num_paths[k]) if paths[k][t][i] == j+1)
                        for k in range(num_people))
            <= action_constraints[j])
'''objective function'''
m.setObjective(non_payment_cost+churn_cost+action_cost, gp.GRB.MINIMIZE)
'''Optimizations'''
m.optimize()
'''Printing Results'''
f = open("output.txt", "w")
if m.status == gp.GRB.OPTIMAL:
    for i in range(num_people):
        for j in range(num_paths[i]):
            if cust_path_bin[i, j].x == 1:
                f.writelines(f" For customer {i+1} we have to choose path {j} \n")
                strr = "Path start ->"
                for k in paths[i][j]:
                    strr += str(k) + "->"
                strr += "\n"
                f.writelines(strr)
else:
    f.writelines('Infeasible')
t3 = time.time()
print(f"Finished optimization in {t3-t2}")
f.close()
