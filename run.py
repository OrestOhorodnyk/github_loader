import github_loader
from github_loader.config import Config

app = github_loader.create_app()

if __name__ == '__main__':
    app.run(debug=Config.DEBUG_MODE, host='0.0.0.0')
