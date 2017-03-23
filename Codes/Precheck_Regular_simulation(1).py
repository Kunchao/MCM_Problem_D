# -*- coding:utf-8 -*-
import Queue
import threading
import os
import math
import random

class people:
    def __init__(self,precheck,arrive_time):
        self.wait_time=0
        self.precheck=precheck
        self.arrive_time=arrive_time
        self.process_time=[]
        self.end_time=0

class simulation:
    def __init__(self,time_args,limit,percentage):
        self.time_clock=0
        self.tsa_people_limit=limit*percentage
        self.reg_people_limit=limit*(1-percentage)
        
        self.tsa_people_line=[Queue.Queue(),Queue.Queue(),Queue.Queue()]
        self.regular_people_line=[Queue.Queue(),Queue.Queue(),Queue.Queue()]

        self.next_tsa_people_time=0
        self.next_regular_people_time=0

        self.tsa_people_num=0
        self.reg_people_num=0

        self.tsa_IDcheck_time=time_args[0]
        self.regular_IDcheck_time=time_args[1]

        self.tsa_Xray_time=time_args[2]
        self.regular_Xray_time=time_args[3]

        self.Milimeter_time=time_args[4]
        self.getbags_time=time_args[5]


    def generate_people(self):
            if self.time_clock >= self.next_tsa_people_time and self.tsa_people_num<self.tsa_people_limit:
                print 'A Precheck passenger arrive'
                self.tsa_people_line[0].put(people(True,self.time_clock))
                self.tsa_people_num+=1
                self.next_tsa_people_time=self.time_clock+self.generate_tsa_time()
                print 'Next Precheck passenger arrive time：',self.next_tsa_people_time

            if self.time_clock >= self.next_regular_people_time and self.reg_people_num<self.reg_people_limit:
                print 'A Regular passenger arrive'
                self.regular_people_line[0].put(people(False,self.time_clock))
                self.reg_people_num+=1
                self.next_regular_people_time=self.time_clock+self.generate_regular_time()
                print 'Next Regular passenger arrive time：',self.next_regular_people_time

    def generate_tsa_time(self):
        #return math.log(random.uniform(0,0.4762)/0.4762,math.e)/-0.1065
        return math.log(random.uniform(0,0.4762)/0.4762,math.e)/-0.2065
        
    def generate_regular_time(self):
        return math.log(random.uniform(0,2.257)/2.257,math.e)/-0.0749

    def IDcheck(self,precheck):
        if precheck:
            while 1:
                people=self.tsa_people_line[0].get()
                print 'TSA IDcheck begin'
                IDcheck_time=self.tsa_IDcheck_time
                people.wait_time+=IDcheck_time
                people.process_time.append(IDcheck_time)
                begin_time_clock=self.time_clock+IDcheck_time
                print 'TSA IDcheck service time ',IDcheck_time
                while self.time_clock<begin_time_clock:
                    pass
                self.tsa_people_line[1].put(people)
                print 'TSA IDcheck over and enter getbags'
        else:
            while 1:
                people=self.regular_people_line[0].get()
                print 'REG IDcheck begin'
                IDcheck_time=self.regular_IDcheck_time
                people.wait_time+=IDcheck_time
                people.process_time.append(IDcheck_time)
                begin_time_clock=self.time_clock+IDcheck_time
                print 'REG IDcheck service time ',IDcheck_time
                while self.time_clock<begin_time_clock:
                    pass
                self.regular_people_line[1].put(people)
                print 'REG IDcheck over and enter getbags'

    def analysis(self):
        print '----------------------------Finished------------------------------'
        print '--------------------TSA Precheck passengers----------------------'
        dif="'"
        begin="'"
        end="'"
        all_arrive=[]
        while not self.tsa_people_line[2].empty():
            people=self.tsa_people_line[2].get()
            print 'begin time ',people.arrive_time
            print 'PreCheck ',people.precheck
            print 'wait_time ',people.wait_time
            print 'end time ',people.end_time
            print 'Process time ',people.process_time
            begin+=str(people.arrive_time)+"','"
            end+=str(people.end_time)+"','"
            dif+=str(people.end_time-people.arrive_time)+"','"
            all_arrive.append(people.arrive_time)
        print begin[:-2]
        print end[:-2]
        print dif[:-2]
        sums=0
        for i in range(len(all_arrive)-1):
            sums+=all_arrive[i+1]-all_arrive[i]
        print 'Interval time:',sums/(len(all_arrive)-1)
        print '--------------------Regular Precheck passengers----------------------'
        dif="'"
        begin="'"
        end="'"
        all_arrive=[]
        while not self.regular_people_line[2].empty():
            people=self.regular_people_line[2].get()
            print 'begin time ',people.arrive_time
            print 'PreCheck',people.precheck
            print 'wait_time',people.wait_time
            print 'end time ',people.end_time
            print 'Process time ',people.process_time
            begin+=str(people.arrive_time)+"','"
            end+=str(people.end_time)+"','"
            dif+=str(people.end_time-people.arrive_time)+"','"
            all_arrive.append(people.arrive_time)
        print 'Begin Time :',begin[:-2]
        print 'End Time :',end[:-2]
        print 'Wait Time :',dif[:-2]
        sums=0
        for i in range(len(all_arrive)-1):
            sums+=all_arrive[i+1]-all_arrive[i]
        print 'Interval time:',sums/(len(all_arrive)-1)
        print '----------------------------Finished------------------------------'
        print 'Passengers number: ',self.reg_people_num+self.tsa_people_num
        
    def getbags(self,precheck):
        if precheck:
            while 1:
                people=self.tsa_people_line[1].get()
                wave_num = math.log(random.uniform(0,0.987)/0.987,math.e)/-0.4805
                getbags_time=random.uniform(self.getbags_time - wave_num,self.getbags_time + wave_num)
                people.wait_time+=getbags_time
                people.process_time.append(getbags_time)
                begin_time_clock=self.time_clock+getbags_time
                print 'TSA getbags service time ',getbags_time
                while self.time_clock<begin_time_clock:
                    pass
                people.end_time=self.time_clock
                self.tsa_people_line[2].put(people)
                print 'TSA getbags over '
        else:
            while 1:
                people=self.regular_people_line[1].get()
                wave_num = math.log(random.uniform(0,0.987)/0.987,math.e)/-0.4805
                getbags_time=random.uniform(self.getbags_time-wave_num,self.getbags_time+wave_num)+self.Milimeter_time
                people.wait_time+=getbags_time
                people.process_time.append(getbags_time)
                begin_time_clock=self.time_clock+getbags_time
                print 'REG getbags service time ',getbags_time
                while self.time_clock<begin_time_clock:
                    pass
                people.end_time=self.time_clock
                self.regular_people_line[2].put(people)
                print 'REG getbags over '

    def check_run(self):
        threads=[]
        threads.append(threading.Thread(target=self.IDcheck,args=(True,)))
        threads.append(threading.Thread(target=self.IDcheck,args=(True,)))
        threads.append(threading.Thread(target=self.IDcheck,args=(True,)))
        
        threads.append(threading.Thread(target=self.IDcheck,args=(False,)))

        threads.append(threading.Thread(target=self.getbags,args=(True,)))
        threads.append(threading.Thread(target=self.getbags,args=(True,)))
        threads.append(threading.Thread(target=self.getbags,args=(True,)))
        
        threads.append(threading.Thread(target=self.getbags,args=(False,)))

        for thread in threads:
            thread.start()

    def run(self):
        self.check_run()
        while self.tsa_people_num + self.reg_people_num < self.tsa_people_limit + self.reg_people_limit:
            self.time_clock+=0.1
            #print 'Now time：',self.time_clock
            self.generate_people()
        while self.is_finished():
            self.time_clock+=0.1
            #print 'Now time：',self.time_clock
        self.analysis()
    
    def is_finished(self):
        if self.tsa_people_line[2].qsize()+self.regular_people_line[2].qsize() >= self.tsa_people_limit + self.reg_people_limit:
            return False
        else:
            return True


test=simulation([10.1967,12.5514,0,0,11.6372,28.6207],100,0.45)
test.run()
os._exit(0)
