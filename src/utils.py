from config import SERVER_ID, ADMIN_ROLE
from discord.utils import get


def get_member(client, member_id):
    guild = get_server(client)
    member = guild.get_member(member_id)
    return member


def get_channel(client, member_id):
    guild = get_server(client)
    return guild.get_channel(member_id)


def get_server(client):
    return next(g for g in client.guilds if g.id == SERVER_ID)


def is_admin(member):
    return ADMIN_ROLE in [role.name for role in member.roles]


def has_role(member, role_name):
    return role_name in [role.name for role in member.roles]


def get_role(client, name):
    return get(get_server(client).roles, name=name)
