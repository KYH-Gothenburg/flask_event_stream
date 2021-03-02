from threading import Thread

from flask import Flask, render_template, Response, request
from queue import Queue

from mqtt_pub_sub import MQTT

app = Flask(__name__)
app.debug = True
queue = Queue()

def event_stream():
    while True:
        message = queue.get()

        yield f'data: {message["device_name"]}: {message["device_data"]}\n\n'
        queue.task_done()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stream')
def stream():
    return Response(event_stream(), mimetype='text/event-stream')


@app.route('/api/post')
def post():
    message = request.args.get('sentence')
    queue.put(message)
    return "Sent"

if __name__ == '__main__':
    mqtt = MQTT(queue, listener=True, topic='device/+/data').bootstrap_mqtt()
    mqtt_thread = Thread(target=mqtt.start)
    mqtt_thread.start()
    app.run(threaded=True)
