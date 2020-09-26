import csv
from geopy.distance import great_circle

# dictionary to hold degrees of education
education = {
    "none": 0,
    "high school": 1,
    "undergraduate degree": 2,
    "master's degree": 3,
    "PhD": 4
}


def sc(em1, em2, ranking):
    person1_email = em1
    person2_email = em2

    person1 = {}
    person2 = {}

    ranklist = []
    sclist = []

    # same email check
    if person1_email == person2_email:
        print("Emails can not be the same.")

    # use DictReader to make each line of the csv file into a dictionary
    with open('UVEC-Fall-2020-Seed.csv') as f:
        reader = csv.DictReader(f)

        if ranking == 1:
            reader1 = csv.DictReader(f)
            for row in reader:
                if row['email'] == person1_email:
                    person1 = row

        else:
            for row in reader:
                if row['email'] == person1_email:
                    person1 = row

                if row['email'] == person2_email:
                    person2 = row

    # create a list of all compatible matches from the list, when ranking is on
    with open('UVEC-Fall-2020-Seed.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row == person1:
                continue
            if gendermatch(person1, row) == 1:
                ranklist.append(row)

    if ranking == 0:
        # if a person's gender does not match the other's gender preference, they should not be matched at all
        if gendermatch(person1, person2) == 1:

            return (person1['firstName'] + " " + person1['lastName'] + " & " +
            person2['firstName'] + " " + person2['lastName'] + " " + str(score_calc(20, person1, person2)))
        else:
            return 0

    else:
        # calculate the score of all matches and store them in a list
        for x in ranklist:
            sclist.append([str(score_calc(20, person1, x)), person1['firstName'] + " " + person1['lastName'] + " & " +
            x['firstName'] + " " + x['lastName']])

        sclist.sort(reverse=True)

        scclist = []

        r = 0

        # get the top 10 matches or just the top x number if there are not 10
        if len(sclist) < 10:
            r = len(sclist)
        else:
            r = 10

        for i in range(r):
            scclist.append((sclist[i][1] + " " + sclist[i][0]))

        return scclist


# determines if two people are compatible based on gender
def gendermatch(p1, p2):

    if p1['genderPreference'] == "anybody" and p2['genderPreference'] == p1['gender']:
        return 1

    if p2['genderPreference'] == "anybody" and p1['genderPreference'] == p2['gender']:
        return 1

    if p1['gender'] == "non-binary" and p2['genderPreference'] == "anyone":
        return 1

    if p2['gender'] == "non-binary" and p1['genderPreference'] == "anyone":
        return 1

    if p1['gender'] == p2['genderPreference'] and p2['gender'] == p1['genderPreference']:
        return 1
    else:
        return 0


# calculate the distance between two people
def distance_diff(p1, p2):
    d1 = (p1['lat'], p1['long'])
    d2 = (p2['lat'], p2['long'])

    return great_circle(d1, d2).kilometers


# calculate the age difference between two people
def age_diff(p1, p2):
    age1 = p1['age']
    age2 = p2['age']

    return abs(int(age1) - int(age2))


# calculate the score of two people's match
def score_calc(score, person1, person2):
    d = distance_diff(person1, person2)

    # if the distance between the two people is more than 20km, the score is reduced on an exponential scale
    if d > 20:
        calc = (2**(d/50))

        # if the distance is too great, the score for location will not be counted
        if calc <= 25:
            score += (25 - calc)

    # otherwise, 25 points are added
    else:
        score += 25

    # 5 bonus points for same city
    if person1['city'] == person2['city']:

        score += 5

    a = age_diff(person1, person2)

    # if the age difference is more than 5 on either side, the score is reduced on an exponential scale
    if a >= 5:
        calc = (2**(a/3))
        #print(calc)

        # if the age difference is too great, the score for location will not be counted
        if calc <= 23:
            score += (23 - calc)

    # otherwise, 23 points are added
    else:
        score += 23

    # 2 bonus points for same favorite animal
    if person1['favoriteAnimal'] == person2['favoriteAnimal']:
        score += 2

    # 2 bonus points for same level of education
    if person1['highestEducationLevel'] == person2['highestEducationLevel']:
        score += 2

    # otherwise, if the levels of education differ by only 1 degree, 1 point is added
    elif abs(education[person1['highestEducationLevel']] - education[person2['highestEducationLevel']]) == 1:
        score += 1

    # 2 bonus points for same favorite animal
    if person1['astrologicalSign'] == person2['astrologicalSign']:
        score += 1


    # 2 bonus points for same favorite music genre
    if person1['favoriteMusicGenre'] == person2['favoriteMusicGenre']:
        score += 5

    p1_job = person1['profession']
    p2_job = person2['profession']

    # 7 bonus points for same job
    if p1_job == p2_job:
        score += 7

    # otherwise, if the jobs share a similar word, 5 points are added
    else:
        p1_lst = p1_job.split()
        p2_lst = p2_job.split()

        for x in p1_lst:
            if x in p2_lst:
                score += 5
                break

    # if the smoking preference is the same, 10 points are added
    if person1['smoking'] == person2['smoking']:

        score += 10

    # if both people smoke, 7 points are added
    elif person1['smoking'] != "none" and person2['smoking'] != "none":

        score += 7

        # if both people smoke, but one vapes, 2 points are removed from 7, therefore 5 are added
        if person1['smoking'] == "vape" and person2['smoking'] != "vape":
            score -= 2

    score = round(score, 2)

    return score