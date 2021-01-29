from unittest.mock import Mock

from src.log_utils import channel_to_string, member_to_string


def test_member_to_string():
    member = Mock()
    member.id = 10
    member.name = "name"

    assert member_to_string(member) == "(10, name)"


def test_channel_to_string():
    channel = Mock()
    channel.id = 10
    channel.name = "name"

    assert channel_to_string(channel) == "(10, name)"
