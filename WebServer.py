#!/usr/bin/python
from http.server import BaseHTTPRequestHandler, HTTPServer
import ssl
from os import curdir, sep
from uuid import uuid4
from io import BytesIO
import sys

# https://requests.readthedocs.io/en/v0.10.2/user/advanced/
# https://blog.anvileight.com/posts/simple-python-http-server/

#
PORT_NUMBER = 8000

# Handling richieste HTTP
class HTTP_Handler(BaseHTTPRequestHandler):
	
	# Handler richieste GET
	def do_GET(self):
		if self.path=="/":
			self.path="/index.html"

		try:
			# Controlla l'estensione del file richiesto  e configura correttamente il tipo di mime
			# https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types
			# self.session_id = uuid4()
			# UUID('6f4a1f4d-1315-4e3e-a737-14f005f86b8c')

			sendReply = False

			#
			if self.path.endswith(".html"):
				mimetype='text/html'
				sendReply = True
			if self.path.endswith(".jpg"):
				mimetype='image/jpg'
				sendReply = True
			if self.path.endswith(".png"):
				mimetype='image/png'
				sendReply = True
			if self.path.endswith(".gif"):
				mimetype='image/gif'
				sendReply = True
			if self.path.endswith(".js"):
				mimetype='application/javascript'
				sendReply = True
			if self.path.endswith(".css"):
				mimetype='text/css'
				sendReply = True

			#
			if sendReply == True and mimetype != 'image/jpg' and mimetype != 'image/png':
				# Apre il file richiesto per la lettura dal diso locale in modalità lettura
				f = open(curdir + sep + self.path, mode="r", encoding="utf8")
				# 
				self.send_response(200)
				self.send_header('Content-type',mimetype)
				self.end_headers()
				#
				self.wfile.write(f.read().encode(encoding="UTF-8",errors="ignore"))
				f.close()
				#raise Exception('spam', 'eggs')
			else:
				# Apre il file richiesto per la lettura dal diso locale in modalità lettura
				# I file immagine devono essere letti in modalità binaria
				f = open(curdir + sep + self.path, mode="rb") 
				self.send_response(200)
				self.send_header('Content-type',mimetype)
				self.end_headers()
				self.wfile.write(f.read())
				f.close()
				
			return

		except IOError:
        #304: Not modified
        #200: OK
        #404: Not found
			self.send_error(404,'File Not Found: %s' % self.path)
		except Exception as inst:
			print("Unexpected error:", sys.exc_info()[0])
			print(inst.args)


	def do_POST(self):
		content_length = int(self.headers['Content-Length'])
		body = self.rfile.read(content_length)
		self.send_response(200)
		self.end_headers()
		response = BytesIO()
		response.write(b'This is POST request.')
		response.write(b'Received: ')
		response.write(body)
		self.wfile.write(response.getvalue())
        
try:
	# Create a web server and define the handler to manage the incoming request
	# Creare il server e assegnare la funzione handler per gestire le richieste in entrata
	server = HTTPServer(('', PORT_NUMBER), HTTP_Handler)
	print("Started httpserver on port: " , PORT_NUMBER)
	
	# Wait forever for incoming http requests
	server.serve_forever()
    
    # SSL
    # httpd = HTTPServer(('localhost', 4443), BaseHTTPRequestHandler)
    # httpd.socket = ssl.wrap_socket (httpd.socket, 
    #    keyfile="path/to/key.pem", 
    #    certfile='path/to/cert.pem', server_side=True)
    # httpd.serve_forever()
    
    # To generate key and cert files with OpenSSL use following command
    # openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365
    
    
    
except KeyboardInterrupt:
	print("^C received, shutting down the web server")
	server.socket.close()