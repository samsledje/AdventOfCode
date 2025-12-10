import sys
import re
import numpy as np


def str_binary(number: int, length: int):
    return bin(number)[2:].zfill(length)


def print_memory(memory: dict[tuple[int, int]]):
    max_len = max([len(bin(i[0])[2:]) for i in memory.keys()])
    for (init_state, button), end_state in memory.items():
        start_repr = str_binary(init_state, max_len)
        button_repr = str_binary(button, max_len)
        end_repr = str_binary(end_state, max_len)
        print(f"{start_repr} + {button_repr} -> {end_repr}")


def build_button_mask(b, nmax):
    toggles = b.strip("(").strip(")").split(",")
    mask = ""
    for i in range(nmax):
        mask += "1" if str(i) in toggles else "0"

    return int(mask, 2)


def update_lights(lights: int, button: int, verbose: bool = False):
    if verbose:
        print("+")
        print(bin(button))
    return lights ^ button


if __name__ == "__main__":
    matcher = re.compile(r"^\[(.*)\] (\((?:\d+,*)+\).*)* \{(.*)\}$")

    machines = []

    with open(sys.argv[1], "r") as f:
        for line in f:
            match = re.match(matcher, line)
            lights = match.group(1).replace(".", "0").replace("#", "1")
            nlights = len(lights)
            buttons = [build_button_mask(b, nlights) for b in match.group(2).split()]
            target_light = int(lights, 2)
            joltage = np.array([int(i) for i in match.group(3).split(",")])
            machines.append((lights, buttons, joltage))

            # print(indicators)
            # print(buttons)
            # print(joltage)

    for i, (lights, buttons, joltage) in enumerate(machines):
        print(f"### MACHINE {i} ###")
        memory = {}
        old_lights = 0

        for b in buttons:
            new_lights = update_lights(old_lights, b)
            memory[(old_lights, b)] = new_lights
            old_lights = new_lights

        print_memory(memory)
