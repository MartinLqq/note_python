import falcon
from .log import logger


class StorageError(Exception):

    @staticmethod
    def handle(ex, req, resp, params):
        logger.error(ex)
        description = (
            'Sorry, couldn\'t write your thing to the database. '
            'It worked on my box.'
        )
        raise falcon.HTTPError(
            falcon.HTTP_725, 'Database Error', description
        )
