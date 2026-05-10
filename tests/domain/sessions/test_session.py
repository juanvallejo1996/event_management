from src.domain.sessions.session_status import SessionStatus


class TestSessionStatus:

    def test_all_statuses_are_defined(self):
        statuses = {s.value for s in SessionStatus}
        assert statuses == {"scheduled", "in_progress", "cancelled", "finished"}

    def test_status_is_string_comparable(self):
        assert SessionStatus.SCHEDULED == "scheduled"


class TestSessionEntity:

    def test_creates_session_with_correct_attributes(self, sample_session, sample_speaker):
        assert sample_session.title == "Async Python"
        assert sample_session.capacity == 30
        assert sample_session.speaker == sample_speaker
        assert sample_session.status == SessionStatus.SCHEDULED

    def test_session_speaker_is_value_object(self, sample_session):
        assert sample_session.speaker.name == "Ana García"
        assert sample_session.speaker.bio == "Senior Python developer"

    def test_session_links_to_event(self, sample_session, event_id):
        assert sample_session.event_id == event_id
