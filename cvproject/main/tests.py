from django.test import TestCase
from django.urls import reverse
from .models import CVInstance


class CVInstanceViewsTest(TestCase):
    """
    Setup test data
    """

    def setUp(self):
        """
        Create two CVInstance objects for testing
        """

        self.cv1 = CVInstance.objects.create(
            firstname="John",
            lastname="Doe",
            bio="Software Developer",
            skills=["Python", "Django"],
            projects=["Project 1", "Project 2"],
            contacts={
                "email": "john.doe@example.com", "phone": "123-456-7890"}
        )
        self.cv2 = CVInstance.objects.create(
            firstname="Jane",
            lastname="Smith",
            bio="Web Developer",
            skills=["JavaScript", "React"],
            projects=["Project A", "Project B"],
            contacts={
                "email": "jane.smith@example.com", "phone": "987-654-3210"}
        )

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
