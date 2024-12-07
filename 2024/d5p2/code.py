import sys
import numpy as np

def check_update(update, rules_mtx):
    for i, page in enumerate(update):
        other_pages = update.copy()
        other_pages.remove(page)
        page_rules = rules_mtx[page, other_pages[i:]]
        if (page_rules < 0).any():
            return False
    return True

def fix_update(update, rules_mtx):
    fixed = update.copy()

    fixed_update = sorted(fixed, key = lambda x: rules_mtx[x,update].sum(), reverse=True)
    # for i, page in enumerate(update):
    #     other_pages = update.copy()
    #     other_pages.remove(page)
    #     page_rules = rules_mtx[page, other_pages[i:]]
    #     if (page_rules < 0).any():
    #         update[i] = other_pages[np.argmin(page_rules)]
    return fixed_update

if __name__ == "__main__":

    rules = []
    updates = []
    all_pages = set()

    with open(sys.argv[1]) as f:
        line = f.readline()
        while line.strip() != "":
            a,b = line.strip().split("|")
            all_pages.add(int(a))
            all_pages.add(int(b))
            rules.append((int(a), int(b)))
            line = f.readline()
        for line in f:
            updates.append([int(i) for i in line.strip().split(",")])

    # build rule matrix
    rule_mtx = np.zeros((max(all_pages)+1, max(all_pages)+1))
    for (ra, rb) in rules:
        rule_mtx[ra, rb] = 1
        rule_mtx[rb, ra] = -1
    # for u in updates:
        # print(u, check_update(u, rule_mtx))
    # print("######")

    bad_updates = [up for up in updates if not check_update(up, rule_mtx)]
    fixed_updates = [fix_update(up, rule_mtx) for up in bad_updates]

    for (up, fup) in zip(bad_updates, fixed_updates):
        print(f"Bad update: {up} -> {fup}")

    score = sum(up[len(up)//2] for up in fixed_updates)
    print(score)