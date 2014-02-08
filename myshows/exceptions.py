class MyShowsException(Exception):
    pass

class MyShowsLoginRequired(MyShowsException):
    pass

class MyShowsLoginException(Exception):
    pass
class MyShowsLoginEmptyException(MyShowsLoginException):
    pass
class MyShowsLoginIncorrectException(MyShowsLoginException):
    pass
