class MyShowsException(Exception):
    pass

class MyShowsLoginRequiredException(MyShowsException):
    pass
class MyShowsNotFoundException(MyShowsException):
    pass
class MyShowsInvalidParameter(MyShowsException):
    pass
class MyShowsLoginException(Exception):
    pass
class MyShowsLoginEmptyException(MyShowsLoginException):
    pass
class MyShowsLoginIncorrectException(MyShowsLoginException):
    pass
