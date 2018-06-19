from .base import BaseTestCase


class EventsTestCase(BaseTestCase):

    event_data = {
        'title': 'The Magical Event',
        'description': 'Coldplay brings Magic to your doorsteps',
        'poster': 'http://link-to-image-resource.com',
        'artistes': ['Coldplay'],
        'date': '2018-11-12',
        'location': 'The Park',
        'ticket_purchase': 'https://purchase-tickets.com'
    }

    def test_create_event_for_not_authenticated_user(self):
        response = self.client.post('/api/v1/events/', self.event_data)
        self.assertEqual(response.status_code, 403)

    def test_create_event_for_authenticated_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.request_token)
        response = self.client.post('/api/v1/events/', self.event_data)
        self.client.credentials()
        self.assertEqual(response.status_code, 201)

    def test_create_duplicate_event_does_not_create(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.request_token)
        response = self.client.post('/api/v1/events/', self.event_data)
        response = self.client.post('/api/v1/events/', self.event_data)
        self.assertEqual(response.status_code, 400)
