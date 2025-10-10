from schedule import Schedule
import time

def generate_initial_solution(schedule: Schedule):
    initial_solution = {}
    initial_time_slot = 1

    for c in schedule.course_list:
        initial_solution[c] = initial_time_slot  # Dictionary : key=course, value=time

    return initial_solution

def find_most_conflicting_course(schedule: Schedule, solution: dict):
    """
    Finds the course with the most conflicts in the current solution.
    A conflict occurs when a course is assigned to the same time slot as 
    one of its conflicting courses.
    
    :param schedule: Schedule object containing the conflict graph
    :param solution: Dictionary mapping courses to their assigned time slots
    :return: The course with the most conflicts, or None if no conflicts exist
    """
    max_conflicts = 0
    most_conflicting_course = None
    
    # Iterate through all courses
    for course in solution:
        course_conflicts = 0
        
        # Get all courses that conflict with this course
        conflicting_courses = schedule.get_node_conflicts(course)
        
        # Count how many conflicting courses are assigned to the same time slot
        for conflicting_course in conflicting_courses:
            if conflicting_course in solution:
                if solution[course] == solution[conflicting_course]:
                    course_conflicts += 1
        
        # Update if this course has more conflicts than the current maximum
        if course_conflicts > max_conflicts:
            max_conflicts = course_conflicts
            most_conflicting_course = course

    return most_conflicting_course

def count_total_conflicts(schedule: Schedule, solution: dict) -> int:
    """
    Count the total number of conflicts in the current solution.
    A conflict occurs when two courses that cannot be scheduled together
    are assigned to the same time slot.
    
    :param schedule: Schedule object containing the conflict graph
    :param solution: Dictionary mapping courses to their assigned time slots
    :return: Total number of conflicts (0 means valid solution)
    """
    total_conflicts = 0
    
    for course1, course2 in schedule.conflict_list:
        if course1 in solution and course2 in solution:
            if solution[course1] == solution[course2]:
                total_conflicts += 1
    
    return total_conflicts

def find_best_time_slot_for_course(schedule: Schedule, solution: dict, course) -> int:
    """
    Find the best time slot for a given course by trying all existing slots plus one new slot.
    The best slot is the one that minimizes total conflicts in the solution.
    
    :param schedule: Schedule object containing the conflict graph
    :param solution: Current solution dictionary
    :param course: The course to find the best slot for
    :return: The time slot that minimizes total conflicts
    """
    existing_slots = set(solution.values())
    
    # Add one new slot to try
    candidate_slots = list(existing_slots) + [max(existing_slots) + 1]
    
    best_slot = solution[course]  # Default to current slot
    min_conflicts = count_total_conflicts(schedule, solution)
    
    # Save original assignment
    original_slot = solution[course]

    for slot in candidate_slots:
        solution[course] = slot

        conflicts = count_total_conflicts(schedule, solution)

        if conflicts < min_conflicts:
            min_conflicts = conflicts
            best_slot = slot
    
    # Restore original assignment before returning
    solution[course] = original_slot
    
    return best_slot

def can_improve_solution(schedule: Schedule, solution: dict) -> bool:
    """
    Check if the solution can be improved by moving any course to a better time slot.
    
    :param schedule: Schedule object containing the conflict graph
    :param solution: Current solution dictionary
    :return: True if any course can be moved to reduce conflicts, False otherwise
    """
    current_conflicts = count_total_conflicts(schedule, solution)
    
    # Try to find a better slot for any course
    for course in solution:
        best_slot = find_best_time_slot_for_course(schedule, solution, course)
        
        # Save current slot
        original_slot = solution[course]
        
        # Temporarily move to best slot
        solution[course] = best_slot
        new_conflicts = count_total_conflicts(schedule, solution)
        
        # Restore original
        solution[course] = original_slot
        
        # If we found an improvement (or sideways move), return True
        if new_conflicts <= current_conflicts and best_slot != original_slot:
            return True
    
    return False

def solve(schedule: Schedule):
    """
    Your solution of the problem
    :param schedule: object describing the input
    :return: a dictionary where the keys are the courses and the values are the time periods associated
    """
    # Add here your agent
    solution = generate_initial_solution(schedule)
    
    timeout_seconds = 300  # 5 minutes timeout
    start_time = time.time()

    while can_improve_solution(schedule, solution):
        # Check if timeout has been exceeded
        elapsed_time = time.time() - start_time
        if elapsed_time > timeout_seconds:
            print(f"\nTimeout reached after {elapsed_time:.2f} seconds")
            break
        
        most_conflicting = find_most_conflicting_course(schedule, solution)
        
        if most_conflicting is None:
            break
        
        best_slot = find_best_time_slot_for_course(schedule, solution, most_conflicting)
        solution[most_conflicting] = best_slot
        
        
    
    # Final statistics
    final_conflicts = count_total_conflicts(schedule, solution)
    final_slots = len(set(solution.values()))
    print(f"Final conflicts: {final_conflicts}")
    print(f"Time slots used: {final_slots}")
    
    return solution