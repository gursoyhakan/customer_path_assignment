# this program simulates the pattern of incoming and exiting customers for any predefined number
# of times. The result of each run is saved and will be used for evaluation of our studies
import random
import time
import gurobipy as gp
from linear_programming import FileOperations, Optimization
input_file = "deneme2_input.txt"
number_of_simulations = 2
simulation_customer_number = 600
static_ratio = 0.1
dynamic_ratio = 1 - static_ratio
simulation_days = 250
customer_exit_probability = dict()
customer_exit_probability[0] = 0
customer_exit_probability[1] = 0.01
for i in range(2, 61):
    customer_exit_probability[i] = customer_exit_probability[i-1] + 0.005 / i
for i in range(61, simulation_days):
    customer_exit_probability[i] = 1

# Here we get the data by using FileOperations class
reading = FileOperations()
num_day, num_actions, num_people, num_paths, paths, debts, CLV, action_costs, action_constraints, reading_time = \
    reading.read_from_file(input_file)
simulations = []

# Simulation part
for simulation in range(number_of_simulations):
    # Random customer selection for static and dynamic optimization
    customer_selected = []
    dynamic_customer_list = []
    static_customer_list = []
    customer_entry_day = {}
    customer_exit_day = {}
    customers_in_system = []
    customers_selected_path = {}
    for i in range(num_people):
        if random.random() <= float(simulation_customer_number/num_people):
            customer_selected.append(i)
            if random.random() <= static_ratio:
                static_customer_list.append(i)
                customer_entry_day[i] = 1
                customers_in_system.append(i)
            else:
                dynamic_customer_list.append(i)
    print(f"# of customers selected for simulation {len(customer_selected)}, "
          f"{len(static_customer_list)}, {len(dynamic_customer_list)}")
    # Static optimization
    daily_remaining = {}
    for day in range(1, simulation_days+61):
        for action in range(1, num_actions+1):
            daily_remaining[day, action] = action_constraints[1, action]
    sim = Optimization()
    sim.paths = [paths[i] for i in static_customer_list]
    sim.num_people = len(static_customer_list)
    sim.num_paths = [num_paths[i] for i in static_customer_list]
    sim.num_day = num_day
    sim.num_actions = num_actions
    sim.action_constraints = {}
    for i in range(1, num_day + 1):
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
    for customer, path_num in cust_path_bin.keys():
        if cust_path_bin[customer, path_num] == 1:
            customers_selected_path[static_customer_list[customer]] = path_num
    for day, action in daily_uses.keys():
        daily_remaining[day, action] -= daily_uses[day, action]
    print(f"Dynamic simulation starts for simulation number : {simulation + 1}")
    # dynamic simulation
    daily_customers = dict()
    exiting_customers = dict()
    for sim_day in range(simulation_days):
        daily_customers[sim_day] = []
        exiting_customers[sim_day] = []
        dynamic_customer_list_len = len(dynamic_customer_list)
        daily_average_dynamic_customers_selection_ratio = float(1/(simulation_days-sim_day))
        for customer in dynamic_customer_list:
            if random.random() <= daily_average_dynamic_customers_selection_ratio:
                daily_customers[sim_day].append(customer)
                customer_entry_day[customer] = sim_day + 1
                dynamic_customer_list.remove(customer)
        for customer in customers_in_system:
            if random.random() <= customer_exit_probability[sim_day - customer_entry_day[customer] + 1]:
                exiting_customers[sim_day].append(customer)
                customer_exit_day[customer] = sim_day + 1
                customers_in_system.remove(customer)
                if customer in static_customer_list:
                    static_customer_list.remove(customer)
                selected_path = paths[customer][customers_selected_path[customer]]
                for i in range(customer_exit_day[customer] - customer_entry_day[customer], num_day):
                    removed_action = selected_path[i]
                    daily_remaining[sim_day + i + 1, removed_action] += 1
        for customer in daily_customers[sim_day]:
            customers_in_system.append(customer)
        print(f" Simülasyon sayısı {simulation + 1}, simülasyon günü {sim_day + 1}, "
              f"sisteme giren müşteriler {len(daily_customers[sim_day])}, "
              f" sistemden çıkan müşteri sayısı {len(exiting_customers[sim_day])}, "
              f"statik analizden kalan müşteri sayısı {len(static_customer_list)}"
              f" Sisteme henüz girmeyen dinamik analiz müşteri sayısı {len(dynamic_customer_list)}")
        daily_sim = Optimization()
        daily_sim.paths = [paths[i] for i in daily_customers[sim_day]]
        daily_sim.num_people = len(daily_customers[sim_day])
        daily_sim.num_paths = [num_paths[i] for i in daily_customers[sim_day]]
        daily_sim.num_day = num_day
        daily_sim.num_actions = num_actions
        daily_sim.action_constraints = {}
        if dynamic_customer_list_len > 0:
            for i in range(1, num_day+1):
                for j in range(1, num_actions+1):
                    daily_sim.action_constraints[i, j] = \
                        daily_remaining[i, j] * len(daily_customers[sim_day]) // dynamic_customer_list_len
        else:
            continue
        daily_sim.action_costs = action_costs
        daily_sim.CLV = [CLV[i] for i in daily_customers[sim_day]]
        daily_sim.debts = [debts[i] for i in daily_customers[sim_day]]
        daily_sim.reading_time = time.time()
        daily_sim.log_to_console = 0
        status, objVal, cust_path_bin, optimization_time = daily_sim.optimize()
        daily_sim_used_actions = daily_sim.action_number_render(cust_path_bin)
        for day, action in daily_sim_used_actions.keys():
            daily_remaining[sim_day + day, action] -= daily_sim_used_actions[day, action]
        for daily_customer, customer_path_no in cust_path_bin.keys():
            if cust_path_bin[daily_customer, customer_path_no] == 1:
                customers_selected_path[daily_customers[sim_day][daily_customer]] = customer_path_no



