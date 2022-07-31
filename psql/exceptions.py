
class DBFailedConnectionException(Exception):

    def __init__(self):
        super().__init__('Connection to DB failed :(')


class DBMaxRetriesExceededException(Exception):

    def __init__(self,msg):
        super().__init__(f'Max connection retries exceeded while {msg}.')

