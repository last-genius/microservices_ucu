from flask import Flask, request

app = Flask(__name__)

host_name = "localhost"
host_port = 9001
messages = dict()


@app.get("/")
def do_GET():
    return str(list(messages.values()))


@app.post("/")
def do_POST():
    key = request.form["uuid"]
    msg = request.form["msg"]
    print(msg)
    messages[key] = msg

    return ""


if __name__ == '__main__':
    print('logging server is running...')
    app.run(host_name, host_port)
