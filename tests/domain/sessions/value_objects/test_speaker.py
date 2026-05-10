import pytest

from src.domain.sessions.value_objects.speaker import Speaker


class TestSpeaker:

    def test_creates_speaker_with_name_and_bio(self):
        speaker = Speaker(name="Ana García", bio="Senior Python developer")
        assert speaker.name == "Ana García"
        assert speaker.bio == "Senior Python developer"

    def test_is_immutable(self):
        speaker = Speaker(name="Ana García", bio="Senior developer")
        with pytest.raises(Exception):
            speaker.name = "Other Name"

    def test_equality_with_same_values(self):
        s1 = Speaker(name="Ana García", bio="Senior developer")
        s2 = Speaker(name="Ana García", bio="Senior developer")
        assert s1 == s2

    def test_inequality_with_different_name(self):
        s1 = Speaker(name="Ana García", bio="Senior developer")
        s2 = Speaker(name="Luis Torres", bio="Senior developer")
        assert s1 != s2

    def test_inequality_with_different_bio(self):
        s1 = Speaker(name="Ana García", bio="Senior developer")
        s2 = Speaker(name="Ana García", bio="Junior developer")
        assert s1 != s2

    def test_accepts_empty_bio(self):
        speaker = Speaker(name="Ana García", bio="")
        assert speaker.bio == ""
