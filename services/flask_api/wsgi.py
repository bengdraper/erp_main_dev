import sys
print('path', sys.path)
from src import create_app
# from src import create_app

import logging
logging.basicConfig(level=logging.WARNING)
logging.getLogger('werkzeug').setLevel(logging.WARNING)
logging.getLogger('flask.app').setLevel(logging.WARNING)

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=False)
