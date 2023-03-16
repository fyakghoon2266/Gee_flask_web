from app import app


if __name__ == '__main__':
  app.debug = True
  app.run(threaded=True, port=5000)