#################
# POINTS SYSTEM #
#################
#  IF  GUESSED  #
#   CORRECTLY   #
#################
#   P1  # +3pts #
#   P2  # +2pts #
#   P3  # +1pts #
#################

def get_points(results, bet):
    round_points = 0

    for result in results:
        if result["position"] == 1 and result["Driver"]["code"] == bet["p1"]:
            round_points += 3

        if result["position"] == 2 and result["Driver"]["code"] == bet["p2"]:
            round_points += 2

        if result["position"] == 3 and result["Driver"]["code"] == bet["p3"]:
            round_points += 1

    return round_points
