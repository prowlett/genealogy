# import time

# start_time=time.time()
# print(f"Start at: {start_time}")

#############################################################
# CONFIG ####################################################
#############################################################

num_sims = 10**2
starting_pop = 2*10**6#15*10**3
probability = 0.95

#############################################################
#############################################################
#############################################################

import random
from statistics import mean, median, mode

def count_gen(gen):
    total1 = len(gen)
    total2 = 0
    for person in gen:
        total2 += person[1]
    print(f"{total1} people, {total2}* ({int(total2/total1*100)}%)")
    return total1, total2

def init_gen():
    gen = []
    special=1
    person_no = 1
    for person in range(0,starting_pop):
        gen.append([person_no,special])
        special=0
        person_no+=1
    return gen

end_counts = []
end_pops = []
num_extinct = 0
num_full = 0

# start_this_sim = start_time

for s in range(0,num_sims):
    # start_this_sim = time.time()

    next_gen = init_gen()

    print("Generation 0: ", end="")
    num_people, num_stars = count_gen(next_gen)

    c=0
    while num_stars>0 and num_stars<len(next_gen):
        c+=1
        this_gen = next_gen.copy()
        next_gen = []
        person_no = 1

        random.shuffle(this_gen)

        i=0
        tot_people = len(this_gen)
        if len(this_gen)>1: # if there's only one breeding person, they don't reproduce
            while i<tot_people: # if there are people, pair them
                # print(i)
                # since the order of this_gen is already random, pair adjacent couples
                while random.random() > probability: # this one didn't reproduce, skip to next
                    i += 1
                if i<tot_people:
                    person1 = this_gen[i]
                    i += 1
                    while random.random() > probability: # this one didn't reproduce, skip to next
                        i += 1
                    if i<tot_people:
                        person2 = this_gen[i]
                        i += 1
                    #else: # only one person left, pick a second union
                        # since the order of this_gen is already random, use whoever is already assigned to person2
                    # print(person1)
                    # print(person2)

                    # print("their kids:")

                    special=0
                    if person1[1]==1 or person2[1]==1:
                        special=1
                    
                    num_kids = random.randint(1,4) # between 1 and 4 children surviving to breeding age for this couple
                    for k in range(num_kids):
                        # print(f"{person_no},{special}")
                        next_gen.append([person_no,special])
                        person_no+=1


                    # print("++++++++++")

        print(f"Generation {c}: ", end="")
        num_people, num_stars = count_gen(next_gen)

    if num_stars == 0:
        num_extinct += 1
    else:
        end_counts.append(c)
        end_pops.append(num_people)
    
    # end_this_sim = time.time()
    # dur = end_this_sim-start_this_sim
    # print(f"Simulation {s} complete ({round(dur,2)}s)")

# end_time=time.time()-start_time


print(f"Number of simulations: {num_sims}")
print(f"Starting with {starting_pop} people")

# print(end_counts)
print(f"Number extinct: {num_extinct} ({int(num_extinct/num_sims*100)}%)")

print("From the simulations which completed without extinction:")

print("End population size:")
print(f"Min: {min(end_pops)}")
print(f"Max: {max(end_pops)}")
print(f"Mean: {round(mean(end_pops),1)}")
print(f"Median: {median(end_pops)}")
print(f"Mode: {mode(end_pops)}")

print("Number of generations:")
print(f"Min: {min(end_counts)}")
print(f"Max: {max(end_counts)}")
print(f"Mean: {round(mean(end_counts),1)}")
print(f"Median: {median(end_counts)}")
print(f"Mode: {mode(end_counts)}")

# print(f"End at: {end_time}")
