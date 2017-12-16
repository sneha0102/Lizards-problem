#!/usr/bin/python3
import os,sys,math
import time,multiprocessing
import queue
import signal
from copy import deepcopy 
from random import randint,randrange,uniform

global count,flag
count=0
flag=0
def can_place_lizard(row,col):
	global sol_m

	for i in range(col,-1,-1):
		if sol_m[row][i] == 1:
			return False
		elif sol_m[row][i] == 2:
			break
	# Check upper diagonal
	for i,j in zip(range(row,-1,-1),range(col,-1,-1)):
		if sol_m[i][j]==1:
			return False
		elif sol_m[i][j]==2:
			break
	# Check lower diagonal
	for i,j in zip(range(row,n,1),range(col,-1,-1)):
		if sol_m[i][j] == 1 :
			return False
		elif sol_m[i][j] == 2:
			break
	# Check column up
	for i in range(row,-1,-1):
		if sol_m[i][col] == 1:
			return False
		elif sol_m[i][col] == 2:
			break
	# Check column down
	for i in range(row,n,1):
		if sol_m[i][col] == 1:
			return False
		elif sol_m[i][col] == 2:
			break
	return True



def place_lizard_column(row,col): 
	global sol_m
	global count
	if count == lizards:
		return True
	if row > n-1 :
		row=0
	# Loop through each cell from row
	repeat = True
	flag=0
	while repeat == True :		
		for i in range(row,n):
			if i == n-1 and col == n-1:
				repeat=False
			if flag==1:
				col=col+1
				flag=0
			if i == n-1 and col < n-1:
				row =0
				flag=1
			if sol_m[i][col] == 2:
				pass
			elif can_place_lizard(i,col) == True:
				sol_m[i][col] = 1
				count=count+1
				if col<n and place_lizard_column(i+1,col) == True:
					return True

				sol_m[i][col] = 0
				count = count -1
				if i>=n:
					count=count-1
					return False
			
def place_lizard(row):
	global count
	global m
	global sol_m
	c=0
	sol_m=deepcopy(m)
	flag=0
	for a in range(0,n):
		if flag == 1:
			break
		for b in range(0,n):
			if sol_m[b][a] == 0:
				c=a
				flag=1
				break
	for i in range(0,n):
		sol_m=deepcopy(m)

		if sol_m[i][c] != 2:
			if can_place_lizard(i,c) == True:
				sol_m[i][c] = 1
				count = count + 1

				if place_lizard_column(i+1,0) == True:
					return True
			else:
				sol_m[i][c]=0
				count = count -1

			count=count-1

	return False


def can_place_lizard_bfs(row,col,sol_bfs):

	# Check row left
	for i in range(col,-1,-1):
		if sol_bfs[row][i] == 1:
			return False
		elif sol_bfs[row][i] == 2:
			break
	# Check row right
	for i in range(col,n,1):
		if sol_bfs[row][i] == 1:
			return False
		elif sol_bfs[row][i] == 2:
			break
	# Check left upper diagonal
	for i,j in zip(range(row,-1,-1),range(col,-1,-1)):
		if sol_bfs[i][j]==1:
			return False
		elif sol_bfs[i][j]==2:
			break
	# Check left lower diagonal
	for i,j in zip(range(row,n,1),range(col,-1,-1)):
		if sol_bfs[i][j] == 1 :
			return False
		elif sol_bfs[i][j] == 2:
			break
	# Check column up
	for i in range(row,-1,-1):
		if sol_bfs[i][col] == 1:
			return False
		elif sol_bfs[i][col] == 2:
			break
	# Check column down
	for i in range(row,n,1):
		if sol_bfs[i][col] == 1:
			return False
		elif sol_bfs[i][col] == 2:
			break
	
	# Check right upper diagonal
	for i,j in zip(range(row,-1,-1),range(col,n,1)):
		if sol_bfs[i][j]==1:
			return False
		elif sol_bfs[i][j]==2:
			break
	# Check right lower diagonal
	for i,j in zip(range(row,n,1),range(col,n,1)):
		if sol_bfs[i][j] == 1 :
			return False
		elif sol_bfs[i][j] == 2:
			break
	return True


def getChildren(current):
	children=[]
	flag=0
	
	for j in range(0,n):
		for i in range(0,n):
			
			if can_place_lizard_bfs(i,j,current) and current[i][j]!=2 and current[i][j]!=1:
				temp_mat=[row[:] for row in current]				
				temp_mat[i][j]=1

				children.append(temp_mat)
	return children



def place_lizard_bfs(sol_bfs):

	bfs_queue=queue.Queue(maxsize=0)
	bfs_queue.put(sol_bfs)

	while bfs_queue.empty() != True:
		current=bfs_queue.get(block=False, timeout=None)
		bfs_queue.task_done()

		#check goal state -loop
		count = 0
		for i in range(0,n):
			for j in range(0,n):
				if current[i][j] == 1:
					count = count +1
		if count == lizards:
			fo = open("output.txt",'w+')
			fo.write("OK\n")
			for i in current:
				fo.write("".join(map(str,i)))
				fo.write("\n")
			fo.close()
			return True

		#find children
		children=getChildren(current)
		if children is not None:
			for l in children:
				if l in bfs_queue.queue:
					pass
				else:
					bfs_queue.put(l)
	return False


def generate_random_positions(m,n):
	c=0
	initial=[row[:] for row in m]
	while c!=lizards:
		x=randint(0,n-1)
		y=randint(0,n-1)
		if initial[x][y] == 0:
			initial[x][y] = 1
			c=c+1
	return initial

def find_random_next(i,j):
	a=(i+randint(0,n-1))%n
	b=(j+randint(0,n-1))%n
	# print(i,j," : ",a,b)
	return a,b

def generate_next(m,current):
	c=0
	next=[row[:] for row in current]
	while True:
		i = randint(0,n-1)
		j = randint(0,n-1)
		if next[i][j] == 1:
			next[i][j] = 0
			a,b = find_random_next(i,j)
			flag=0
			while flag==0:
				if next[a][b] == 0 :
					next[a][b] = 1
					flag=1
					return next
				else:
					a,b = find_random_next(i,j)

def find_conflicts(mat):
	conflicts=0
	for i in range(0,n):
		for j in range(0,n):
			if mat[i][j]==1:
				mat[i][j] = 0 
				if can_place_lizard_bfs(i,j,mat) == False:
					conflicts=conflicts +1
				mat[i][j]=1
	return conflicts

def probability_function(p):
	r=uniform(0,1)
	if r <=p :
		return True
	return False


def main():
	# Accept input
	
	global n
	# global sol_m
	global lizards
	global col
	global m
	m=[]
	col=0

	with open('input.txt') as f:
		algo = f.readline().strip()
		n  = int(f.readline().strip())
		lizards = int(f.readline().strip())
		fo = open("output.txt",'w+')

		if n>=0 and n<2**32:
			pass
		else:
			fo.write("FAIL")
			return "FAIL"
		if lizards>=0 and lizards<2**32:
			pass
		else:
			fo.write("FAIL")
			return "FAIL"
		if n == 0 :
			fo.write("FAIL")
			return "FAIL"
		for i in range(n):
			m.append(list( int(i) for i in f.readline().strip()))
	f.close()


	if algo == "DFS" :
		global sol_m
		sol_m=[row[:] for row in m]

		result = place_lizard(0)
		if result is  False:
			fo.write("FAIL\n")
			sys.exit()
		else:
			fo.write("OK\n")
			for i in sol_m:
				fo.write("".join(map(str,i)))
				fo.write("\n")
			sys.exit()
	elif algo == "BFS":
		sol_bfs=[row[:] for row in m]

		result= place_lizard_bfs(sol_bfs)
		if result is  False:
			fo.write("FAIL\n")
			sys.exit()
		else:
			sys.exit()
	
	elif algo == "SA":

		current = generate_random_positions(m,n)
		t=0
		C=0.1
		d=9
		while True:
			T = C/(math.log(t+d))  #schedule[t]
			if T==0:
				fo = open("output.txt",'w+')
				fo.write("FAIL\n")
				fo.close()
				sys.exit()
				return False
			next_m = generate_next(m,current)

			delta = find_conflicts(next_m) - find_conflicts(current)
			if find_conflicts(next_m) == 0:
				fo.write("OK\n")
				for i in next_m:
					fo.write("".join(map(str,i)))
					fo.write("\n")
				sys.exit()
			if delta < 0:
				current = next_m
			else:
				p=math.e**(-(delta)/T)
				if probability_function(p):
					current = next_m

			t = t+1

		

if __name__ == "__main__":
	
    p = multiprocessing.Process(target=main)
    p.start()
    

    # Wait for 285 seconds or until process finishes
    p.join(5000)
    if p.is_alive():
        # print ("running... let's kill it...")
        fo = open("output.txt",'w+')
        fo.write("FAIL\n")
        fo.close()

        # Terminate
        p.terminate()
        p.join()	

		




