from schedule import Schedule

def solve(schedule: Schedule):
    """
    Your solution of the problem
    :param schedule: object describing the input
    :return: a dictionary where the keys are the courses and the values are the time periods associated
    """

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

    return solution