from crawlers.tests import init_tests, teardown_tests
from crawlers.enalquiler_crawler import EnalquilerCrawler


class TestEnalquiler:
    @classmethod
    def setup_class(cls):
        """ setup any state specific to the execution of the given class (which
        usually contains tests).
        """
        init_tests()

    @classmethod
    def teardown_class(cls):
        """ teardown any state that was previously setup with a call to
        setup_class.
        """
        teardown_tests()

    def test_fetching_enalquiler_info(self):
        # Checking for marbella which has with this filter more than 1800 posts
        target_url = 'http://www.enalquiler.com/search?provincia=31&poblacion=28247'
        crawler = EnalquilerCrawler(target_url)
        posts = crawler.get_last_posts()
        assert len(posts) > 0
        first_full_post = None
        for p in posts:
            if p.image and p.href and p.description and p.price:
                first_full_post = p
                break
        assert first_full_post is not None
