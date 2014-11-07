from django.test import TestCase
from django.core.urlresolvers import reverse
# Create your tests here.


class LessonViewTests(TestCase):
	def test_questions_show_in_order(self):
		lesson = 
		response = self.client.get(reverse('support:lesson'))

