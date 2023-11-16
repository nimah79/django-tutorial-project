from django.test import TestCase

from spotify.models import Person


# F.I.R.S.T
class PersonTest(TestCase):
    fixtures = ["person.json"]

    def test_is_older_than(self):
        ali = Person.objects.get(first_name="Ali")
        self.assertTrue(ali.is_older_than(22))
        self.assertFalse(ali.is_older_than(24))
        self.assertFalse(ali.is_older_than(25))
        self.assertTrue(ali.is_older_than(23))

    def test_str(self):
        first_names = [
            "Ali",
            "Taghi",
        ]
        for first_name in first_names:
            self._test_str_by_first_name(first_name)

    def _test_str_by_first_name(self, first_name):
        person = Person.objects.get(first_name=first_name)
        self.assertEqual(person.__str__(), first_name)
