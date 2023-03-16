from login_functions import login, signup
import utilities as util

departments = {
    1: "Time Reporting",
    2: "Accounting",
    3: "Engineering",
    4: "Employee Records"
}

required_access_levels = {
    "Time Reporting": 1,
    "Accounting": 2,
    "Engineering": 2,
    "Employee Records": 3
}


def menu():
    """
    Runs the menu that allows for logins, signups, and department access
    """
    util.initialize_database()

    user_input = util.get_range_selection("Would you like to (1) Login or (2) Sign up: ", [1, 2])

    running = False

    # Login
    if user_input == 1:
        login_results = login()
        valid_login = login_results[0]
        access_level = login_results[1]

    # Sign up
    else:
        signup_results = signup()
        access_level = signup_results
        valid_login = True

    if valid_login:
        running = True

    while running:
        user_input = util.get_range_selection("Which area would you like to access?\n"
                                              "(1) for Time Reporting, (2) for Accounting,\n(3) for Engineering, "
                                              "(4) for Employee Records, (0) to sign out\n", [0, 4])
        if user_input == 0:
            print("Goodbye!")
            running = False
        else:
            open_department(departments[user_input], access_level)


def open_department(department: str, access_level: int):
    """
    Opens the given department if the access level is high enough
    :param department: The department to access
    :param access_level: The current user's access level
    """

    if access_level >= required_access_levels[department]:
        print("\n***** Welcome to the " + department + " Department! *****\n")
    else:
        print("\n***** Sorry, you do not have access to this department. *****\n")


if __name__ == "__main__":
    menu()
