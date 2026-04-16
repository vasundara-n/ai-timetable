def is_valid(subject, slot, assignment):
    return slot not in assignment.values()

def backtrack(subjects, slots, assignment={}):
    if len(assignment) == len(subjects):
        return assignment

    subject = subjects[len(assignment)]

    for slot in slots:
        if is_valid(subject, slot, assignment):
            assignment[subject] = slot
            result = backtrack(subjects, slots, assignment)
            if result:
                return result
            del assignment[subject]

    return None
