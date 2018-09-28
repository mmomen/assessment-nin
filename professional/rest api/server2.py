import time
import BaseHTTPServer
import json
import string

# base code source: https://wiki.python.org/moin/BaseHttpServer

HOST_NAME = 'localhost'
PORT_NUMBER = 9090

wordnames = {}


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def page_headers(self, code, content_type):
        self.send_response(code)
        self.send_header("Content-type", content_type)
        self.end_headers()

    def do_HEAD(s):
        s.page_headers(200, "text/html")

    def do_GET(s):
        """Respond to a GET request."""
        s.page_headers(200, "text/html")
        s.wfile.write("<html><head><title>Title goes here.</title></head>")
        s.wfile.write("<body><p>This is a test.</p>")
        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then s.path equals "/foo/bar/".
        s.wfile.write("<p>You accessed path: %s</p>" % s.path)
        s.wfile.write("</body></html>")

    def do_PUT(s):
        """Respond to a PUT request."""
        # On Success, return the integer count of how many times that word has been PUT to the api in a JSON hash
        invalidChars = set(string.punctuation)
        path = s.path
        content_len = int(s.headers.getheader('content-length', 0))
        body = s.rfile.read(content_len)
        path_split = path.split('/')
        path_levels = len(path_split)-1  # first item is always empty (starting slash)

        def return_request(code, content_type, message):
            s.page_headers(code, content_type)
            if content_type == "application/json":
                message_to_write = json.dumps(message)
            else:  # TK is this needed?
                print 'is this needed?'
            s.wfile.write(message_to_write)

        def return_single(wordname, word_log):
            if wordname in word_log:
                word_log[wordname] += 1
            else:
                word_log[wordname] = 1
            return_request(200, "application/json", {"words": {wordname: word_log[wordname]}})

        def return_error(error_type, code):
            if error_type == "special character":
                error_message = "PUT requests may not contain special characters."
            elif error_type == "not one word":
                error_message = "PUT requests must be one word (e.g. /word/christopherwalken)."
            elif error_type == "first level not word":
                error_message = "PUT requests must use 'word' as first level in path (e.g. /word/[WORDNAME])."
            elif error_type == "bad path":
                error_message = "PUT requests must have paths in the following structure: /word/[WORDNAME])"
            elif error_type == "request has body":
                error_message = "PUT requests cannot contain a request body."
            else:
                error_message = "An unexpected error has occured."
            return_request(code, "application/json", {"error": error_message})

        if content_len == 0:  # check for nothing in request body
            # 2 levels and last is not an empty string (trailing slash with no WORDNAME) or
            # 3 levels and last is an empty string (trailling slash)
            if (path_levels == 2 and path_split[-1] != '') or (path_levels == 3 and path_split[-1] == ''):
                path_first_level = path_split[1].lower()
                path_second_level = path_split[2].lower()
                if path_first_level == "word":
                    if len(path_second_level.split('%20')) == 1:
                        if any(char in invalidChars for char in path_second_level):  # if no special characters
                            return_error("special character", 400)
                        else:
                            return_single(path_second_level, wordnames)
                    else:
                        return_error("not one word", 400)
                else:
                    return_error("first level not word", 400)
            else:
                return_error("bad path", 400)
        else:
            return_error("request has body", 400)


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
