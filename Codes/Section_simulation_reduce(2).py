# -*- coding:utf-8 -*-
import Queue
import threading
import os
import math
import random

class people:
    def __init__(self,arrive_time):
        self.wait_time=0
        self.arrive_time=arrive_time
        self.process_time=[]
        self.end_time=0

class simulation:
    def __init__(self,time_args,limit):
        self.time_clock=0
        self.people_num=0
        self.people_limit=limit
        
        self.people_line=[[[],[],[],Queue.Queue()],[[],[],[],Queue.Queue()],Queue.Queue()]

        self.next_tsa_people_time=0
        self.next_regular_people_time=0

        self.tsa_IDcheck_time=time_args[0]
        self.regular_IDcheck_time=time_args[1]

        self.tsa_Xray_time=time_args[2]
        self.regular_Xray_time=time_args[3]

        self.Milimeter_time=time_args[4]
        self.getbags_time=time_args[5]


    def generate_people(self):
            if self.time_clock >= self.next_tsa_people_time and self.people_num<self.people_limit:
                print 'A passenger arrive'
                self.people_line[0][3].put(people(self.time_clock))
                self.people_num+=1
                self.next_tsa_people_time=self.time_clock+self.generate_time()
                print 'Next passenger arrive time',self.next_tsa_people_time

    def generate_time(self):
        return math.log(random.uniform(0,0.4762)/0.4762,math.e)/-0.2065
        
    def IDcheck(self,index):
        while 1:
            people=False
            if len(self.people_line[0][index]) == 0:
                for i in range(3)[1:]:
                    if not len(self.people_line[0][(index-i)%3])==0:
                        people=self.people_line[0][(index-i)%3].pop(random.randint(0,len(self.people_line[0][(index-i)%3])-1))
                        break
            else:
                people=self.people_line[0][index].pop(0)
            if people:
                print 'IDcheck begin'
                IDcheck_time=self.tsa_IDcheck_time
                people.wait_time+=IDcheck_time
                people.process_time.append(IDcheck_time)
                begin_time_clock=self.time_clock+IDcheck_time
                print 'IDcheck service time ',IDcheck_time
                while self.time_clock<begin_time_clock:
                    pass
                self.people_line[1][3].put(people)
                print 'IDcheck over and enter getbags'


    def analysis(self):
        print '----------------------------Finished------------------------------'
        dif="'"
        begin="'"
        end="'"
        all_arrive=[]
        while not self.people_line[2].empty():
            people=self.people_line[2].get()
            print 'begin time ',people.arrive_time
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
        print sums/(len(all_arrive)-1)
        print '----------------------------Finished------------------------------'
        print 'Passenger number: ',self.people_num
        
    def getbags(self,index):
        while 1:
            people=False
            if len(self.people_line[1][index]) == 0:
                for i in range(3)[1:]:
                    if not len(self.people_line[1][(index-i)%3])==0:
                        people=self.people_line[1][(index-i)%3].pop(random.randint(0,len(self.people_line[1][(index-i)%3])-1))
                        break
            else:
                people=self.people_line[1][index].pop(0)

            if people:
                wave_num = math.log(random.uniform(0,0.987)/0.987,math.e)/-0.4805
                getbags_time=random.uniform(self.getbags_time - wave_num,self.getbags_time + wave_num)
                people.wait_time+=getbags_time
                people.process_time.append(getbags_time)
                begin_time_clock=self.time_clock+getbags_time
                print 'TSA getbags service time ',getbags_time
                while self.time_clock<begin_time_clock:
                   pass
                people.end_time=self.time_clock
                self.people_line[2].put(people)
                print 'TSA getbags over '

    def check_run(self,):
        threads=[]
        threads.append(threading.Thread(target=self.IDcheck,args=(0,)))
        threads.append(threading.Thread(target=self.IDcheck,args=(1,)))
        threads.append(threading.Thread(target=self.IDcheck,args=(2,)))
        
        threads.append(threading.Thread(target=self.getbags,args=(0,)))
        threads.append(threading.Thread(target=self.getbags,args=(1,)))
        threads.append(threading.Thread(target=self.getbags,args=(2,)))
        
        threads.append(threading.Thread(target=self.manage,args=()))
        for thread in threads:
            thread.start()

    def run(self):
        self.check_run()
        while self.people_num < self.people_limit:
            self.time_clock+=0.1
            #print 'Now time ：',self.time_clock
            self.generate_people()
        while self.is_finished():
            self.time_clock+=0.1
            #print 'Now time ：',self.time_clock
        self.analysis()
    
    def is_finished(self):
        if self.people_line[2].qsize() >= self.people_limit:
            return False
        else:
            return True

    def manage(self):
        while 1:
            for index in range(3):
                if len(self.people_line[0][index])==0 and not self.people_line[0][3].empty():
                    for i in range(min(4,self.people_line[0][3].qsize())):
                        self.people_line[0][index].append(self.people_line[0][3].get())

                if len(self.people_line[1][index])==0 and not self.people_line[1][3].empty():
                    for i in range(min(4,self.people_line[1][3].qsize())):
                        self.people_line[1][index].append(self.people_line[1][3].get())


test=simulation([10.1967,12.5514,0,0,11.6372,28.6207],45)
test.run()
os._exit(0)
