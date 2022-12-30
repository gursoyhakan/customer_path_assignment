# this program simulates the pattern of incoming and exiting customers for any predefined number
# of times. The result of each run is saved and will be used for evaluation of our studies
import random
import time
import gurobipy as gp
from linear_programming import FileOperations, Optimization

number_of_simulations = 10
simulation_customer_number = 200
static_ratio = 0.3
dynamic_ratio = 1 - static_ratio
simulation_days = 100
customer_exit_probability = dict()
customer_exit_probability[0] = 0
customer_exit_probability[1] = 0.02
for i in range(2, 61):
    customer_exit_probability[i] = customer_exit_probability[i-1] + 0.005 / i
for i in range(61, 101):
    customer_exit_probability[i] = 1
print(customer_exit_probability)

# Here we get the data by using FileOperations class
reading = FileOperations()
num_day, num_actions, num_people, num_paths, paths, debts, CLV, action_costs, action_constraints, reading_time = \
    reading.read_from_file("deneme2_input.txt")
simulations = []


# Simulation part
for simulation in range(number_of_simulations):
    # Random customer selection for static and dynamic optimization
    customer_selected = []
    dynamic_customer_list = []
    static_customer_list = []
    for i in range(num_people):
        if random.random() <= float(simulation_customer_number/num_people):
            customer_selected.append(i)
            if random.random() <= static_ratio:
                static_customer_list.append(i)
            else:
                dynamic_customer_list.append(i)
    print("\n", len(customer_selected), len(static_customer_list), len(dynamic_customer_list))
    # Static optimization
    daily_remaining = {}
    for day in range(1, num_day+1):
        for action in range(1, num_actions+1):
            daily_remaining[day, action] = action_constraints[day, action] * len(customer_selected) // num_people
    sim = Optimization()
    sim.paths = [paths[i] for i in static_customer_list]
    sim.num_people = len(static_customer_list)
    sim.num_paths = [num_paths[i] for i in static_customer_list]
    sim.num_day = num_day
    sim.num_actions = num_actions
    sim.action_constraints = {}
    for i in range(1, num_day+1):
        for j in range(1, num_actions+1):
            sim.action_constraints[i, j] = action_constraints[i, j] * len(static_customer_list) // num_people
    sim.action_costs = action_costs
    sim.CLV = [CLV[i] for i in static_customer_list]
    sim.debts = [debts[i] for i in static_customer_list]
    sim.reading_time = time.time()
    sim.log_to_console = 0
    status, objVal, cust_path_bin, optimization_time = sim.optimize()
    if status == gp.GRB.OPTIMAL:
        print(f"Static Optimization is optimal with objective Value: {objVal:.2f} in {optimization_time:.2f} seconds")
    else:
        print(f"Static Optimization is infeasible in {optimization_time} seconds, passing to the next simulation")
        continue
    daily_uses = sim.action_number_render(cust_path_bin)
    for day, action in daily_uses.keys():
        daily_remaining[day, action] -= daily_uses[day, action]
    print(f"Dynamic simulation starts for simulation number : {simulation + 1}")
    daily_average_dynamic_customers = len(dynamic_customer_list)//simulation_days
    # dynamic simulation
    daily_customers = dict()
    exiting_customers = dict()
    for sim_day in range(simulation_days):
        daily_customers[sim_day] = []
        exiting_customers[sim_day] = []
        for customer in dynamic_customer_list:
            if random.random() <= daily_average_dynamic_customers / len(dynamic_customer_list):
                daily_customers[sim_day].append(customer)
                dynamic_customer_list.remove(customer)
        for customer in static_customer_list:
            if random.random() <= customer_exit_probability[sim_day + 1]:
                exiting_customers[sim_day].append(customer)
                static_customer_list.remove(customer)
        for sim_day_2 in range(sim_day):
            for customer in daily_customers[sim_day_2]:
                if random.random() <= customer_exit_probability[sim_day + 1 - sim_day_2]:
                    exiting_customers[sim_day].append(customer)
                    daily_customers[sim_day_2].remove(customer)
        print(f" Simülasyon sayısı {simulation + 1}, simülasyon günü {sim_day + 1},sisteme giren müşteriler {len(daily_customers[sim_day])}, "
              f" sistemden çıkan müşteri sayısı{len(exiting_customers[sim_day])}, statik analizden kalan müşteri sayısı {len(static_customer_list)}")

