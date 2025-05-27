import http.server
import socketserver
import urllib.parse
import os

PORT = 8080
posts = []  # In-memory store for blog posts

class BlogHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index':
            self.show_home()
        elif self.path == '/new':
            self.show_new_post_form()
        else:
            self.send_error(404, "Page not found")

    def do_POST(self):
        if self.path == '/submit':
            length = int(self.headers.get('Content-Length'))
            post_data = self.rfile.read(length).decode('utf-8')
            fields = urllib.parse.parse_qs(post_data)
            title = fields.get('title', [''])[0]
            content = fields.get('content', [''])[0]
            if title and content:
                posts.append({'title': title, 'content': content})
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()

    def show_home(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        html = "<html><head><title>My Blog</title></head><body>"
        html += "<h1>My Blog</h1><a href='/new'>New Post</a><hr>"
        for post in reversed(posts):
            html += f"<h2>{post['title']}</h2><p>{post['content']}</p><hr>"
        html += "</body></html>"
        self.wfile.write(html.encode('utf-8'))

    def show_new_post_form(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        html = """
        <html><head><title>New Post</title></head><body>
        <h1>Create a New Post</h1>
        <form method='POST' action='/submit'>
            Title:<br><input type='text' name='title'><br><br>
            Content:<br><textarea name='content' rows='5' cols='40'></textarea><br><br>
            <input type='submit' value='Post'>
        </form>
        <a href='/'>Back to Home</a>
        </body></html>
        """
        self.wfile.write(html.encode('utf-8'))

if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), BlogHandler) as httpd:
        print(f"Serving on http://localhost:{PORT}")
        httpd.serve_forever()
