import sys
import re
import numpy as np
from functools import lru_cache


def build_button(b, nmax):
    toggles = b.strip("(").strip(")").split(",")
    mask = []
    for i in range(nmax):
        mask.append(1 if str(i) in toggles else 0)

    return np.array(mask)


# def get_button_priority(button, argsort):
#     return sum([2**i if button[loc] else 0 for i, loc in enumerate(argsort)])


class JoltageChecker:
    def __init__(self, buttons: list[np.ndarray]):
        self.buttons = buttons
        # self.init_joltage = joltage
        self.cache = {}

    def distance_to_zero(self, joltage: np.ndarray, verbose: bool = False):
        # print(f"Testing joltage {joltage}")

        if tuple(joltage) in self.cache:
            return self.cache[tuple(joltage)]

        if (joltage == 0).all():
            self.cache[tuple(joltage)] = 0
            return 0

        else:
            bdistances = []
            for b in self.buttons:
                if ((joltage - b) == 0).all():
                    if verbose:
                        print(f"Button {b} goes to zero")
                    self.cache[tuple(joltage)] = 1
                    return 1
                elif ((joltage - b) >= 0).all():
                    if verbose:
                        print(f"{joltage} - {b} -> {joltage - b}")
                    bdistances.append(1 + self.distance_to_zero(joltage - b))
                else:
                    if verbose:
                        print(f"Button {b} goes negative ({joltage - b})")
                    bdistances.append(np.inf)

        if verbose:
            print(f"At joltage {joltage} we have distances {bdistances}")

        min_dist = min(bdistances)
        self.cache[tuple(joltage)] = min_dist
        return min_dist


if __name__ == "__main__":
    matcher = re.compile(r"^\[(.*)\] (\((?:\d+,*)+\).*)* \{(.*)\}$")

    total_presses = 0

    with open(sys.argv[1], "r") as f:
        for i_, line in enumerate(f):
            # if i_ != 1:
            # continue

            match = re.match(matcher, line)
            lights = match.group(1).replace(".", "0").replace("#", "1")
            n_lights = len(lights)
            buttons = [build_button(b, n_lights) for b in match.group(2).split()]
            target_light = int(lights, 2)
            joltage = np.array([int(i) for i in match.group(3).split(",")])

            print(f"Target {i_}: {joltage}")
            # argsort = np.argsort(joltage)[::-1]

            jc = JoltageChecker(buttons)
            n_presses = jc.distance_to_zero(joltage)
            print(f"Machine {i_} takes {n_presses} button presses")
            total_presses += n_presses

            # sorted_buttons = sorted(
            #     buttons, key=lambda x: get_button_priority(x, argsort), reverse=True
            # )

            # for b in sorted_buttons:
            #     running_sum = running_sum_last.copy()
            #     # k -= 1
            #     print(f"Applying {b} to {running_sum}")
            #     while (running_sum <= joltage).all():
            #         running_sum_last = running_sum.copy()
            #         running_sum += b
            #         if (running_sum <= joltage).all():
            #             k += 1
            #             print(f"After {k} steps: joltage={running_sum}")

            # print(f"Took {k} presses")
            # total_presses += k

        print(total_presses)
