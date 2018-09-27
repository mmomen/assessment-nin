import time
import BaseHTTPServer
# import urlparse

# base code source: https://wiki.python.org/moin/BaseHttpServer

HOST_NAME = 'localhost'
PORT_NUMBER = 9090


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write("<html><head><title>Title goes here.</title></head>")
        s.wfile.write("<body><p>This is a test.</p>")
        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then s.path equals "/foo/bar/".
        s.wfile.write("<p>You accessed path: %s</p>" % s.path)
        s.wfile.write("</body></html>")

    def do_PUT(s):
        """Respond to a PUT request."""
        s.send_response(200)
        s.send_header("Content-type", "application/json")
        s.end_headers()
        # On Success, return the integer count of how many times that word has been PUT to the api in a JSON hash
        path = s.path
        content_len = int(s.headers.getheader('content-length', 0))
        body = s.rfile.read(content_len)
        path_split = path.split('/')
        path_first = path_split[1]
        path_second = path_split[2]
        print path, content_len, body, path_split, len(path_split)

        if content_len == 0:  # check for nothing in request body
            if len(path_split) == 3:  # what we're looking for
                print 'yes'
            elif (len(path_split) == 4 and path_split[-1] == ''):  # in case there is a trailing slash
                print 'yes but why'
            else:  # all other cases do nothing
                print 'no'
        #else ignore

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
