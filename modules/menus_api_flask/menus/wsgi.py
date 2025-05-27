import sys
print('path', sys.path)
from menus_app.src import create_app
# from src import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
