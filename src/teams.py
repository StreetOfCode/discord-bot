def create(names, number_of_teams, shuffle_fn=None):
    if len(names) < number_of_teams:
        return names

    if shuffle_fn:
        shuffle_fn(names)

    teams = []
    for i in range(number_of_teams):
        teams.append([])

    for i, item in enumerate(names):
        teams[i % number_of_teams].append(item)

    return teams
