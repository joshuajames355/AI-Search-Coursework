import os
import sys
import time
import random
import math

def read_file_into_string(input_file, from_ord, to_ord):
    # take a file "input_file", read it character by character, strip away all unwanted
    # characters with ord < "from_ord" and ord > "to_ord" and return the concatenation
    # of the file as the string "output_string"
    the_file = open(input_file,'r')
    current_char = the_file.read(1)
    output_string = ""
    while current_char != "":
        if ord(current_char) >= from_ord and ord(current_char) <= to_ord:
            output_string = output_string + current_char
        current_char = the_file.read(1)
    the_file.close()
    return output_string

def stripped_string_to_int(a_string):
    # take a string "a_string" and strip away all non-numeric characters to obtain the string
    # "stripped_string" which is then converted to an integer with this integer returned
    a_string_length = len(a_string)
    stripped_string = "0"
    if a_string_length != 0:
        for i in range(0,a_string_length):
            if ord(a_string[i]) >= 48 and ord(a_string[i]) <= 57:
                stripped_string = stripped_string + a_string[i]
    resulting_int = int(stripped_string)
    return resulting_int

def get_string_between(from_string, to_string, a_string, from_index):
    # look for the first occurrence of "from_string" in "a_string" starting at the index
    # "from_index", and from the end of this occurrence of "from_string", look for the first
    # occurrence of the string "to_string"; set "middle_string" to be the sub-string of "a_string"
    # lying between these two occurrences and "to_index" to be the index immediately after the last
    # character of the occurrence of "to_string" and return both "middle_string" and "to_index"
    middle_string = ""              # "middle_string" and "to_index" play no role in the case of error
    to_index = -1                   # but need to initialized to something as they are returned
    start = a_string.find(from_string,from_index)
    if start == -1:
        flag = "*** error: " + from_string + " doesn't appear"
        #trace_file.write(flag + "\n")
    else:
        start = start + len(from_string)
        end = a_string.find(to_string,start)
        if end == -1:
            flag = "*** error: " + to_string + " doesn't appear"
            #trace_file.write(flag + "\n")
        else:
            middle_string = a_string[start:end]
            to_index = end + len(to_string)
            flag = "good"
    return middle_string,to_index,flag

def string_to_array(a_string, from_index, num_cities):
    # convert the numbers separated by commas in the file-as-a-string "a_string", starting from index "from_index",
    # which should point to the first comma before the first digit, into a two-dimensional array "distances[][]"
    # and return it; note that we have added a comma to "a_string" so as to find the final distance
    # distance_matrix = []
    if from_index >= len(a_string):
        flag = "*** error: the input file doesn't have any city distances"
        #trace_file.write(flag + "\n")
    else:
        row = 0
        column = 1
        row_of_distances = [0]
        flag = "good"
        while flag == "good":
            middle_string, from_index, flag = get_string_between(",", ",", a_string, from_index)
            from_index = from_index - 1         # need to look again for the comma just found
            if flag != "good":
                flag = "*** error: there aren't enough cities"
                # trace_file.write(flag + "\n")
            else:
                distance = stripped_string_to_int(middle_string)
                row_of_distances.append(distance)
                column = column + 1
                if column == num_cities:
                    distance_matrix.append(row_of_distances)
                    row = row + 1
                    if row == num_cities - 1:
                        flag = "finished"
                        row_of_distances = [0]
                        for i in range(0, num_cities - 1):
                            row_of_distances.append(0)
                        distance_matrix.append(row_of_distances)
                    else:
                        row_of_distances = [0]
                        for i in range(0,row):
                            row_of_distances.append(0)
                        column = row + 1
        if flag == "finished":
            flag = "good"
    return flag

def make_distance_matrix_symmetric(num_cities):
    # make the upper triangular matrix "distance_matrix" symmetric;
    # note that there is nothing returned
    for i in range(1,num_cities):
        for j in range(0,i):
            distance_matrix[i][j] = distance_matrix[j][i]

# read input file into string

#######################################################################################################
############ now we read an input file to obtain the number of cities, "num_cities", and a ############
############ symmetric two-dimensional list, "distance_matrix", of city-to-city distances. ############
############ the default input file is given here if none is supplied via a command line   ############
############ execution; it should reside in a folder called "city-files" whether it is     ############
############ supplied internally as the default file or via a command line execution.      ############
############ if your input file does not exist then the program will crash.                ############

input_file = "AISearchfile042.txt"

#######################################################################################################

# you need to worry about the code below until I tell you; that is, do not touch it!

if len(sys.argv) == 1:
    file_string = read_file_into_string("../city-files/" + input_file,44,122)
else:
    input_file = sys.argv[1]
    file_string = read_file_into_string("../city-files/" + input_file,44,122)
file_string = file_string + ","         # we need to add a final comma to find the city distances
                                        # as we look for numbers between commas
print("I'm working with the file " + input_file + ".")
                                        
# get the name of the file

name_of_file,to_index,flag = get_string_between("NAME=", ",", file_string, 0)

if flag == "good":
    print("I have successfully read " + input_file + ".")
    # get the number of cities
    num_cities_string,to_index,flag = get_string_between("SIZE=", ",", file_string, to_index)
    num_cities = stripped_string_to_int(num_cities_string)
else:
    print("***** ERROR: something went wrong when reading " + input_file + ".")
if flag == "good":
    print("There are " + str(num_cities) + " cities.")
    # convert the list of distances into a 2-D array
    distance_matrix = []
    to_index = to_index - 1             # ensure "to_index" points to the comma before the first digit
    flag = string_to_array(file_string, to_index, num_cities)
if flag == "good":
    # if the conversion went well then make the distance matrix symmetric
    make_distance_matrix_symmetric(num_cities)
    print("I have successfully built a symmetric two-dimensional array of city distances.")
else:
    print("***** ERROR: something went wrong when building the two-dimensional array of city distances.")

#######################################################################################################
############ end of code to build the distance matrix from the input file: so now you have ############
############ the two-dimensional "num_cities" x "num_cities" symmetric distance matrix     ############
############ "distance_matrix[][]" where "num_cities" is the number of cities              ############
#######################################################################################################

# now you need to supply some parameters ...

#######################################################################################################
############ YOU NEED TO INCLUDE THE FOLLOWING PARAMETERS:                                 ############
############ "my_user_name" = your user-name, e.g., mine is dcs0ias                        ############

my_user_name = "hrxb22"

############ "my_first_name" = your first name, e.g., mine is Iain                         ############

my_first_name = "Joshua"

############ "my_last_name" = your last name, e.g., mine is Stewart                        ############

my_last_name = "Smith"

############ "alg_code" = the two-digit code that tells me which algorithm you have        ############
############ implemented (see the assignment pdf), where the codes are:                    ############
############    BF = brute-force search                                                    ############
############    BG = basic greedy search                                                   ############
############    BS = best_first search without heuristic data                              ############
############    ID = iterative deepening search                                            ############
############    BH = best_first search with heuristic data                                 ############
############    AS = A* search                                                             ############
############    HC = hilling climbing search                                               ############
############    SA = simulated annealing search                                            ############
############    GA = genetic algorithm                                                     ############

alg_code = "GA"

############ you can also add a note that will be added to the end of the output file if   ############
############ you like, e.g., "in my basic greedy search, I broke ties by always visiting   ############
############ the first nearest city found" or leave it empty if you wish                   ############

added_note = ""

############ the line below sets up a dictionary of codes and search names (you need do    ############
############ nothing unless you implement an alternative algorithm and I give you a code   ############
############ for it when you can add the code and the algorithm to the dictionary)         ############

codes_and_names = {'BF' : 'brute-force search',
                   'BG' : 'basic greedy search',
                   'BS' : 'best_first search without heuristic data',
                   'ID' : 'iterative deepening search',
                   'BH' : 'best_first search with heuristic data',
                   'AS' : 'A* search',
                   'HC' : 'hilling climbing search',
                   'SA' : 'simulated annealing search',
                   'GA' : 'genetic algorithm'}

#######################################################################################################
############    now the code for your algorithm should begin                               ############
#######################################################################################################

tour = []
tour_length = 0

#Aiming for IDA*
#Start with ID, then add heuristic

#represent state as an array of city indices, first element is the intial city. - these represent a partial tour.
#A transition is adding on a new city to a partial tour.

def greedy(initialCity, distanceMatrix, numCities):
    state = [initialCity]
    while len(state) < numCities:
        currentCity = state[len(state)-1]

        best = -1
        bestScore = math.inf
        for x in range(num_cities):
            if x not in state:
                if distance_matrix[x][currentCity] < bestScore:
                    bestScore = distance_matrix[x][currentCity]
                    best = x
        state.append(best)
    return state


def genetic(distanceMatrix, numCities):
    POPULATION_SIZE = 100*2 #MUST BE EVEN
    NUM_ITERATIONS = 5000
    CROSSOVER_RATE = 0.4
    MUTATION_RATE = 0.02

    #Initial Population 
    population = [randomTour(numCities) for _ in range(1, POPULATION_SIZE)]
    population.append(greedy(0, distanceMatrix, numCities)) #TODO: BETTER SEEDING
    
    for i in range(NUM_ITERATIONS):
        #-----------------------SELECTION VIA Stochastic universal sampling---------------------------------------------
        if i % 100 == 0:
            fitness = [getTourLength(distanceMatrix, numCities, x) for x in population]
            _, min_score = min(enumerate(fitness), key=lambda x: x[1])
            print("\rIteration: {} Best Score: {}".format(i, min_score), end="")

        newPop = []

        fitness = [1/getTourLength(distanceMatrix, numCities, x) for x in population]
        numParents = POPULATION_SIZE//2

        distance = sum(fitness)/numParents
        i = 0
        total = random.random()*distance + fitness[0]
        while i < len(population):
            while total < distance:
                i += 1
                if i >= len(population):
                    break
                total += fitness[i]
            if i >= len(population):
                break
            newPop.append(population[i])
            total -= distance 

        #--------------------GENERATING NEXT GENERATION------------------------------------------------------------
        
        finalPop = [ population[max(enumerate(fitness), key=lambda x: x[1])[0]] ] #Elitism, maintain best solution
        
        #New random children
        while len(finalPop) < POPULATION_SIZE:
            #choose two different numbers to swap
            firstIndex, secondIndex = random.sample(range(numParents), 2)

            first = newPop[firstIndex]
            second = newPop[secondIndex]

            #CROSSOVER
            chance = random.random()
            if chance < CROSSOVER_RATE:
                first, second = pmco(first, second, numCities)

            #MUTATION
            chance = random.random()
            if chance < MUTATION_RATE:
                first = randomPermutation(first)
            chance = random.random()
            if chance < MUTATION_RATE:
                first = randomPermutation(second)

            finalPop += [first, second]

        population = finalPop
    
    fitness = [getTourLength(distanceMatrix, numCities, x) for x in population]
    min_index, _ = min(enumerate(fitness), key=lambda x: x[1])
    return population[min_index]


#Crossover operators, all return a tuple of 2 siblings

#Partially Mapped Crossover Operator
def pmco(tour1, tour2, numCities):
    #Get 2 cut points (x[0], x[1]) with x0 != x1 and x0 < x1
    cutPoints = [x for x in range(numCities+1)]
    random.shuffle(cutPoints)
    cutPoints = cutPoints[:2]
    cutPoints.sort()

    newTour1 = tour1[:]
    newTour2 = tour2[:]

    #Crossover
    for x in range(cutPoints[0], cutPoints[1]):
        newTour1[x] = tour2[x]
        newTour2[x] = tour1[x]

    crossover1 = tour1[cutPoints[0]:cutPoints[1]]
    crossover2 = tour2[cutPoints[0]:cutPoints[1]]

    #Map
    for x in range(numCities):
        if x >= cutPoints[0] and x < cutPoints[1]:
            continue
        while newTour1[x] in crossover2:
            newTour1[x] = crossover1[crossover2.index(newTour1[x])]

        while newTour2[x] in crossover1:
            newTour2[x] = crossover2[crossover1.index(newTour2[x])]

    return (newTour1, newTour2)

#cycle crossover
def cx(tour1, tour2, numCities):
    #Get 2 cut points (x[0], x[1]) with x0 != x1 and x0 < x1
    x = [x for x in range(numCities)]
    random.shuffle(x)
    x = x[:2]
    x.sort()


def randomTour(numCities):
    newTour = [x for x in range(numCities)]
    random.shuffle(newTour)
    return newTour

def randomPermutation(tour):
    chance = random.random()
    if chance < 0.01: #1% chance of reverse
        return tour[::-1]
    if chance < 0.06: #5% chance of randomize
        newTour = tour[:]
        random.shuffle(newTour)
        return newTour
    else:#otherwise swap two elements
        #choose two different numbers to swap
        first = random.randint(0, len(tour)-1)
        second = random.randint(0, len(tour)-2)
        if second >= first:
            second += 1

        #Do swap
        new = tour[:]
        temp = new[first]
        new[first] = new[second]
        new[second] = temp
        return new

def getTourLength(distanceMatrix, numCities, tour):
    length = distanceMatrix[tour[0]][tour[num_cities-1]]
    for x in range(0, numCities-1):
        length += distanceMatrix[tour[x]][tour[x+1]]
    return length

#runs a search function with the parameters distanceMatrix, numCities, and prints the result.
#then saves the result into the required global variables for the skeleton program to work
def go(f):
    global tour, tour_length
    result = f(distance_matrix, num_cities)
    print(result)
    tour = result
    tour_length = getTourLength(distance_matrix, num_cities, tour)

go(genetic)


#######################################################################################################
############ the code for your algorithm should now be complete and you should have        ############
############ computed a tour held in the list "tour" of length "tour_length"               ############
#######################################################################################################

# you do not need to worry about the code below; that is, do not touch it

#######################################################################################################
############ start of code to verify that the constructed tour and its length are valid    ############
#######################################################################################################

check_tour_length = 0
for i in range(0,num_cities-1):
    check_tour_length = check_tour_length + distance_matrix[tour[i]][tour[i+1]]
check_tour_length = check_tour_length + distance_matrix[tour[num_cities-1]][tour[0]]
flag = "good"
if tour_length != check_tour_length:
    flag = "bad"
if flag == "good":
    print("Great! Your tour-length of " + str(tour_length) + " from your " + codes_and_names[alg_code] + " is valid!")
else:
    print("***** ERROR: Your claimed tour-length of " + str(tour_length) + "is different from the true tour length of " + str(check_tour_length) + ".")

#######################################################################################################
############ start of code to write a valid tour to a text (.txt) file of the correct      ############
############ format; if your tour is not valid then you get an error message on the        ############
############ standard output and the tour is not written to a file                         ############
############                                                                               ############
############ the name of file is "my_user_name" + mon-dat-hr-min-sec (11 characters);      ############
############ for example, dcs0iasSep22105857.txt; if dcs0iasSep22105857.txt already exists ############
############ then it is overwritten                                                        ############
#######################################################################################################

if flag == "good":
    local_time = time.asctime(time.localtime(time.time()))   # return 24-character string in form "Tue Jan 13 10:17:09 2009"
    output_file_time = local_time[4:7] + local_time[8:10] + local_time[11:13] + local_time[14:16] + local_time[17:19]
                                                             # output_file_time = mon + day + hour + min + sec (11 characters)
    output_file_name = my_user_name + output_file_time + ".txt"
    f = open(output_file_name,'w')
    f.write("USER = " + my_user_name + " (" + my_first_name + " " + my_last_name + ")\n")
    f.write("ALGORITHM = " + alg_code + ", FILENAME = " + name_of_file + "\n")
    f.write("NUMBER OF CITIES = " + str(num_cities) + ", TOUR LENGTH = " + str(tour_length) + "\n")
    f.write(str(tour[0]))
    for i in range(1,num_cities):
        f.write("," + str(tour[i]))
    if added_note != "":
        f.write("\nNOTE = " + added_note)
    f.close()
    print("I have successfully written the tour to the output file " + output_file_name + ".")