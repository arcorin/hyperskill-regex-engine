# write your code here
# import re
import sys

sys.setrecursionlimit(10000)


def check_strings(r, s):
    """Compares the pair regex|string: character by character, recursively,
       and returns to the main function the result True or False of the comparison"""

    # if regex is empty (and string is empty or not) => match
    if r == "":
        return True

    # if string is empty:
    if s == "":

        # regex is not empty => no match
        if r[0] != "$" or len(r) > 1:
            return False

        # regex must be at the end of the string =>...
        # ...=> regex and string end with the same character => match
        if r[0] == "$" and len(r) == 1:
            return True

    # if the escape character is followed by a metacharacter or by another escape char:
    if r[:2] in ["\\.", "\\?", "\\*", "\\+", "\\\\"]:

        # if string starts with the second character from regex...
        # ...(metacharacter or escape character) =>...
        # ...=> check recursively the next characters in regex and string
        if r[1] == s[0]:
            return check_strings(r[2:], s[1:])

        # else => no match
        else:
            return False

    # if the first character in regex is ? or * (regex starts with ? or *)
    if r[0] in ["?", "*"]:

        # check recursively the next characters in regex and the entire string
        return check_strings(r[1:], s)

    # else if regex starts with wild card (.) or with the same character as string...
    # ...check if the second character in regex is one of the metacharacters * or + :
    elif r[0] in [s[0], "."]:

        # if the second character in regex is not a metacharacter * or + ...
        # ... check recursively next characters in regex and string
        if (len(r) > 1 and r[1] not in ["*", "+"]) or len(r) == 1:
            r = r[1:]
            s = s[1:]

        # if the string has one or more characters equal with...
        # ...the character preceding the metacharacter * or + from regex:
        elif len(r) > 1 and r[1] in ["*", "+"]:

            # the character to be compared (char) is equal with:
            # ... the first char in regex if regex does not start with the wild card (.)
            if r[0] != ".":
                char = r[0]

            # ... the first char in string if regex starts with the wild card (.)
            else:
                char = s[0]
            r = r[2:]

            # loop over all first characters in string identical with char:
            while len(s) > 0 and s[0] == char:
                s = s[1:]

        # check recursively the next characters in regex and string
        return check_strings(r, s)

    # if the first character in regex is not a metachar or equal with...
    # ...the first character in string:
    else:

        # if the second character in regex is not a metachar ? or *...
        # ... or the regex has no more characters => no match
        if (len(r) > 1 and r[1] not in ["?", "*"]) or len(r) in range(1, 3):
            return False

        # if the second character in regex is a metachar ? or *...
        # ...and regex has more characters => ...
        # ...check recursively the next characters in regex and the entire string
        elif len(r) > 2 and r[1] in ["?", "*"]:
            r = r[2:]
            return check_strings(r, s)

        # if regex starts with one or two escape characters...
        # ...check recursively the next characters in regex and the entire string
        elif len(r) > 2 and r[0] == "\\":
            r = r[1:]
            return check_strings(r, s)
        elif len(r) > 2 and r[:2] == "\\\\":
            r = r[2:]
            return check_strings(r, s)


def main():
    """ Main function: takes the input, checks and prepare the input
        (checks if the input is 'exit', split it in regex and string,
         checks if it starts with the metachar ^, check if regex or string are empty)
         and, while regex and string are not empty, prints the result True or False
         returned by the function check_strings() with arguments regex and string """

    a = input()

    if a == "exit":
        exit()

    # split the input in regex and string
    regex, string = a.split("|")

    # if regex starts with the metachar ^ check with function check_strings()...
    # ... the next characters in regex and the entire string
    if regex.startswith("^"):
        regex = regex[1:]
        result = check_strings(regex, string)

    # if regex is empty => match
    elif regex == "":
        result = True
    # if string is empty => no match
    elif string == "":
        result = False

    # while regex and string are not empty check if they match...
    # ...with the function check_strings()
    else:
        while len(regex) and len(string):
            result = check_strings(regex, string)

            # stop the loop if the result returned by the function is true...
            # ...(regex and string match)
            if result:
                break

            # if the result is false remove the first character from string and...
            # ...compare again in the while loop the regex and the new string
            else:
                string = string[1:]

    print(result)
    # uncomment main() to execute the program in loop
    # main()


main()
