from game import app

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], port=app.config['PORT'])
