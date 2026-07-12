def calculate_scores(answers):

    total_scores = {
        "AI": 0,
        "CLD": 0,
        "CYB": 0,
        "DS": 0,
        "SE": 0
    }

    for answer in answers.values():

        for domain, points in answer["scores"].items():

            total_scores[domain] += points

    return total_scores

def calculate_percentages(scores):
    total = sum(scores.values())

    percentages = {}

    for domain, score in scores.items():
        percentages[domain] = round((score / total) * 100, 1)

    return percentages