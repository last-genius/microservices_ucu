from flask import Flask, request

app = Flask(__name__)
host_name = "localhost"
host_port = 9001


@app.get("/")
def do_GET():
    return "not implemented yet"


if __name__ == '__main__':
    print('message server is running...')
    app.run(host_name, host_port)
