import time
import BaseHTTPServer
import json

# base code source: https://wiki.python.org/moin/BaseHttpServer

HOST_NAME = 'localhost'
PORT_NUMBER = 9090

wordnames = {}


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def page_headers(self, code, content_type="text/html"):
        self.send_response(code)
        self.send_header("Content-type", content_type)
        self.end_headers()

    def do_HEAD(s):
        s.page_headers(200)

    def do_GET(s):
        """Respond to a GET request."""
        s.page_headers(200)
        s.wfile.write("<html><head><title>Title goes here.</title></head>")
        s.wfile.write("<body><p>This is a test.</p>")
        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then s.path equals "/foo/bar/".
        s.wfile.write("<p>You accessed path: %s</p>" % s.path)
        s.wfile.write("</body></html>")

    def do_PUT(s):
        """Respond to a PUT request."""
        # On Success, return the integer count of how many times that word has been PUT to the api in a JSON hash
        path = s.path
        content_len = int(s.headers.getheader('content-length', 0))
        body = s.rfile.read(content_len)
        path_split = path.split('/')
        path_levels = len(path_split)-1  # first item is always empty (starting slash)

        if content_len == 0:  # check for nothing in request body
            # 2 levels and last is not an empty string (trailing slash with no WORDNAME) or
            # 3 levels and last is an empty string (trailling slash)
            if (path_levels == 2 and path_split[-1] != '') or (path_levels == 3 and path_split[-1] == ''):
                path_first_level = path_split[1].lower()
                path_second_level = path_split[2].lower()
                if path_first_level == 'word':
                    if len(path_second_level.split('%20')) == 1:
                        if path_second_level in wordnames:
                            wordnames[path_second_level] += 1
                            print wordnames
                        else:
                            wordnames[path_second_level] = 1
                            print wordnames
                    else:  # not one word, return json hash and http error code
                        print 'wordname is not 1 word'
                        json_string = json.dumps({"error": "PUT requests must be one word in length"})
                        s.page_headers(400, "application/json")
                        s.wfile.write(json_string)
                else:  # first level is not 'word'
                    print 'first level must be \'word\''
            else:  # path is not expected
                print 'path is not correct'
        else:  # request has a body
            print 'must have no request body'  # else ignore

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
