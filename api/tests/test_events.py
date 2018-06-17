from .base import BaseTestCase


class EventsTestCase(BaseTestCase):

    event_data = {
        'title': 'The Magical Event',
        'artiste': ['Coldplay'],
        'date': '11/12/2018',
        'location': 'The Park',
        'ticket-purchase': 'https://purchase-tickets.com'
    }

    def test_create_event_for_not_authenticated_user(self):
        response = self.client.post('/api/v1/events/', self.event_data)
        self.assertEqual(response.status_code, 401)

    def test_create_event_for_authenticated_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.request_token)
        response = self.client.post('/api/v1/events/', self.event_data)
        self.client.credentials()
        self.assertEqual(response.status_code, 200)

    def test_create_duplicate_event_does_not_create(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.request_token)
        response = self.client.post('/api/v1/events/', self.event_data)
        self.assertEqual(response.status_code, 409)
