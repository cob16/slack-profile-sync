import pytest

from slack_profile_update.domain.slackuser import SlackUser
from slack_profile_update.gateway.stub_user_link_store import StubUserLinkStore


def test_link():
    gateway = StubUserLinkStore()
    user1 = "user1"
    user2 = "user2"
    gateway.link(user1, user2)
    assert gateway.fetch(user1) == {user2}
    assert gateway.fetch(user2) == {user1}


def test_unlink_is_silent_when_user_not_found():
    gateway = StubUserLinkStore()
    user1 = "user1"
    user2 = "user2"
    gateway.link(user1, user2)

    gateway.unlink("random user id")


def test_unlink_with_2_users():
    gateway = StubUserLinkStore()
    user1 = "user1"
    user2 = "user2"
    gateway.link(user1, user2)

    gateway.unlink(user1)

    with pytest.raises(KeyError):
        gateway.fetch(user1)
    with pytest.raises(KeyError):
        gateway.fetch(user2)


def test_unlink_with_3_users():
    gateway = StubUserLinkStore()
    user1 = "user1"
    user2 = "user2"
    user3 = "user3"
    gateway.link(user1, user2)
    gateway.link(user1, user3)

    gateway.unlink(user3)

    assert gateway.fetch(user1) == {user2}
    assert gateway.fetch(user2) == {user1}

    with pytest.raises(KeyError):
        gateway.fetch(user3)


def test_key_error_raised():
    gateway = StubUserLinkStore()
    with pytest.raises(KeyError):
        gateway.fetch("key_not_found")


def test_link_2_separate_users():
    gateway = StubUserLinkStore()
    user1 = "user1"
    user2 = "user2"

    gateway.link(user1, user2)
    assert gateway.fetch(user1) == {user2}
    assert gateway.fetch(user2) == {user1}

    user3 = "user3"
    user4 = "user4"
    gateway.link(user3, user4)
    assert gateway.fetch(user3) == {user4}
    assert gateway.fetch(user4) == {user3}


def test_link_across_3_users():
    gateway = StubUserLinkStore()
    user1 = "user1"
    user2 = "user2"
    user3 = "user3"
    gateway.link(user1, user2)
    gateway.link(user2, user3)

    assert gateway.fetch(user1) == {user2, user3}
    assert gateway.fetch(user2) == {user1, user3}
    assert gateway.fetch(user3) == {user1, user2}


def test_link_across_3_users_in_reverse():
    gateway = StubUserLinkStore()
    user1 = "user1"
    user2 = "user2"
    user3 = "user3"
    gateway.link(user2, user1)
    gateway.link(user3, user1)

    assert gateway.fetch(user1) == {user2, user3}
    assert gateway.fetch(user2) == {user1, user3}
    assert gateway.fetch(user3) == {user2, user1}


def test_links_across_different_source_users():
    gateway = StubUserLinkStore()
    user1 = "user1"
    user2 = "user2"
    user3 = "user3"
    user4 = "user4"
    gateway.link(user1, user2)
    gateway.link(user2, user3)
    gateway.link(user3, user4)

    assert gateway.fetch(user1) == {user2, user3, user4}
    assert gateway.fetch(user2) == {user1, user3, user4}
    assert gateway.fetch(user3) == {user1, user2, user4}
    assert gateway.fetch(user4) == {user1, user2, user3}


def test_handles_duplicates_calls():
    gateway = StubUserLinkStore()
    user1 = "user1"
    user2 = "user2"
    gateway.link(user1, user2)
    gateway.link(user1, user2)

    assert gateway.fetch(user1) == {user2}
    assert gateway.fetch(user2) == {user1}


def test_links_with_user_object():
    gateway = StubUserLinkStore()
    user1 = SlackUser("user1", "team1")
    user2 = SlackUser("user2", "team2")
    user3 = SlackUser("user3", "team3")
    user4 = SlackUser("user4", "team4")
    gateway.link(user1, user2)
    gateway.link(user2, user3)
    gateway.link(user3, user4)

    assert gateway.fetch(user1) == {user2, user3, user4}
    assert gateway.fetch(user2) == {user1, user3, user4}
    assert gateway.fetch(user3) == {user1, user2, user4}
    assert gateway.fetch(user4) == {user1, user2, user3}
