#############################################################
# CONFIG ####################################################
#############################################################

num_sims = 10**1
num_towns = 15
starting_pop = 10**2
probabilities = (0.9,0.05,0.05) # stay, move, don't reproduce

#############################################################
#############################################################
#############################################################

import random
from statistics import mean, median, mode

print(f"Number of simulations: {num_sims}")
print(f"Starting with {num_towns} towns, each of {starting_pop} people")
towns = range(num_towns)

def print_gen(gen):
    total = 0
    for person in gen:
        special = ""
        if person[2] == 1:
            special = "*"
        print(f"{person[0]}{person[1]}{special}",end=" ")
        total += person[2]
    print(f"\nNumber of *: {total}")
    return total

def count_gen(gen):
    total1 = len(gen)
    total2 = 0
    for person in gen:
        total2 += person[2]
    # print(f"{total1} people, {total2}* ({int(total2/total1*100)}%)")
    return total1, total2

def swap_town(town):
    targets = []
    for t in towns:
        if t != town:
            targets.append(t)
    return random.choice(targets)

def init_gen():
    gen = []
    special=1
    person_no = 1
    for town in towns:
        for person in range(0,starting_pop):
            gen.append([town,person_no,special])
            special=0
            person_no+=1
    return gen

end_counts = []
end_pops = []
num_extinct = 0
num_full = 0

for s in range(0,num_sims):
    next_gen = init_gen()

    # print("Generation 0: ", end="")
    num_people, num_stars = count_gen(next_gen)

    c=0
    while num_stars>0 and c<20: # num_stars<len(next_gen):
        c+=1
        this_gen = next_gen.copy()
        next_gen = []
        person_no = 1

        # setup towns to hold reproducing people
        repo_people = {}
        for town in towns:
            repo_people[town] = []

        for person in this_gen:
            odds = random.random()
            if odds < probabilities[0]:
                repo_people[person[0]].append(person)
            elif odds < probabilities[0]+probabilities[1]:
                repo_people[swap_town(person[0])].append(person)

        for town in repo_people:
            people = repo_people[town].copy()
            if len(people)>1: # if there's only one breeding person here, they don't reproduce
                while len(people):
                    if len(people)>1: # if there are people, pair them
                        person1 = people.pop(0)
                        random.shuffle(people)
                        person2 = people.pop(0)
                    else: # only one person left, pick a second union
                        person1 = people.pop(0)
                        person2 = person1
                        while person1 == person2:
                            person2 = random.choice(repo_people[town])

                    special=0
                    if person1[2]==1 or person2[2]==1:
                        special=1
                    
                    num_kids = random.randint(1,4) # between 1 and 4 children surviving to breeding age for this couple
                    for i in range(num_kids):
                        next_gen.append([town,person_no,special])
                        person_no+=1

        # print(f"Generation {c}: ", end="")
        num_people, num_stars = count_gen(next_gen)

    if num_stars == 0:
        num_extinct += 1
    else:
        end_counts.append(num_stars)
        end_pops.append(num_people)
        if num_people == num_stars:
            num_full += 1

# print(end_counts)
print(f"Number extinct: {num_extinct} ({int(num_extinct/num_sims*100)}%)")

print("From the simulations which completed without extinction:")

print(f"Number all *: {num_full} ({int(num_full/(num_sims-num_extinct)*100)}%)")

print("End population size:")
print(f"Min: {min(end_pops)}")
print(f"Max: {max(end_pops)}")
print(f"Mean: {round(mean(end_pops),1)}")
print(f"Median: {median(end_pops)}")
print(f"Mode: {mode(end_pops)}")

print("End number related to *:")
print(f"Min: {min(end_counts)}")
print(f"Max: {max(end_counts)}")
print(f"Mean: {round(mean(end_counts),1)}")
print(f"Median: {median(end_counts)}")
print(f"Mode: {mode(end_counts)}")