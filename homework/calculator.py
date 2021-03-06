"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

    * Addition
    * Subtractions
    * Multiplication
    * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
    http://localhost:8080/multiply/3/5   => 15
    http://localhost:8080/add/23/42      => 65
    http://localhost:8080/subtract/23/42 => -19
    http://localhost:8080/divide/22/11   => 2
    http://localhost:8080/divide/6/0     => HTTP "400 Bad Request"
    http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

    * Fork this repository (Session03).
    * Edit this file to meet the homework requirements.
    * Your script should be runnable using `$ python calculator.py`
    * When the script is running, I should be able to view your
        application in my browser.
    * I should also be able to see a home page (http://localhost:8080/)
        that explains how to perform calculations.
    * Commit and push your changes to your fork.
    * Submit a link to your Session03 fork repository!


"""
import re

def add(*args):
    """ Returns a STRING with the sum of the arguments """
    # DONE: Fill sum with the correct value, based on the
    # args provided.
    args = [int(i) for i in args]
    addition = args[0]
    for i in args[1:]:
        addition += i
    return str(addition)

# DONE: Add functions for handling more arithmetic operations.

def subtract(*args):
    """ Returns a STRING with the difference of the arguments """
    args = [int(i) for i in args]
    diff = args[0]
    for i in args[1:]:
        diff -= i
    return str(diff)

def multiply(*args):
    """ Returns a STRING with the product of the arguments """
    args = [int(i) for i in args]
    prod = args[0]
    for i in args[1:]:
        prod *= i
    return str(prod)

def divide(*args):
    """ Returns a STRING with the quotient of the arguments """
    args = [int(i) for i in args]
    quot = args[0]
    for i in args[1:]:
        quot /= i
    return str(quot)

def home(*args):
    """ Returns a home page that explains how to perform calculations """
    home_page = """<html>
                <h1>Calculator Program</h1>
                <body>To use this calculator, open a browser to this</ br>
                wsgi application and type the desired the type of</ br>
                calculation you require, followed by the numbers to be</ br>
                calculated.</ br>
                For example: `http://localhost:8080/multiple/3/5'.</ br>
                The response will appear in the body of your browser.</ br>
                For the above example,'15'. Your choices for types of</ br>
                calculations are:</ br>
                add</ br>
                subtract</ br>
                multiply</ br>
                divide</ br>
                </body>
                </html>
                """
    return home_page

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """
    # DONE: Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path.
    args = path.strip("/").split("/")
    func_name = args.pop(0)
    if not func_name:
        func = home
    else:
        func = {
        "add": add,
        "subtract": subtract,
        "multiply": multiply,
        "divide": divide
        }.get(func_name.lower())
    return func, args

def application(environ, start_response):
    # DONE: Your application code from the book database
    # work here as well! Remember that your application must
    # invoke start_response(status, headers) and also return
    # the body of the response in BYTE encoding.
    #
    # TODO (bonus): Add error handling for a user attempting
    # to divide by zero.
    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1> Internal Server Error</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

if __name__ == '__main__':
    # DONE: Insert the same boilerplate wsgiref simple
    # server creation that you used in the book database.
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
