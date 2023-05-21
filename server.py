import sys;
import json;
from http.server import HTTPServer, BaseHTTPRequestHandler;
from web3 import Web3
import urllib
import climbs_mysql

db = climbs_mysql.Database()
db.createTables()


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
      elif self.path == "preview-climbs":
        dataRows = db.loadClimbPreviews()
        
        data = []
        for row in dataRows:
          result = {}
          result['name'] = row[0]
          result['width'] = row[1]
          result['height'] = row[2]
          result['angle'] = row[3]
          result['difficulty'] = row[4]
          result['author'] = row[5]
          result['region'] = row[6]
          result['hold_theme'] = row[7]
          result['climd_id'] = row[8]
            
          data.append(result)

        content = json.dumps(data)

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))
      else:
        self.send_response( 404 );
        self.end_headers();
        self.wfile.write( bytes( "404: not found", "utf-8" ) );
    
    def do_POST(self):
      if self.path == '/create-climb':
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length);
        print(content_length)
        print(data)
        data = urllib.parse.parse_qs( data.decode( 'utf-8' ) );

        print("PRINTING IN SERVER")
        print(data)

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
    def do_OPTION():
      self.send_response(200)
      self.send_header('Access-Control-Allow-Origin', '*')
      self.end_headers()

if __name__ == '__main__':
  httpd = HTTPServer(('0.0.0.0', int(sys.argv[1])), MyHandler);
  httpd.serve_forever();
