import sys;
import json;
from http.server import HTTPServer, BaseHTTPRequestHandler;
from web3 import Web3
import urllib
import climbs_mysql

climbConfigs = {
  "crimp": [
    1,
    2,
    3,
    4,
    5
  ]
}
db = climbs_mysql.Database()

class MyHandler( BaseHTTPRequestHandler ):
    def do_GET(self):
      if(self.path == "/climbConfigs"):
        self.send_response( 200 );
        self.send_header( "Content-type", "application/json" );
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers();
        self.wfile.write( bytes( json.dumps(climbConfigs), "utf-8" ) );
      elif self.path == "/hello.html":
        self.send_response( 200 ); # OK
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header( "Content-type", "text/html" );
        self.send_header( "Content-length", len(home_page) );
        self.end_headers();

        self.wfile.write( bytes( home_page, "utf-8" ) );

      else:
        self.send_response( 404 );
        self.end_headers();
        self.wfile.write( bytes( "404: not found", "utf-8" ) );
    
    def do_POST(self):
      if self.path == '/create-climb':
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length);
        data = urllib.parse.parse_qs( data.decode( 'utf-8' ) );

        db.createClimb(data)

        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
      
      elif self.path == '/buy-climb':
        request_body = self.rfile.read(content_length)
        purchaseRequest = json.loads(request_body.decode('utf-8'))

        climb_data = purchaseRequest.get('climbData');
        signed_transaction = purchaseRequest.get('signedTransaction')

        if not signed_transaction:
          self.send_response(400)
          self.send_header('Access-Control-Allow-Origin', '*')
          self.send_header('Content-Type', 'application/json')
          self.end_headers()
          response = {'error': 'Invalid purchase request'}
          self.wfile.write(json.dumps(response).encode('utf-8'))
          return

        transaction_hash = Web3.eth.sendRawTransaction(signed_transaction.rawTransaction).hex()

        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        response = {'message': 'Purchase successful', 'transactionHash': transaction_hash}
        self.wfile.write(json.dumps(response).encode('utf-8'))

if __name__ == '__main__':
  httpd = HTTPServer(('0.0.0.0', int(sys.argv[1])), MyHandler);
  httpd.serve_forever();
