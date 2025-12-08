import sys


def check_game(game: list[dict], totals: dict):
    for draw in game:
        for color, value in draw.items():
            if value > totals[color]:
                return False
    return True


if __name__ == "__main__":
    games = []

    totals = {
        "red": 12,
        "green": 13,
        "blue": 14,
    }

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

        okay_games = [
            idx + 1 for idx, game in enumerate(games) if check_game(game, totals)
        ]
        print(sum(okay_games))
