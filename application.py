from website import create_app

application = create_app()

if __name__ == '__main__':
    application.run(debug=True, ssl_context='adhoc')

