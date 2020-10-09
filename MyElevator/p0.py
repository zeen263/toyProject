import requests, time
from Elevator import Elevator, Call
maxquota = 8
height = 5
url = 'http://localhost:8000'


def start(user, problem, count):
    uri = url + '/start' + '/' + user + '/' + str(problem) + '/' + str(count)
    return requests.post(uri).json()


def oncalls(token):
    uri = url + '/oncalls'
    return requests.get(uri, headers={'X-Auth-Token': token}).json()


def action(token, cmds):
    uri = url + '/action'
    return requests.post(uri, headers={'X-Auth-Token': token}, json={'commands': cmds}).json()


def p0_simulator():
    user = 'tester'
    problem = 0
    count = 4
    isend = False

    ret = start(user, problem, count)
    token = ret['token']
    print('Token for %s is %s' % (user, token))

    elevators = [0, 0, 0, 0]
    for i in range(4):
        elevators[i] = Elevator(i, 1, [], "STOPPED")
        elevators[i].updateStatus(ret['elevators'][i])



    while not isend:
        '''
        oncall로 콜 상태 업데이트(v)
        이 층에 내릴 사람이 있다면 멈추고 > 문을 열고 > 내린다 (v)
        이 층에서 탈 사람이 있으면 멈추고 > 문을 열고 > 태운다 (v)
        탈 사람이 없고 문이 열려 있다면 문을 닫는다 (v)
        탈 사람이 없고 문이 닫혀 있다면 올라가거나 내려간다 (v)
        action 실행, 엘리베이터 상태 업데이트 ()
        isend 체크 ()
        '''
        ev_stat = ['','','','']

        ret = oncalls(token)
        calls = []
        command = [-1, -1, -1, -1]

        # 콜 업데이트
        for cl in ret['calls']:
            calls.append(Call(cl['id'], cl['timestamp'], cl['start'], cl['end']))


        # 1순위 : 내리기
        for i, ev in enumerate(elevators):
            byebye = ev.exitablePassengers() # 이 층에서 내릴 승객들의 id
            if byebye:
                if ev.status == "UPWARD" or ev.status == "DOWNWARD": # 안 멈췄으면 멈추고
                    command[i] = ev.stop()
                    ev_stat[ev.id] = 'stop to exit'

                elif ev.status == "STOPPED": # 멈췄으면 문 열고
                    command[i] = ev.open()
                    ev_stat[ev.id] = 'open to exit'

                elif ev.status == "OPENED": # 열었으면 내려주기
                    command[i] = ev.exit(byebye)
                    ev_stat[ev.id] = 'bye' + ', '.join(map(str, byebye)) + '!'


        # 2순위 : 태우기
        for i, ev in enumerate(elevators):
            quota = ev.quota
            comein = []

            for call in calls:
                if quota == maxquota: break
                if call.start == ev.floor:
                    comein.append(call.id)
                    calls.remove(call)
                    quota += 1

            if comein:
                if command[i] == -1:
                    if ev.status == "UPWARD" or ev.status == "DOWNWARD": # 올라가거나 내려가다가 태울 애가 생기면 멈추기
                        command[i] = ev.stop()
                        ev_stat[ev.id] = 'stop to enter'

                    elif ev.status == "STOPPED": # 멈춘 상태면 태우기 위해 열기
                        command[i] = ev.open()
                        ev_stat[ev.id] = 'open to enter'

                    elif ev.status == "OPENED": # 열렸으면 태우기
                        command[i] = ev.enter(comein)
                        ev_stat[ev.id] = 'come in' + ', '.join(map(str, comein)) + '!'


        # 3순위 : 문 닫거나 올라가거나 내려가기
        for i, ev in enumerate(elevators):
            if command[i] == -1:  # 아직 명령을 수행하지 않은 엘리베이터만
                if ev.status == "OPENED":
                    command[i] = ev.close()
                    ev_stat[ev.id] = 'close to move'

                else:
                    if ev.direction == "upward" and ev.floor != height: # 그냥 올라가면 됨
                        command[i] = ev.up()
                        ev_stat[ev.id] = 'go up'

                    elif ev.direction == "downward" and ev.floor != 1: # 그냥 내려가면 됨
                        command[i] = ev.down()
                        ev_stat[ev.id] = 'go down'

                    elif ev.direction == "upward" and ev.floor == height: # 올라가다가 꼭대기 도착한 경우
                        ev.direction = "stop_maxheight"
                        command[i] = ev.stop()
                        ev_stat[ev.id] = 'top of building'

                    elif ev.direction == "stop_maxheight" and ev.floor == height: # 꼭대기에서 멈춰 있는 경우
                        ev.direction = "downward"
                        command[i] = ev.down()
                        ev_stat[ev.id] = 'go down'

                    elif ev.direction == "downward" and ev.floor == 1: # 내려가다가 1층 도착한 경우
                        ev.direction = "stop_minheight"
                        command[i] = ev.stop()
                        ev_stat[ev.id] = '1th floor'

                    elif ev.direction == "stop_minheight" and ev.floor == 1: # 1층에서 멈춰 있는 경우
                        ev.direction = "upward"
                        command[i] = ev.up()
                        ev_stat[ev.id] = 'go up'


        # ===== 진행상황 표시용 =====
        for i in range(4):
            print(i, ev_stat[i])

        print()
        for i in range(height, 0, -1):
            tmp = []
            for call in calls:
                if call.start == i:
                    tmp.append(call.id)

            print('floor', i, ':', end=' ')
            for t in tmp:
                print(t, end=' ')

            for ev in elevators:
                if ev.floor == i:
                    print('  ['+str(ev.id)+')', end=' ')
                    for person in ev.passengers:
                        print(person.id, end=' ')
                    print(']', end = ' ')

            print()
        print()
        # ====================


        print(command)
        print('\n','======================================','\n')
        # 4순위 : action 실행, 엘리베이터 상태 업데이트
        ret = action(token, command)

        for i in range(4):
            elevators[i].updateStatus(ret['elevators'][i])


        # 5순위 : isend 체크
        isend = ret['is_end']


if __name__ == '__main__':
    p0_simulator()