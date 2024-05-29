from django.test import TestCase
from .models import Students
from django.utils import timezone

class StudentModelTest(TestCase):
    
    def setUp(self):
        self.student = Students.objects.create(
            first_name='Student1',
            middle_name='Student1',
            last_name='Student1',
            username='Student1',
            email='student1@gmail.com',
            password='odoo',
        )

    def test_student_creation(self):
        """Test if a student object is created correctly"""
        self.assertEqual(self.student.first_name, "Student1")
        self.assertEqual(self.student.last_name, "Student1")
        self.assertEqual(self.student.middle_name, "Student1e")

