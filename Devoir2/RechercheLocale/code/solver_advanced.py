from schedule import Schedule
import random
import math

def calculate_cost(schedule: Schedule, solution):
    """
    Calculate the cost of a solution.
    Cost = number of time slots used + penalty for conflicts
    """
    num_slots = len(set(solution.values()))
    
    conflicts = 0
    for course1, course2 in schedule.conflict_list:
        if solution[course1] == solution[course2]:
            conflicts += 1
    
    penalty = conflicts * 1000
    
    return num_slots + penalty


def generate_neighbor(solution):
    """
    Generate a neighbor solution by swapping time slots of two random courses.
    """
    neighbor = solution.copy()
    courses = list(solution.keys())
    
    course1, course2 = random.sample(courses, 2)
    
    neighbor[course1], neighbor[course2] = neighbor[course2], neighbor[course1]
    
    return neighbor


def acceptance_probability(current_cost, new_cost, temperature):
    """
    Calculate acceptance probability.
    """
    if new_cost < current_cost:
        return 1.0
    else:
        return math.exp(-(new_cost - current_cost) / temperature)


def simulated_annealing(schedule: Schedule, initial_solution, 
                       initial_temp=100, cooling_rate=0.95, 
                       iterations_per_temp=100, min_temp=0.01):
    """
    Apply Simulated Annealing to refine a solution.
    """
    current_solution = initial_solution.copy()
    current_cost = calculate_cost(schedule, current_solution)
    
    best_solution = current_solution.copy()
    best_cost = current_cost
    
    temperature = initial_temp
    
    while temperature > min_temp:
        for _ in range(iterations_per_temp):
            neighbor = generate_neighbor(current_solution)
            neighbor_cost = calculate_cost(schedule, neighbor)
            
            if random.random() < acceptance_probability(current_cost, neighbor_cost, temperature):
                current_solution = neighbor
                current_cost = neighbor_cost
                
                if current_cost < best_cost:
                    best_solution = current_solution.copy()
                    best_cost = current_cost
        
        temperature *= cooling_rate
    
    return best_solution


def solve(schedule: Schedule):
    """
    Your solution of the problem
    :param schedule: object describing the input
    :return: a dictionary where the keys are the courses and the values are the time periods associated
    """

    # Phase 1: Greedy initialization
    solution = {}

    # Sort courses by degree (number of conflicts) - helps reduce slots needed
    courses_by_degree = sorted(schedule.course_list,
                               key=lambda c: len(list(schedule.get_node_conflicts(c))),
                               reverse=True)

    for course in courses_by_degree:
        # Get all time slots used by conflicting courses
        conflicting_slots = set()
        for conflicting_course in schedule.get_node_conflicts(course):
            if conflicting_course in solution:
                conflicting_slots.add(solution[conflicting_course])

        # Find the first available slot (greedy algorithm)
        slot = 1
        while slot in conflicting_slots:
            slot += 1

        solution[course] = slot

    # Phase 2: Simulated Annealing refinement
    refined_solution = simulated_annealing(schedule, solution)

    return refined_solution