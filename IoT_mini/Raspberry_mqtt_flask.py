import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import time

def on_connect(client, userdata, flags, rc): # 클라이언트 연결 시
    print("Connected!")

    client.subscribe("# TOPIC 1 #")
    client.subscribe("# TOPIC 2 #")

def on_message(client, userdata, msg): # 메세지 받으면

    msg_decoded = msg.payload.decode("utf-8")
    print(msg.topic + " : " + msg_decoded)


ADDRESS="# YOUR RASPBERRY IP ADDRESS #"
PORT = 1883 # mosquitto 기본 포트

client = mqtt.Client()
client.connect(ADDRESS, PORT, 220)
client.on_connect = on_connect # 콜백함수 설정
client.on_message = on_message

client.loop_start()  # 플라스크와 같이 돌릴 경우 loop_forever() 말고 이것을 사용


app = Flask(__name__)  # 플라스크 코드는 mqtt 코드 아래에 넣어야 함

@app.route("/")
def mainPage():
    return render_template("# HTML MAIN PAGE #")

@app.route("/Farm/View", methods=["post"])
def viewPage():
    return render_template("# HTML VIEW PAGE #", val0="# DATA 0 #", val1="# DATA 1 #")
    # Jinja 템플릿 문법으로 변수 전달
    # HTML 안에서 {{val0}} 이라고 쓰면 val0으로 전달한 변수 호출 가능




if __name__ == "__main__":
    app.run(host="localhost", debug=True, port=80) # 서버 열 경우에는 host="0.0.0.0"








