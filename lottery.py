import random
import re

NUM_SEATS = 40

# Randomly allocate a fixed number (NUM_SEATS) of seats of more than
# seats are requested than available.
# The input is an open file, each of whose lines are of the form
# <n> <name>
# where <n> is the number of seats requested by <name>.

# The output is a string containing the answer or an error message.
def lottery(content):
    entries = []
    line_number = 0
    for c in content:
        try:
            line = c.decode("utf-8")
        except:
            return "The file is not a text file"
        line_number += 1
        m = re.match(r"^\d+ +", line, re.ASCII)
        if m:
            count = int(m.group())
            if count == 0:
                return f"Format error on line {line_number}\n{line}\n"
            entries.append((int(m.group()), line[m.end() : -1]))
        else:
            return f"Format error on line {line_number}\n{line}\n"

    selected = select(entries)
    selected.sort(key=lambda x: x[1])
    m = "".join(map(lambda s: (f"{s[0]:2} {s[1]}\n"), selected))
    return f"{sum(x[0] for x in selected)} seats filled:\n{m}"


def attempt(entries):
    seats_left = NUM_SEATS
    selected = []
    while True:
        # Filter out entries we don't have seats left to fill.
        entries = list(filter(lambda x: x[0] <= seats_left, entries))

        # Quit if there are no more contenders.
        if not entries:
            return selected

        # Choose a group to admit.
        # Every individual has the same chance of getting in,
        # but if a member of group gets in, the whole group gets in.
        picked = random.randrange(len(entries))
        p = entries[picked]
        del entries[picked]
        seats_left -= p[0]
        selected.append(p)


def select(entries):
    if sum(e[0] for e in entries) <= NUM_SEATS:
        # Everybody gets in
        return entries

    # The attempt algorithm is fair, but may not fill all the seats.
    # If that happens, try again. But don't keep trying forever. For some
    # inputs, it is impossible to fill all the seats.
    tries = 25
    for i in range(1, tries + 1):
        s = attempt(entries)
        if i == tries or sum(e[0] for e in s) == NUM_SEATS:
            return s
