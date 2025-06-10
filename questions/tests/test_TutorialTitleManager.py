from unittest.mock import patch
from django.test import TestCase
from questions.models import TutorialTitle


class TutorialTitleManagerTest(TestCase):
    """
    Tests for the TutorialTitleManager custom manager.
    """

    @classmethod
    def setUpTestData(cls):
        """Set up data for the entire test class."""
        # A title with a specific name
        cls.title1 = TutorialTitle.objects.create(
            title_id_slug="django-deployment", name="Deploying Django Apps"
        )
        # A title without a specific name, relies on slug generation
        cls.title2 = TutorialTitle.objects.create(title_id_slug="aws-basics")
        cls.title3 = TutorialTitle.objects.create(
            title_id_slug="docker-for-devs", name="Docker for Developers"
        )

    def test_get_initial_titles_returns_slugs(self):
        """Test that get_initial_titles returns a list of slugs."""
        titles = TutorialTitle.objects.get_initial_titles(amount=2)
        self.assertEqual(len(titles), 2)
        self.assertIsInstance(titles, list)
        # Ensure it returns slugs, not names
        self.assertIn("-", titles[0])

    @patch("random.shuffle")
    def test_get_initial_titles_shuffles_results(self, mock_shuffle):
        """Test that get_initial_titles calls random.shuffle."""
        TutorialTitle.objects.get_initial_titles()
        mock_shuffle.assert_called_once()

    def test_get_initial_titles_handles_no_titles(self):
        """Test it returns an empty list when no titles exist."""
        TutorialTitle.objects.all().delete()
        self.assertEqual(TutorialTitle.objects.get_initial_titles(), [])

    def test_search_titles_by_name(self):
        """Test searching by the 'name' field."""
        results = TutorialTitle.objects.search_titles("Deploy")
        self.assertEqual(results, ["Deploying Django Apps"])

    def test_search_titles_by_slug(self):
        """Test searching by the 'title_id_slug' field."""
        results = TutorialTitle.objects.search_titles("aws")
        # Should return the generated readable name
        self.assertEqual(results, ["Aws Basics"])

    def test_search_titles_returns_name_when_available(self):
        """Test that the explicit name is prioritized over the generated one."""
        results = TutorialTitle.objects.search_titles("docker")
        self.assertEqual(results, ["Docker for Developers"])

    def test_search_titles_with_empty_query(self):
        """Test that an empty query falls back to get_initial_titles."""
        with patch(
            "questions.models.TutorialTitleManager.get_initial_titles"
        ) as mock_get_initial:
            mock_get_initial.return_value = ["test-slug-one", "test-slug-two"]
            results = TutorialTitle.objects.search_titles(query="", limit=5)
            # Check that the manager method was called with the correct limit
            mock_get_initial.assert_called_once_with(5)
            # Check that the slugs were converted to readable names
            self.assertEqual(results, ["Test Slug One", "Test Slug Two"])
