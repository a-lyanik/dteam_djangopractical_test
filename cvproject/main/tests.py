from django.test import TestCase, Client
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .models import CVInstance, RequestLog

TEST_FIXTURES = [
    {
        "firstname": "John",
        "lastname": "Doe",
        "bio": "Software Developer",
        "skills": ["Python", "Django"],
        "projects": ["Project 1", "Project 2"],
        "contacts": {
            "email": "john.doe@example.com", "phone": "123-456-7890"}
    },
    {
        "firstname": "Jane",
        "lastname": "Smith",
        "bio": "Web Developer",
        "skills": ["JavaScript", "React"],
        "projects": ["Project A", "Project B"],
        "contacts": {
            "email": "jane.smith@example.com", "phone": "987-654-3210"}
    }
]


class CVInstanceViewsTest(TestCase):
    """
    Setup test data
    """

    def setUp(self):
        """
        Create two CVInstance objects for testing
        """

        self.cv1 = CVInstance.objects.create(**TEST_FIXTURES[0])
        self.cv2 = CVInstance.objects.create(**TEST_FIXTURES[1])

    def test_cv_instance_list_view(self):
        """
        Test the CV List View
        """
        response = self.client.get(reverse('cvinstance-list'))
        self.assertEqual(response.status_code, 200)
        # Check if correct template is used
        self.assertTemplateUsed(
            response, 'main/cvinstance_list.html')
        # Check if the heading "CV List" is in the response
        self.assertContains(response, "CV List")
        # Check if cv1's firstname appears in the list
        self.assertContains(response, self.cv1.firstname)
        # Check if cv2's firstname appears in the list
        self.assertContains(response, self.cv2.firstname)

    def test_cv_instance_detail_view(self):
        """
        Test the CV Detail View for a specific CV
        """

        for cv_data in [self.cv1, self.cv2]:
            response = self.client.get(
                reverse(
                    'cvinstance-detail', kwargs={'pk': cv_data.pk}))
            self.assertEqual(response.status_code, 200)
            # Check if correct template is used
            self.assertTemplateUsed(
                response, 'main/cvinstance_detail.html')
            # Check if cv1's firstname is in the response
            self.assertContains(response, cv_data.firstname)
            # Check if cv1's lastname is in the response
            self.assertContains(response, cv_data.lastname)
            # Check if cv1's bio is in the response
            self.assertContains(response, cv_data.bio)
            # Check if cv1's first skill is in the response
            self.assertContains(response, cv_data.skills[0])


class CVInstanceAPITest(APITestCase):

    def setUp(self):
        """
        Setup test data
        """

        self.cv_instance = CVInstance.objects.create(**TEST_FIXTURES[0])
        self.cv_list_url = reverse("api-cvinstance-list")
        self.cv_detail_url = reverse(
            "api-cvinstance-detail",
            kwargs={"pk": self.cv_instance.pk}
        )

    def test_create_cv(self):
        """Test creating a new CV instance."""
        response = self.client.post(
            self.cv_list_url, TEST_FIXTURES[0], format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # One already created in setUp
        self.assertEqual(CVInstance.objects.count(), 2)

    def test_list_cvs(self):
        """Test retrieving the list of CVs."""
        response = self.client.get(self.cv_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_cv(self):
        """Test retrieving a single CV instance."""
        response = self.client.get(self.cv_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["firstname"], self.cv_instance.firstname)

    def test_update_cv(self):
        """Test updating an existing CV instance."""
        updated_data = TEST_FIXTURES[0].copy()
        updated_data["firstname"] = "Jane"
        response = self.client.put(
            self.cv_detail_url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cv_instance.refresh_from_db()
        self.assertEqual(self.cv_instance.firstname, "Jane")

    def test_partial_update_cv(self):
        """Test partially updating a CV instance."""

        # Only updating the first name
        patch_data = {"firstname": "Jane"}
        response = self.client.patch(
            self.cv_detail_url, patch_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.cv_instance.refresh_from_db()
        # Ensure only the first name was updated
        self.assertEqual(
            self.cv_instance.firstname, "Jane")
        # Last name should remain unchanged
        self.assertEqual(self.cv_instance.lastname, "Doe")

    def test_delete_cv(self):
        """Test deleting a CV instance."""
        response = self.client.delete(self.cv_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CVInstance.objects.count(), 0)

    def test_partial_update_invalid_data(self):
        """Test partially updating a CVInstance with invalid data fails."""
        # Invalid: 123 is not a string
        response = self.client.patch(self.cv_detail_url, {
            "skills": ["Python", 123],
        }, format="json")

        self.assertEqual(response.status_code, 400)


class RequestLoggingMiddlewareTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_request_is_logged(self):
        """Test if a request is logged in RequestLog."""

        # Ensure database is empty before test
        self.assertEqual(RequestLog.objects.count(), 0)

        # Make a test request (to an existing endpoint)
        response = self.client.get("/api/cvs/")

        # Check if request is logged
        self.assertEqual(response.status_code, 200)
        self.assertEqual(RequestLog.objects.count(), 1)

        # Verify the log content
        log = RequestLog.objects.first()
        self.assertEqual(log.http_method, "GET")
        self.assertEqual(log.path, "/api/cvs/")

    def test_multiple_requests_are_logged(self):
        """Test if multiple requests are logged separately."""

        self.client.get("/api/cvs/")
        self.client.post(
            "/api/cvs/",
            {"firstname": "John", "lastname": "Doe"},
            content_type="application/json",
        )

        self.assertEqual(RequestLog.objects.count(), 2)

        logs = RequestLog.objects.all()
        self.assertEqual(logs[0].http_method, "GET")
        self.assertEqual(logs[1].http_method, "POST")

    def test_invalid_request_is_logged(self):
        """Test if a 404 request is still logged."""

        self.client.get("/invalid-url/")
        self.assertEqual(RequestLog.objects.count(), 1)

        log = RequestLog.objects.first()
        self.assertEqual(log.http_method, "GET")
        self.assertEqual(log.path, "/invalid-url/")


class RequestLogViewTests(TestCase):
    def setUp(self):
        """Create some sample request logs."""
        for i in range(12):  # Create 12 logs to test the last 10 retrieval
            RequestLog.objects.create(
                http_method="GET", path=f"/test-path-{i}/")

    def test_request_log_view(self):
        """Test that the request log view returns the last 10 requests."""
        url = reverse("request-log-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "test-path")

        logs = response.context["logs"]
        # Should return only the last 10 logs
        self.assertEqual(len(logs), 10)

        # Check that the latest logs are included (reverse order)
        latest_log_path = "/test-path-11/"
        # We check the [1] because [0] will be `requests`
        self.assertEqual(logs[1].path, latest_log_path)
