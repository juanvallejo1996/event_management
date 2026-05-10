import pytest

from src.domain.users.user_exceptions import InvalidEmailFormat
from src.domain.users.value_objects.email import Email


class TestEmail:

    def test_creates_with_valid_email(self):
        email = Email("user@example.com")
        assert email.value == "user@example.com"

    def test_creates_with_subdomain_email(self):
        email = Email("user@mail.example.com")
        assert email.value == "user@mail.example.com"

    def test_raises_when_missing_at_sign(self):
        with pytest.raises(InvalidEmailFormat):
            Email("userexample.com")

    def test_raises_when_missing_domain(self):
        with pytest.raises(InvalidEmailFormat):
            Email("user@")

    def test_raises_when_missing_local_part(self):
        with pytest.raises(InvalidEmailFormat):
            Email("@example.com")

    def test_raises_when_empty_string(self):
        with pytest.raises(InvalidEmailFormat):
            Email("")

    def test_raises_when_missing_tld(self):
        with pytest.raises(InvalidEmailFormat):
            Email("user@example")

    def test_is_immutable(self):
        email = Email("user@example.com")
        with pytest.raises(Exception):
            email.value = "other@example.com"

    def test_equality_with_same_value(self):
        assert Email("user@example.com") == Email("user@example.com")

    def test_inequality_with_different_value(self):
        assert Email("a@example.com") != Email("b@example.com")
