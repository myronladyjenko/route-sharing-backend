import sys;
import json;
from http.server import HTTPServer, BaseHTTPRequestHandler;

let climbConfigs = {
  "crimp": [
    1,
    2,
    3,
    4,
    5
  ]
}
class MyHandler( BaseHTTPRequestHandler ):
    def do_GET(self):
      if(self.path == "/climbConfigs"):
        self.send_response( 200 );
        self.send_header( "Content-type", "application/json" );
        self.end_headers();
        self.wfile.write( bytes( json.dumps(climbConfigs), "utf-8" ) );
      elif self.path == "/hello.html":
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len(home_page) );
            self.end_headers();

            self.wfile.write( bytes( home_page, "utf-8" ) );

        else:
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: not found", "utf-8" ) );


httpd = HTTPServer( ( '0.0.0.0', int(sys.argv[1]) ), MyHandler );
httpd.serve_forever();
