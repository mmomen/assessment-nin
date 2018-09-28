import time
import BaseHTTPServer
import json
import string

# base code source: https://wiki.python.org/moin/BaseHttpServer

HOST_NAME = 'localhost'
PORT_NUMBER = 9090

wordnames = {}
invalidChars = set(string.punctuation)
for i in range(0, 10):
    invalidChars.add(str(i))


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def send_to_client(s, code, content_type, message):
        s.send_response(code)
        s.send_header("Content-type", content_type)
        s.end_headers()
        if message:
            if content_type == "application/json":
                message_to_write = json.dumps(message)
            else:
                message_to_write == message
            s.wfile.write(message_to_write)

    def return_success(s, request_type, wordname, word_log):
        if request_type == "PUT":
            if wordname in word_log:
                word_log[wordname] += 1
            else:
                word_log[wordname] = 1
        elif request_type == "GET":
            if wordname is None:
                s.send_to_client(200, "application/json", {"words": word_log})
                return
            if wordname not in word_log:
                s.send_to_client(200, "application/json", {"words": {wordname: 0}})
                return 0
        s.send_to_client(200, "application/json", {"words": {wordname: word_log[wordname]}})

    def return_error(s, error_type, code):
        if error_type == "non alpha character":
            error_message = "PUT requests may only be alphabetical, cannot contain numeric or special characters."
        elif error_type == "not one word":
            error_message = "PUT requests must be one word (e.g. /word/christopherwalken)."
        elif error_type == "first level not word":
            error_message = "PUT requests must use 'word' as first level in path (e.g. /word/[WORDNAME])."
        elif error_type == "bad path":
            error_message = "PUT requests must have paths in the following structure: /word/[WORDNAME])"
        elif error_type == "request has body":
            error_message = "PUT requests cannot contain a request body."
        elif error_type == "unsupported GET":
            error_message = "This is an unsupported GET request. Please visit /words or /word/[WORDNAME]."
        elif error_type == "unsupported PUT":
            error_message = "This is an unsupported PUT request. Make a PUT request to /word/[WORDNAME]."
        else:
            error_message = "An unexpected error has occured."
        s.send_to_client(code, "application/json", {"error": error_message})

    def do_HEAD(s):
        s.send_to_client(200, "text/html", False)

    def do_GET(s):
        """Respond to a GET request."""
        path = s.path
        path_split = path.split('/')
        path_levels = len(path_split)-1  # first item is always empty (starting slash)

        # check for proper level, with or without trailing slash
        if (path_levels == 1 and path_split[-1] != '') or (path_levels == 2 and path_split[-1] == ''):
            path_first_level = path_split[1].lower()
            if path_first_level == "words":
                s.return_success("GET", None, wordnames)
                return
        elif (path_levels == 2 and path_split[-1] != '') or (path_levels == 3 and path_split[-1] == ''):
            path_first_level = path_split[1].lower()
            path_second_level = path_split[2].lower()
            if path_first_level == "word":
                s.return_success("GET", path_second_level, wordnames)
                return

        s.return_error("unsupported GET", 412)  # last resort

    def do_PUT(s):
        """Respond to a PUT request."""
        path = s.path
        content_len = int(s.headers.getheader('content-length', 0))
        # body = s.rfile.read(content_len)
        path_split = path.split('/')
        path_levels = len(path_split)-1  # first item is always empty (starting slash)

        if content_len == 0:  # check for nothing in request body
            if (path_levels == 2 and path_split[-1] != '') or (path_levels == 3 and path_split[-1] == ''):
                path_first_level = path_split[1].lower()
                path_second_level = path_split[2].lower()
                if path_first_level == "word":
                    if len(path_second_level.split('%20')) == 1:
                        if any(char in invalidChars for char in path_second_level):
                            s.return_error("non alpha character", 412)
                            return
                        else:
                            s.return_success("PUT", path_second_level, wordnames)
                            return
                    else:
                        s.return_error("not one word", 412)
                        return
                else:
                    s.return_error("first level not word", 412)
                    return
            else:
                s.return_error("bad path", 412)
                return
        else:
            s.return_error("request has body", 412)
            return

        s.return_error("unsupported PUT", 412)  # last resort


if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
