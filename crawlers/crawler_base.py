class Crawler:
    def __init__(self, chat_id=None, *args, **kwargs):
        """
        Crawler generic interface
        :param chat_id: optional parameter to specify where the crawler should be writing the results
        """
        self.chat_id = chat_id

    def get_last_updates(self):
        """
        Generic method to get the last update of any crawler
        :return: [dict{text='text', image='image'}]
        """
        pass
