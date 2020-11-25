from finance.utility.config import Config
from finance.server import app


if __name__ == "__main__":
  app.run(debug=Config.test_env)