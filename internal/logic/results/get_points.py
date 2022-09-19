def get_points(results, bet):
    round_points = 0

    for result in results:
        if result["position"] == 1:
            if result["Driver"]["code"] == bet["p1"]:
                round_points += 3

        if result["position"] == 2:
            if result["Driver"]["code"] == bet["p2"]:
                round_points += 2

        if result["position"] == 3:
            if result["Driver"]["code"] == bet["p3"]:
                round_points += 1

    return round_points
