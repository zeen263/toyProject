class Elevator:
    def __init__(self, _id, _floor, _passengers, _status):
        self.id = _id
        self.floor = _floor
        self.passengers = _passengers
        self.quota = 0
        self.status = _status
        self.direction = "upward"


    def updateStatus(self, dic):
        self.floor = dic['floor']
        self.passengers = self.__setPassengers(dic['passengers'])
        self.quota = len(self.passengers)
        self.status = dic['status']

    def __setPassengers(self,lst):
        ret = []
        for person in lst:
            p_id = person['id']
            p_stamp = person['timestamp']
            p_start = person['start']
            p_end = person['end']
            ret.append(Call(p_id, p_stamp, p_start, p_end))
        return ret

    def exitablePassengers(self):
        ret = []
        if self.passengers:
            for person in self.passengers:
                if person.end == self.floor:
                    ret.append(person.id)
        return ret

    def stop(self):
        return {"elevator_id":self.id, "command":"STOP"}

    def up(self):
        return {"elevator_id":self.id, "command":"UP"}

    def down(self):
        return {"elevator_id":self.id, "command":"DOWN"}

    def open(self):
        return {"elevator_id":self.id, "command":"OPEN"}

    def close(self):
        return {"elevator_id":self.id, "command":"CLOSE"}

    def enter(self, lst):
        return {"elevator_id":self.id, "command":"ENTER", "call_ids":lst}

    def exit(self, lst):
        return {"elevator_id":self.id, "command":"EXIT", "call_ids":lst}




class Call:
    def __init__(self, _id, _timestamp, _start, _end):
        self.id = _id
        self.timestamp = _timestamp
        self.start = _start
        self.end = _end
        if self.start > self.end:
            self.direction = -1   # down
        else:
            self.direction = 1    # up

