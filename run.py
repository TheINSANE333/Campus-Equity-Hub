import os
from app.builder import FlaskAppBuilder

if __name__ == '__main__':
    builder = FlaskAppBuilder()
    flask_app = (builder
           .configure_app()
           .init_extensions()
           .create_database()
           .register_endpoints()
           .seed_database()
           .register_context_processors()
           .build())

    flask_app.run(debug=True, host='0.0.0.0', port=5000)
