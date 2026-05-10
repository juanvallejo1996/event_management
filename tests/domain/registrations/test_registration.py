from src.domain.registrations.registration_status import RegistrationStatus


class TestRegistrationStatus:

    def test_all_statuses_are_defined(self):
        statuses = {s.value for s in RegistrationStatus}
        assert statuses == {"confirmed", "canceled"}

    def test_status_is_string_comparable(self):
        assert RegistrationStatus.CONFIRMED == "confirmed"
        assert RegistrationStatus.CANCELED == "canceled"


class TestRegistrationEntity:

    def test_creates_registration_with_correct_attributes(
        self, sample_registration, user_id, event_id
    ):
        assert sample_registration.user_id == user_id
        assert sample_registration.event_id == event_id
        assert sample_registration.status == RegistrationStatus.CONFIRMED

    def test_registration_links_user_and_event(self, sample_registration, user_id, event_id):
        assert sample_registration.user_id == user_id
        assert sample_registration.event_id == event_id

    def test_registration_has_timestamp(self, sample_registration):
        assert sample_registration.registered_at is not None
