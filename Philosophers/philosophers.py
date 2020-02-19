from threading import Lock, Thread, BoundedSemaphore, Semaphore
from time import sleep
from random import randint
from datetime import datetime


fork1 = Lock()
fork2 = Lock()
fork3 = Lock()
fork4 = Lock()
fork5 = Lock()


class Forks():
	forks = [[fork1, fork2], [fork2, fork3], [fork3, fork4], [fork4, fork5], [fork5, fork1]]
	s = Semaphore(4)
	
	
	def get_left_fork(self, c):
		try:
			self.s.acquire()
		except ValueError:
			return False
		else:
			self.forks[c][0].acquire()
			print(f'{datetime.now()}:  {c + 1} takes  left')
			return True
		
	
	def get_right_fork(self, c):
		self.forks[c][1].acquire()
		print(f'{datetime.now()}:  {c + 1} takes  right')
		
	
	def put_forks(self, c):
		self.s.release()
		print(f'{datetime.now()}:  {c + 1} puts  left')
		self.forks[c][0].release()
		
		self.s.release()
		print(f'{datetime.now()}:  {c + 1} puts  right')
		self.forks[c][1].release()
		

class Phils(Thread):
	_c = 1
	forks = Forks()
	
	def __init__(self, name):
		super().__init__(name=name)
		self.c = __class__._c
		__class__._c += 1
		
	
	def run(self):
		while True:
			sleep(randint(0, 3)) #Думает
			a = __class__.forks.get_left_fork(self.c - 1)
			if not a:
				continue
			
			b = __class__.forks.get_right_fork(self.c - 1)
				
			print(f'{datetime.now()}:  {self.c}  eating...')
			sleep(randint(0, 3)) #Ест
			__class__.forks.put_forks(self.c - 1)
			
			print(f'{datetime.now()}:  {self.c}  Finished')
			sleep(2) #Отдыхает
				
				
				
if __name__ == '__main__':			
	f1 = Phils('1')
	f2 = Phils('2')
	f3 = Phils('3')
	f4 = Phils('4')
	f5 = Phils('5')

	f1.start()
	f2.start()
	f3.start()
	f4.start()
	f5.start()

	f1.join()
	f2.join()
	f3.join()
	f4.join()
	f5.join()
