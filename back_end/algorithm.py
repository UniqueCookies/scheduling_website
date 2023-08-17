from scheduling_website.back_end.schedule import *
import random

#create the size of population input by the user
def create_population(num_of_population, num_of_section, num_of_period, grade_level):
    # initailize the schedule
    course_key = get_course_key_list()
    # create a number of schedules
    population = []
    for _ in range(num_of_population):
        schedule = Schedule(num_of_section, num_of_period, grade_level, course_key)  # 2 sections, 6 periods  --> input by the user
        population.append(schedule)
    return population

#tournament selection
def tournament_selection(population,tournament_size):
    selected_parents = []

    tournament = random.sample(population, tournament_size)
    winner = max(tournament, key=lambda schedule: schedule.hcs)

    return winner

#Mutation Operator Section
#Single Mutation
def single_mutation(schedule):
    num_rows = len(schedule.matrix)
    num_cols = len(schedule.matrix[0])

    # Generate random row and column indices for the two elements to swap
    row1 = random.randint(0, num_rows - 1)
    col1 = random.randint(0, num_cols - 1)
    row2 = random.randint(0, num_rows - 1)
    col2 = random.randint(0, num_cols - 1)

    # Ensure the two sets of indices are distinct
    while row1 == row2 and col1 == col2:
        row2 = random.randint(0, num_rows - 1)
        col2 = random.randint(0, num_cols - 1)

    #swap the element
    schedule.swap_element(row1,col1,row2,col2)

    return schedule

#Hill climber for singler course
def hill_climber(schedule):
    num_rows = len(schedule.matrix)
    num_cols = len(schedule.matrix[0])
    iteration =0
    maxiterations=100

    # Generate random row and column indices for the two elements to swap
    row1 = random.randint(0, num_rows - 1)
    col1 = random.randint(0, num_cols - 1)
    row2 = random.randint(0, num_rows - 1)
    col2 = random.randint(0, num_cols - 1)

    #make sure this one is a clash, after certain iteration, assume no clash
    while not schedule.check_if_clash(row1,col1) and iteration<maxiterations:
        row1 = random.randint(0, num_rows - 1)
        col1 = random.randint(0, num_cols - 1)
        iteration +=1
    if not schedule.check_if_clash(row1,col1):
        return None

    iteration = 0
    #make sure 2nd swap is a clash is a clash
    while not schedule.check_if_clash(row2,col2) and iteration<maxiterations and row1 == row2 and col1 == col2:
        row2 = random.randint(0, num_rows - 1)
        col2 = random.randint(0, num_cols - 1)
        iteration += 1
    schedule.swap_element(row1, col1, row2, col2)

    if not schedule.check_if_clash(row2,col2): #only one teacher has a schedule conflict
        return False #still performed swap but it is a mutation with one clash
    return True
