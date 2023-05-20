import sys;
from http.server import HTTPServer, BaseHTTPRequestHandler;

class MyHandler( BaseHTTPRequestHandler ):
    def do_GET(self):
        if self.path == "/hello.html":
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len(home_page) );
            self.end_headers();

            self.wfile.write( bytes( home_page, "utf-8" ) );

        else:
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: not found", "utf-8" ) );




home_page = """
<html>
  <head>
    <title> Hello, world! </title>
  </head>
  <body>
    <h1> Hello, world!\n </h1>
    <p> Welcome to the world of "hello"! </p>
  </body>
</html>
""";

httpd = HTTPServer( ( '0.0.0.0', int(sys.argv[1]) ), MyHandler );
httpd.serve_forever();
