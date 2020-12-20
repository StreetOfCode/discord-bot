from config import SERVER_ID


def get_member(client, id):
    guild = get_server(client)
    member = guild.get_member(id)
    return member


def get_channel(client, id):
    guild = get_server(client)
    return guild.get_channel(id)


def get_server(client):
    return next(g for g in client.guilds if g.id == SERVER_ID)
