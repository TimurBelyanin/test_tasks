def merge_intersections(lst: list) -> list:
    result = [lst[0]]
    for i in range(1, len(lst)):
        if lst[i][0] < result[-1][1]:
            if lst[i][1] > result[-1][1]:
                result[-1][1] = lst[i][1]
        else:
            result.append(lst[i])
    return result


def check_limits(lst: list, start: int, end: int) -> list:
    return list(filter(lambda interval: interval[1] > interval[0], map(lambda interval: [max(start, interval[0]), min(end, interval[1])], merge_intersections(lst))))


def create_pretty_intervals(lst: list, start: int, end: int) -> list:
    dest = []
    for ind, val in enumerate(lst):
        if ind % 2 != 0:
            dest.append([lst[ind - 1], lst[ind]])
    dest.sort(key=lambda x: x[0])
    dest = check_limits(dest, start, end)
    return dest


def appearance(intervals: dict[str, list[int]]) -> int:
    start = intervals['lesson'][0]
    end = intervals['lesson'][1]
    result = 0

    intervals_pupil = create_pretty_intervals(intervals['pupil'], start, end)
    intervals_tutor = create_pretty_intervals(intervals['tutor'], start, end)

    pupil = 0
    tutor = 0

    while pupil < len(intervals_pupil) and tutor < len(intervals_tutor):
        intersection = min(intervals_pupil[pupil][1], intervals_tutor[tutor][1]) - max(intervals_pupil[pupil][0], intervals_tutor[tutor][0])
        if intersection > 0:
            result += intersection
        if intervals_tutor[tutor][1] < intervals_pupil[pupil][1]:
            tutor += 1
        else:
            pupil += 1
    return result


tests = [
    {'intervals': {'lesson': [1594663200, 1594666800],
             'pupil': [1_594_663_340, 1_594_663_389, 1_594_663_390, 1_594_663_395, 1_594_663_396, 1594_666_472],
             'tutor': [1_594_663_290, 1_594_663_430, 1_594_663_443, 1_594_666_473]},
     'answer': 3117
    },
    {'intervals': {'lesson': [1594702800, 1594706400],
             'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
             'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
    'answer': 3577
    },
    {'intervals': {'lesson': [1594692000, 1594695600],
             'pupil': [1594692033, 1594696347],
             'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
    'answer': 3565
    },
]

if __name__ == '__main__':
    for i, test in enumerate(tests):
        test_answer = appearance(test['intervals'])
        assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
        print(test_answer)