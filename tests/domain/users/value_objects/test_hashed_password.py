import pytest

from src.domain.users.user_exceptions import InvalidPasswordFormat
from src.domain.users.value_objects.hashed_password import HashedPassword


class TestHashedPasswordCreation:

    def test_creates_hash_from_valid_plain_password(self):
        hp = HashedPassword.from_plain("securepass123")
        assert hp.value is not None
        assert isinstance(hp.value, str)

    def test_hash_is_different_from_plain_password(self):
        hp = HashedPassword.from_plain("securepass123")
        assert hp.value != "securepass123"

    def test_two_hashes_of_same_password_are_different(self):
        hp1 = HashedPassword.from_plain("securepass123")
        hp2 = HashedPassword.from_plain("securepass123")
        assert hp1.value != hp2.value

    def test_raises_when_password_too_short(self):
        with pytest.raises(InvalidPasswordFormat):
            HashedPassword.from_plain("short")

    def test_raises_when_password_exactly_7_chars(self):
        with pytest.raises(InvalidPasswordFormat):
            HashedPassword.from_plain("1234567")

    def test_accepts_password_with_exactly_8_chars(self):
        hp = HashedPassword.from_plain("12345678")
        assert hp.value is not None

    def test_error_message_is_descriptive(self):
        with pytest.raises(InvalidPasswordFormat, match="8 characters"):
            HashedPassword.from_plain("short")


class TestHashedPasswordVerify:

    def test_verify_returns_true_for_correct_password(self):
        hp = HashedPassword.from_plain("securepass123")
        assert hp.verify("securepass123") is True

    def test_verify_returns_false_for_wrong_password(self):
        hp = HashedPassword.from_plain("securepass123")
        assert hp.verify("wrongpassword") is False

    def test_verify_returns_false_for_empty_password(self):
        hp = HashedPassword.from_plain("securepass123")
        assert hp.verify("") is False

    def test_verify_is_case_sensitive(self):
        hp = HashedPassword.from_plain("SecurePass123")
        assert hp.verify("securepass123") is False

    def test_can_construct_from_existing_hash_and_verify(self):
        original = HashedPassword.from_plain("securepass123")
        reconstructed = HashedPassword(original.value)
        assert reconstructed.verify("securepass123") is True
