def get_all_users_data(uuid):
    return {
        "users": [
            {
                "username": "test_user",
                "uuid": uuid
            }
        ]
    }


def get_user_by_id_data(uuid):
    return {
        "username": "test_user",
        "uuid": uuid,
        "points_2022": 6
    }


def create_user_data(uuid):
    return {
        "username": "test_user",
        "uuid": uuid
    }


def create_bet_data(uuid):
    return {
        "p1": "VER",
        "p2": "LEC",
        "p3": "PER",
        "season": 2022,
        "round": 22,
        "points": 6,
        "uuid": uuid
    }
