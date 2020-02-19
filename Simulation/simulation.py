from dataclasses import dataclass
import numpy as np
from math import sqrt
from time import time
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from random import sample, choices


def create_field():
	'''
	Создаем поле
	'''
	field = np.zeros((21, 15))
	half_exit = 7
	shape = field.shape
	
	#верх сужения
	up = int((shape[0] - half_exit)/2)
	c = half_exit
	for i in range(up):
		for j in range(shape[1] - c, shape[1]):
			field[i, j] = 2		
		c -= 1
	
	#низ сужения
	down1 = int(shape[0] - half_exit)
	down2 = shape[0]
	c = 1
	for i in range(down1, down2):
		for j in range(shape[1] - c, shape[1]):
			field[i, j] = 2
		c += 1
		
	return field


def create_ims(field):
		ims = []    #для scatter's
		counter = 0 #для вывода в консоль
		for frame in field._frames:
			im = []
			blue_x, blue_y = [], []		
			red_x, red_y = [], []	
			shape = frame.shape
			
			for i in range(shape[0]):
				for j in range(shape[1]):
					if frame[i, j] == 2:
						red_x.append(j)
						red_y.append(-i) #минус чтобы не инвертирвоал верх и низ pyplot
					elif frame[i, j] == 1:					
						blue_x.append(j)
						blue_y.append(-i)
			
			im.append(plt.scatter(blue_x, blue_y, c='blue', s=100, marker='s'))
			im.append(plt.scatter(red_x, red_y, c='red', s=120, marker='s'))
			counter += 1
			print(f'frame {counter} ready')
			ims.append(im)
		
		return ims	
		

@dataclass
class Field:
	_field = create_field()
	_shape = _field.shape
	_frames = [] 
	_n = 19 #max кол-во точек в первом столбце
	
		
	def save_frame(self):
		'''Сохранение фрейма'''
		copy = np.copy(self._field)
		self._frames.append(copy)
		
		
	def spawn_first_row(self):
		'''Спавн перого ряда'''
		#Получаем первый ряд и 'вырезаем' несвободные элементы
		current_frow = self._field[:,0]
		indxs = []
		for indx, j in enumerate(current_frow):
			if j != 1:
				indxs.append(indx)
		
		#рассчитываем сколько точек нужно создать
		n_in_row = self._n #количество точек в первом столбце
		lines = []
		b = self._shape[0] - len(indxs)
		if self._shape[0] - b > self._shape[0] - n_in_row:
			lines = sample(indxs, n_in_row - b)
		
		dots = []
		for i in lines:
			dots.append([i, 0])
			
		for i in dots:
			self._field[i[0], i[1]] = 1
			
		
	def move_dots(self):
		'''Двигаем точки начиная с конца'''
		#удаляем точки на выходе
		for i in range(self._shape[0]):
			if self._field[i, self._shape[1] - 1] == 1:
				self._field[i, self._shape[1] - 1] = 0
		
		#двигаем
		for i in range(self._shape[1]):
			current_row = []
			for j in range(self._shape[0]):	
				if self._field[j, self._shape[1] - 1 - i] == 1:
					
					dot = [j, self._shape[1] - 1 - i]	
					direction = self._black_box(dot)

					if direction == 'N':
						ndot = [dot[0], dot[1] + 1]
						self._field[ndot[0], ndot[1]] = 1
						current_row.append(dot)
					elif direction == 'S':
						ndot = []
						self._field[dot[0], dot[1] - 1] = 1
						current_row.append(dot)
					elif direction == 'E':
						ndot = [dot[0] - 1, dot[1]]
						self._field[ndot[0], ndot[1]] = 3
						current_row.append(dot)
					elif direction == 'W':
						ndot = [dot[0] + 1, dot[1]]
						self._field[ndot[0], ndot[1]] = 3
						current_row.append(dot)
					elif direction == 'stay':
						current_row.append(dot)
						
			for dot in current_row:
				self._field[dot[0], dot[1]] = 0
				
		for i in range(self._shape[0]):
			for j in range(self._shape[1]):
				if self._field[i, j] == 3:
					self._field[i, j] = 1
					
				
	def _calc_sin(self, dot):
		'''Вычисляем dsin'''
		centr = int((self._shape[0] - 1)/2)
		sinus = 0
		if dot[0] < centr:
			a = centr - dot[0]
			b = self._shape[1] + 2 - dot[1] + 1
			c = sqrt(a**2 + b**2)
			sinus =  a/c
		elif dot[0] > centr: 
			a = dot[0] - centr
			b = self._shape[1] + 2 - dot[1] + 1
			c = sqrt(a**2 + b**2)
			sinus = -a/c
		else:
			sinus = 0
		
		W = (sinus**2 + 1 / 3) if sinus <= 0 else 3
		E = (sinus**2 + 1 / 3) if sinus >= 0 else 3
		N = 1 - sinus**2
		S = (sinus**2 + 1 / 3)/6
		
		return [N, S, E, W]
		
	
	def _view_dirs(self, dot):
		'''Смотрим по направлениям'''
		N, S, E, W = 0, 0, 0, 0
		tN, tS, tE, tW = True, True, True, True #для проверки необходимости 'смотреть'
		kek = [1, 2, 3]
		for i in range(1, 4):
			if dot[0] + i < self._shape[0] and self._field[dot[0] + i, dot[1]] == 0 and tW:
				W += 1
			elif tW == True:
				tW = False
				
			if dot[0] - i >= 0 and self._field[dot[0] - i, dot[1]] == 0 and tE:
				E += 1
			elif tE == True:
				tE = False
				
			if dot[1] + i < self._shape[1] and self._field[dot[0], dot[1] + i] == 0 and tN:
				N += 1
			elif tN == True:
				tN = False
				
			if dot[1] - i >= 0 and self._field[dot[0], dot[1] - i] == 0 and tS:
				S += 1
			elif tS == True:
				tS = False
		
		values = [0, 0.5, 0.75, 1]
		N = values[N]
		S = values[S]
		E = values[E]
		W = values[W]
		
		return [N, S, E, W]
		
		
	def _black_box(self, dot):
		#сделать рандом с помощью равномерной случ велич
		dirs = self._calc_sin(dot)# N S E W	
		free_dirs = self._view_dirs(dot)
		profit = [dirs[i] * free_dirs[i] for i in range(4)]
		
		maxel = 0
		maxIndex = 0
		for i in range(len(profit)):
			if profit[i] > maxel:
				maxel = profit[i]
				maxIndex = i
		directions = ['N', 'S', 'E', 'W']
		
		iszero = any(profit)
		if not iszero:
			maxIndex = 0
			directions = ['stay']
			
		return directions[maxIndex]
		


		

if __name__ == '__main__':
	start = time()
	field = Field()
	
	c = 0
	while True:
		c += 1
		if c <= 100:
			field.spawn_first_row()
		field.save_frame()
		field.move_dots()
		field.save_frame()
		if 1 not in field._field:
			break
	print('Preframe preparation completed.')
	print(f'{len(field._frames)} frames will be created')
	print('Frame preparation begins...')
	
	fig = plt.figure(figsize=(5, 6),dpi=150)
	#fig = plt.figure()
	
	ims = create_ims(field)
	print(f'Time spent: {time()-start}')
	
	ani = animation.ArtistAnimation(fig, ims, interval=70, blit=False, repeat_delay=2)
		
	plt.show()
	plt.close(fig)
