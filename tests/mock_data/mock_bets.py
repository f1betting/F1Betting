def create_bet_data(uuid):
    return {
        "p1": "ALB",
        "p2": "ALO",
        "p3": "BOT",
        "uuid": uuid,
        "season": 2022,
        "round": 22,
        "points": 0
    }


def create_bet_put_data(uuid):
    return {
        "p1": "ALB",
        "p2": "BOT",
        "p3": "ALO",
        "uuid": uuid,
        "season": 2022,
        "round": 22,
        "points": 0
    }

def create_wrong_user_data(uuid):
    return {
        "username": "wrong_user",
        "uuid": uuid
    }