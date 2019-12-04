from app import app
from flask import send_from_directory

if __name__ == "__main__":
    @app.route('/fonts/<path:path>')
    def send_fonts(path):
        return send_from_directory('static/dist/fonts', path)


    @app.route('/static/<path:path>')
    def send_static(path):
        return send_from_directory('static', path)


    app.run(host='0.0.0.0', port=8080, debug=False)
