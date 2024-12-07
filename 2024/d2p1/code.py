import sys
import numpy as np

def check_safe(report: np.ndarray) -> bool:
    report_buffered = np.concatenate([report, np.array([np.infty])])

    diffs = (report - report_buffered[1:])[:-1]
    # print(f"diffs {diffs}")

    check1 = ((diffs) < 0).all() or ((diffs) > 0).all()
    check2 = ((diffs.min() >= 1) and (diffs.max() <= 3)) or ((diffs.min() >= -3) and (diffs.max() <= -1))
    # print(f"check1: {check1}, check2: {check2}")
    if check1 and check2:
        return True
    return False

if __name__ == "__main__":
    file = sys.argv[1]

    safe_reports = 0
    with open(file, "r") as f:
        for line in f:
            report = np.array([int(i) for i in line.strip().split()])
            # print(report, check_safe(report))
            if check_safe(report):
                safe_reports += 1
    print(safe_reports)
    