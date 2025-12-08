import sys
import numpy as np


def check_game(game: list[dict]):
    color_draws = {"red": [], "green": [], "blue": []}

    for draw in game:
        for color, value in draw.items():
            color_draws[color].append(value)

    min_dict = {k: max(v) for k, v in color_draws.items()}
    return min_dict


if __name__ == "__main__":
    games = []

    with open(sys.argv[1], "r") as f:
        for line in f:
            line = line.strip()
            # game_number = int(line.split(":")[0].split()[1])
            line_results = line.split(":")[1]
            draws = line_results.split(";")
            game_draws = []
            for draw in draws:
                draw_colors = {}
                cgroups = draw.split(",")
                for color_group in cgroups:
                    num, color = color_group.split()
                    num = int(num)
                    draw_colors[color] = num
                game_draws.append(draw_colors)
            games.append(game_draws)

        running_sum = 0
        for i, g in enumerate(games):
            running_sum += np.prod(list(check_game(g).values()))
        # okay_games = [
        #     idx + 1 for idx, game in enumerate(games) if check_game(game, totals)
        # ]
        print(running_sum)
