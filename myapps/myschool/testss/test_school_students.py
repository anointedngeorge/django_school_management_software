from django.test import TestCase
from ..models import Students
from django.utils import timezone

class BookModelTest(TestCase):
    
    def setUp(self):
        self.student = Students.objects.create(
            first_name='Student1',
            middle_name='Student1',
            last_name='Student1',
            username='Student1',
            email='student1@gmail.com',
            password='odo',
        )

    def test_student_creation(self):
        """Test if a student object is created correctly"""
        self.assertEqual(self.student.first_name, "Student1")
        self.assertEqual(self.student.last_name, "Student1")
        self.assertEqual(self.student.middle_name, "Student1e")
        # self.assertRegexpMatches(self.student.email, '!')

    # def test_book_str(self):
    #     """Test the __str__ method of the Book model"""
    #     self.assertEqual(str(self.book), "Test Book")
    
    # def test_unique_isbn(self):
    #     """Test the ISBN field for uniqueness"""
    #     with self.assertRaises(Exception):
    #         Book.objects.create(
    #             title="Another Book",
    #             author="Jane Doe",
    #             published_date=timezone.now().date(),
    #             isbn="1234567890123"  # Same ISBN as self.book
    #         )

