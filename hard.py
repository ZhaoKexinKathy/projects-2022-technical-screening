"""
Inside conditions.json, you will see a subset of UNSW courses mapped to their 
corresponding text conditions. We have slightly modified the text conditions
to make them simpler compared to their original versions.

Your task is to complete the is_unlocked function which helps students determine 
if their course can be taken or not. 

We will run our hidden tests on your submission and look at your success rate.
We will only test for courses inside conditions.json. We will also look over the 
code by eye.

NOTE: This challenge is EXTREMELY hard and we are not expecting anyone to pass all
our tests. In fact, we are not expecting many people to even attempt this.
For complete transparency, this is worth more than the easy challenge. 
A good solution is favourable but does not guarantee a spot in Projects because
we will also consider many other criteria.
"""
import json
import string
import re

# NOTE: DO NOT EDIT conditions.json
with open("./conditions.json") as f:
    CONDITIONS = json.load(f)
    f.close()


def decide_course_level():
    course_level = {}
    split_conditions = {}
    for k in CONDITIONS:
        split_conditions[k] = CONDITIONS[k].strip().replace("(", "( ").replace(")", " )").replace(",", "").replace(".","").split()
    for k in split_conditions:
        if not split_conditions[k]:
            course_level[k] = 0
        else:
            for conditions in split_conditions[k]:
                if conditions in course_level and (k not in course_level or course_level[k] > course_level[conditions] + 1):
                    course_level[k] = course_level[conditions] + 1
            if k not in course_level:
                course_level[k] = 1
    return course_level


def is_valid(courses_list, statement):
    # check the truth of one statement
    if len(statement) == 1:
        # prerequisite is some specific courses
        if statement[0] in courses_list:
            return "True" if statement[0] in courses_list else "False"
    if len(statement) == 9 and statement[1:6] == ["units", "of", "credit", "in", "level"]:
        # deal with "12 units of credit in  level 1 COMP courses" like statement
        course_level = decide_course_level()
        total_credit = 0
        for course in course_level:
            if course_level[course] == statement[6]:
                total_credit += 6
        return "True" if total_credit >= int(statement[0]) else "False"
    if (len(statement)) == 7:
        # deal with " 36 units of credit in COMP courses "
        subject = statement[5]
        total_credit = 0
        for course in courses_list:
            if course.startswith(subject):
                total_credit += 6
        return "True" if total_credit >= int(statement[0]) else "False"

    if statement[1:6] == ["units", "of", "credit", "in", "("]:
        # 18 units of credit in (COMP9417, COMP9418, COMP9444, COMP9447)
        courses_range = statement[6:10]
        total_credit = 0
        for course in courses_list:
            if course in courses_range:
                total_credit += 6
        return "True" if total_credit >= int(statement[0]) else "False"

    if (len(statement)) == 4:
        #  24 units of credit
        return "True" if len(courses_list) * 6 >= int(statement[0]) else "False"
    return "False"


def is_unlocked(courses_list, target_course):
    """Given a list of course codes a student has taken, return true if the target_course 
    can be unlocked by them.

    You do not have to do any error checking on the inputs and can assume that
    the target_course always exists inside conditions.json

    You can assume all courses are worth 6 units of credit
    """
    
    # TODO: COMPLETE THIS FUNCTION!!!
    conditions = CONDITIONS[target_course]
    if conditions == '':
        return True
    conditions = conditions.strip().replace("(", "( ").replace(")", " )").replace(",", "").replace(".", "").split()
    i = 0
    # convert the conditions to the expression of statements
    statements = ""
    while i < len(conditions):
        if conditions[i].lower() in ["and", "or", "(", ")"]:
            statements += conditions[i].lower()
            i += 1

        elif len(re.findall(r"\d", conditions[i])) == 4:
            statements += is_valid(courses_list, [conditions[i]])
            i += 1

        elif 0 < len(re.findall(r"\d", conditions[i])) < 4 and i+3 < len(conditions) and conditions[i+1:i+4] == ["units", "of", "credit"]:
            if i+8 < len(conditions) and conditions[i+4] == "in":
                if conditions[i+5] == "level":
                    # 12 units of credit in  level 1 COMP courses
                    statements += is_valid(courses_list, conditions[i:i + 9])
                    i += 9
                elif conditions[i+5] == "COMP":
                    # 36 units of credit in COMP courses
                    statements += is_valid(courses_list, conditions[i:i + 8])
                    i += 8
                else:
                    # 12 units of credit in (COMP6443,  COMP6843, COMP6445, COMP6845, COMP6447)
                    j = i + 5
                    if conditions[j] == "(":
                        while conditions[j] != ")":
                            j += 1
                        j += 1
                        statements += is_valid(courses_list, conditions[i:j])
                        i = j
            else:
                # 102 units of credit
                statements += is_valid(courses_list, conditions[i:i+4])
                i += 4

        else:
            i += 1
        statements += " "
    return eval(statements)

