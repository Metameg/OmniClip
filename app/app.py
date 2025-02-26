# import json
import os
import app.tools.utilities
from app import create_app

# os.environ['FLASK_APP'] = 'app'
app = create_app()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
    