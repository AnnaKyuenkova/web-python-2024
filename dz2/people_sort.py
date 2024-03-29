import operator

def person_lister(f):
    def inner(people):
        people.sort(key=operator.itemgetter(2))
        formatted_people = [f(person) for person in people]
        return formatted_people
    return inner

@person_lister
def sort_people(person):
    return ("Mr. " if person[3] == "M" else "Ms. ") + person[0] + " " + person[1]