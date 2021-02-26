import sys
#盤面
#450 line
board=[]
board_weight=[]
step=0
#下棋邏輯：下下去會贏(六/雙活四)>被下下去會輸(現在單活四/未來雙活四)
#攻擊要對所有自己棋子附近為'.'的做update 5格內
#防守要對對方剛下的兩步棋附近為'.'的做detect 4格內
#連數,被擋邊數							   不連貫   xoooo o
#weight_dic={'5':15,'40':14,'30':13,'41':13,'31':12,'n5':15,'n40':13,'n30':12,'n41':12,'n31':10}
#weight=[]
#權重設計
#---------------------------
#攻擊:
#1.第一步:
#	10	下完會連五 且至少1邊沒被擋 
#	9	下完會連四 且都沒被擋
#	8	下完會連三 且都沒被擋 ooo
#	8	下完會連四 被檔一邊 xoooo
#	n	下完這子 還需幾子才能滿六 且都沒被擋
#	n-2	下完這子 還需幾子才能滿六 且一邊被擋
#	0	就算下了也無法六 (兩邊早已被堵死)
#2.第二步:
#	10 下完會連六 
#	 9 下完會連四 且都沒被擋
#	 8 下完會連四 且一邊被擋
#	 n 下完這子 還需幾子才能滿六 且都沒被擋
#	 n-2 下完這子 還需幾子才能滿六 且一邊被擋
#	 ? 下完會連五								xoooo.
#													 .
'''													 o
													 o'''
#防守:
#1.第一步:
#	10 發現對方有連四	xxxx
#	9  下完可擋對方可能連四的機會	xoxx
#	n  同一排上，下完可擋對方棋子個數	x xo :2 or x x o :2
#	
def init(r):
	#print(len(r))
	global board,board_weight,step,step_1,step_2,opponent
	#matrix=[['.']*r for i in range(len(r))
	board=[ ['.'] * int(r) for i in range(int(r)) ]
	board_weight=[ [0] * int(r) for i in range(int(r)) ]
	#步數初始
	#大步
	step = 1
	#小步第一步
	step_1 = 0
	step_2 = 1
	opponent = [[-1,-1],[-1,-1]]
def CheckIsDot(check_point):
	if check_point == '.':
		return 1
	else:
		return 0
def check_finish(row,col):
	End=False
	count=1
	color=board[row][col]	
	col1=col
	#檢查右橫
	try:
		while(1):
			try:
				col1+=1
				if board[row][col1]==color:
					count+=1
				else:
					break
			except:
				break
		col1=col
		#檢查左橫
		while(1):
			try:
				col1-=1
				if board[row][col1]==color:
					count+=1
				else:
					break
			except:
				break
		if count==6:
			End=True
			return End
		else:
			count=1
		row1=row
		#----------------------------------------
		#檢查上直
		while(1):
			try:
				row1+=1
				if board[row1][col]==color:
					count+=1
				else:
					break
			except:
				break
		row1=row
		#檢查下直
		while(1):
			try:
				row1-=1
				if board[row1][col]==color:
					count+=1
				else:
					break
			except:
				break
		if count==6:
			End=True
			return End
		else:
			count=1
		col1=col
		row1=row
		#----------------------------------------
		#檢查右下斜
		while(1):
			try:
				row1+=1
				col1+=1
				if board[row1][col1]==color:
					count+=1
				else:
					break
			except:
				break
		if count==6:
			End=True
			return End
		else:
			count=1
		#檢查左上斜
		col1=col
		row1=row
		while(1):
			try:
				row1-=1
				col1-=1
				if board[row1][col1]==color:
					count+=1
				else:
					break
			except:
				break
		if count==6:
			End=True
			return End
		else:
			count=1
		#----------------------------------------
		#檢查右上
		col1=col
		row1=row
		while(1):
			try:
				row1-=1
				col1+=1
				if board[row1][col1]==color:
					count+=1
				else:
					break
			except:
				break
		if count==6:
			End=True
			return End
		else:
			count=1
		#檢查左下
		col1=col
		row1=row
		while(1):
			try:
				row1+=1
				col1-=1
				if board[row1][col1]==color:
					count+=1
				else:
					break
			except:
				break
		if count==6:
			End=True
			return End
		else:
			count=1
		return End
	except KeyboardInterrupt:
		print('ckeck wrong')
#尋找需更新的位置
def find_step(row,col):
	#左上角點
	if col-5<0:
		col1=0
	else:
		col1=col-5
	if row-5<0:
		row1=0
	else:
		row1=row-5
	#右下角點
	if col+5>18:
		col2=18
	else:
		col2=col+5
	if row+5>18:
		row2=18
	else:
		row2=row+5
	while(row1<=row2):
		col=col1
		while(col<=col2):
			if board[row1][col]=='.':
				update_attack_weight(row1,col)
			col+=1
		row1+=1
#下棋
def draw(row,col):
	board[row][col]='X'
	board_weight[row][col]=-10
	find_step(row,col)
#找出最佳位置(防守)
def detect(position,mod):
	global rest_step
	if(mod == 'col'):
		print("col:("+str(position[0])+','+str(position[2])+')~('+str(position[1])+','+str(position[2])+')'+'middle:('+str(position[3])+','+str(position[2])+')')
		count = position[1] - position[0] +1
		if(count >= 4):
			if(position[1]+1 <= 18):
				if(board[position[2]][position[1]+1] == '.'):
					#board[position[2]][position[1]+1] = 'X'
					draw(position[2],position[1]+1) 
					print("AI put"+":("+str(position[2])+","+str(position[1]+1)+")")
					rest_step-=1
					if(rest_step == 0):
						return
			if(position[0]-1 >= 0):
				if(board[position[2]][position[0]-1] == '.'):
					draw(position[2],position[0]-1)
					print("AI put"+":("+str(position[2])+","+str(position[0]-1)+")")
					rest_step-=1
					if(rest_step == 0):
						return
		elif(count == 3):
			#在右邊
			if(position[1]-position[3]>=1.5):#o.ooo.  o..ooo  .o.ooo
				draw(position[2],position[0]-1) 
				print("AI put"+":("+str(position[2])+","+str(position[0]-1)+")")
				rest_step-=1
				if(rest_step == 0):
					return
			#在左邊
			elif(position[3]-position[0]>=1.5):#.ooo.o  ooo..o  .ooo.o
				draw(position[2],position[1]+1) 
				print("AI put"+":("+str(position[2])+","+str(position[1]+1)+")")
				rest_step-=1
				if(rest_step == 0):
					return
		elif(count == 2):
			#在左邊 演算法關係只會在左
			#oo.oo.  oo..oo  .oo.oo  o.oo.o
			draw(position[2],position[1]+1)
			print("AI put"+":("+str(position[2])+","+str(position[1]+1)+")")
			rest_step-=1
			if(rest_step == 0):
				return
	elif(mod == 'row'):
		print("row:("+str(position[2])+','+str(position[0])+')~('+str(position[2])+','+str(position[1])+')'+'middle:('+str(position[2])+','+str(position[3])+')')
		count = position[1] - position[0] +1
		if(count >= 4):
			if(position[1]+1 <= 18):
				if(board[position[1]+1][position[2]] == '.'):
					draw(position[1]+1,position[2])
					print("AI put"+":("+str(position[1]+1)+","+str(position[2])+")")
					rest_step-=1
					if(rest_step == 0):
						return
			if(position[0]-1 >= 0):
				if(board[position[0]-1][position[2]] == '.'):
					#board[position[0]-1][position[2]] = 'X'
					draw(position[0]-1,position[2])
					print("AI put"+":("+str(position[0]-1)+","+str(position[2])+")")
					rest_step-=1
					if(rest_step == 0):
						return
		elif(count == 3):
			#在下面
			if(position[1]-position[3]>=1.5):#o.ooo.  o..ooo  .o.ooo
				#board[position[0]-1][position[2]] = 'X'
				draw(position[0]-1,position[2]) 
				print("AI put"+":("+str(position[0]-1)+","+str(position[2])+")")
				rest_step-=1
				if(rest_step == 0):
					return
			#在上面
			elif(position[3]-position[0]>=1.5):#.ooo.o  ooo..o  .ooo.o
				#board[position[1]+1][position[2]] = 'X'
				draw(position[1]+1,position[2])
				print("AI put"+":("+str(position[1]+1)+","+str(position[2])+")")
				rest_step-=1
				if(rest_step == 0):
					return
		elif(count == 2):
			#在上面 演算法關係只會在上
			#oo.oo.  oo..oo  .oo.oo  o.oo.o
			#board[position[1]+1][position[2]] = 'X'
			draw(position[1]+1,position[2])
			print("AI put"+":("+str(position[1]+1)+","+str(position[2])+")")
			rest_step-=1
			if(rest_step == 0):
				return
	elif(mod == 'normal'):
		print("slash:("+str(position[1])+','+str(position[0])+')~('+str(position[3])+','+str(position[2])+')'+'middle:('+str(position[5])+','+str(position[4])+')')
		count = position[2] - position[0] + 1
		print(count)
		if(count >= 4):
			if(position[0]-1 >= 0 and position[1]+1<=18):
				if(board[position[0]-1][position[1]+1] == '.'):
					#board[position[0]-1][position[1]+1] = 'X'
					draw(position[0]-1,position[1]+1) 
					print("AI put"+":("+str(position[1]+1)+","+str(position[0]-1)+")")
					rest_step-=1
					if(rest_step == 0):
						return
			if(position[2]+1 <= 18 and position[3]-1>=0):
				if(board[position[2]+1][position[3]-1] == '.'):
					#board[position[2]+1][position[3]-1] = 'X'
					draw(position[2]+1,position[3]-1)
					print("AI put"+":("+str(position[3]-1)+","+str(position[2]+1)+")")
					rest_step-=1
					if(rest_step == 0):
						return
		elif(count == 3):
			#在左下
			if(position[2]-position[4]>=1.5):#o.ooo.  o..ooo  .o.ooo
				#board[position[0]-1][position[1]+1] = 'X'
				draw(position[0]-1,position[1]+1) 
				print("AI put"+":("+str(position[1]+1)+","+str(position[0]-1)+")")
				rest_step-=1
				if(rest_step == 0):
					return
			#在右上
			elif(position[4]-position[0]>=1.5):#.ooo.o  ooo..o  .ooo.o
				#board[position[2]+1][position[3]-1] = 'X'
				draw(position[2]+1,position[3]-1)
				print("AI put"+":("+str(position[3]-1)+","+str(position[2]+1)+")")
				rest_step-=1
				if(rest_step == 0):
					return
		elif(count == 2):
			#在右上 演算法關係只會在右上
			#oo.oo.  oo..oo  .oo.oo  o.oo.o
			#board[position[2]+1][position[3]-1] = 'X'
			draw(position[2]+1,position[3]-1) 
			print("AI put"+":("+str(position[3]-1)+","+str(position[2]+1)+")")
			rest_step-=1
			if(rest_step == 0):
				return
	elif(mod == 'back'):
		print("backslash:("+str(position[1])+','+str(position[0])+')~('+str(position[3])+','+str(position[2])+')'+'middle:('+str(position[5])+','+str(position[4])+')')
		count = position[2] - position[0] + 1
		if(count >= 4):
			if(position[2]+1 <= 18 and position[3]+1<=18):
				if(board[position[2]+1][position[3]+1] == '.'):
					#board[position[2]+1][position[3]+1] = 'X'
					draw(position[2]+1,position[3]+1) 
					print("AI put"+":("+str(position[3]+1)+","+str(position[2]+1)+")")
					rest_step-=1
					if(rest_step == 0):
						return
			if(position[0]-1 >= 0 and position[1]-1>=0):
				if(board[position[0]-1][position[1]-1] == '.'):
					#board[position[0]-1][position[1]-1] = 'X'
					draw(position[0]-1,position[1]-1)
					print("AI put"+":("+str(position[1]-1)+","+str(position[0]-1)+")")
					rest_step-=1
					if(rest_step == 0):
						return
		elif(count == 3):
			#在右下
			if(position[2]-position[4]>=1.5):#o.ooo.  o..ooo  .o.ooo
				#board[position[0]-1][position[1]-1] = 'X'
				draw(position[0]-1,position[1]-1) 
				print("AI put"+":("+str(position[1]-1)+","+str(position[0]-1)+")")
				rest_step-=1
				if(rest_step == 0):
					return
			#在左上
			elif(position[4]-position[0]>=1.5):#.ooo.o  ooo..o  .ooo.o
				#board[position[2]+1][position[3]+1] = 'X'
				draw(position[2]+1,position[3]+1) 
				print("AI put"+":("+str(position[3]+1)+","+str(position[2]+1)+")")
				rest_step-=1
				if(rest_step == 0):
					return
		elif(count == 2):
			#在左上 演算法關係只會在左上
			#oo.oo.  oo..oo  .oo.oo  o.oo.o
			#board[position[2]+1][position[3]+1] = 'X'
			draw(position[2]+1,position[3]+1) 
			print("AI put"+":("+str(position[3]+1)+","+str(position[2]+1)+")")
			rest_step-=1
			if(rest_step == 0):
				return
def find_col(row,col):#如果有單活4觸發detect
	global rest_step
	col_left = col#須判斷的橫線最左
	col_right = col#須判斷的橫線最右
	for i in range(5):
		if (not col_left-1 < 0 and not board[row][col_left-1] == 'X'):
			col_left-=1
		else:
			break
	for i in range(5):
		if (not col_right+1 > 18 and not board[row][col_right+1] == 'X'):
			col_right+=1
		else:
			break
	if (col_right - col_left < 5):
		return#不可能讓對方連6子
	print("find col:"+str(col_left)+"~"+str(col_right))
	
	for col_left in range(col_left,col_right-4):
		biggest_left = col_left#最大相連數的左
		biggest_right = col_left#最大相連數的右
		tmp_biggest_left = col_left
		tmp_biggest_right = col_left
		total_count = 0
		for i in range(6):
			if (board[row][col_left+i] == 'O'):
				total_count+=1
				tmp_biggest_right+=1
			elif(board[row][col_left+i] == '.'):#'.'
				if (tmp_biggest_right - tmp_biggest_left > biggest_right - biggest_left +1):
					print("inner change:"+str(tmp_biggest_left)+" "+str(tmp_biggest_right))
					biggest_left = tmp_biggest_left
					biggest_right = tmp_biggest_right-1
				tmp_biggest_left = col_left+i+1
				tmp_biggest_right = col_left+i+1
			elif(board[row][col_left+i] == 'X'):
				break
		if (tmp_biggest_right - tmp_biggest_left > biggest_right - biggest_left +1):#保留先看到的
			print("outter change:"+str(tmp_biggest_left)+" "+str(tmp_biggest_right))
			biggest_left = tmp_biggest_left
			biggest_right = tmp_biggest_right-1
		if (total_count >= 4):#有單活4detect
			middle = col_left+2.5
			print(col_left)
			detect_position = [biggest_left,biggest_right,row,middle]
			detect(detect_position,'col')#防守
			if(rest_step == 0):
				return
	return#目前還沒有危險|已經防守
def find_row(row,col):#如果有單活4觸發detect
	global rest_step
	row_top = row#須判斷的直線最上
	row_bottom = row#須判斷的直線最下
	for i in range(5):
		if (not row_top-1 < 0 and not board[row_top-1][col] == 'X'):
			row_top-=1
		else:
			break
	for i in range(5):
		if (not row_bottom+1 > 18 and not board[row_bottom+1][col] == 'X'):
			row_bottom+=1
		else:
			break
	if (row_bottom - row_top < 5):
		return#不可能讓對方連6子
	print("find row:"+str(row_top)+"~"+str(row_bottom))
	for row_top in range(row_top,row_bottom-4):
		biggest_top = row_top#最大相連數的左
		biggest_bottom = row_top#最大相連數的右
		tmp_biggest_top = row_top
		tmp_biggest_bottom = row_top
		total_count = 0
		for row_i in range(row_top,row_top+6):
			if (board[row_i][col] == 'O'):
				total_count+=1
				tmp_biggest_bottom+=1
			elif(board[row_i][col] == '.'):#'.'
				if (tmp_biggest_bottom - tmp_biggest_top > biggest_bottom - biggest_top +1):
					biggest_top = tmp_biggest_top
					biggest_bottom = tmp_biggest_bottom-1
				tmp_biggest_top = row_i+1
				tmp_biggest_bottom = row_i+1
			elif(board[row_i][col] == 'X'):
				break
		if (tmp_biggest_bottom - tmp_biggest_top > biggest_bottom - biggest_top +1):
			biggest_top = tmp_biggest_top
			biggest_bottom = tmp_biggest_bottom-1
		if (total_count >= 4):#有單活4detect
			middle = row_top+2.5
			detect_position = [biggest_top,biggest_bottom,col,middle]
			detect(detect_position,'row')#防守
			if(rest_step == 0):
				return
	return#目前還沒有危險|已經防守	
def find_slash(row,col,mod):#如果有單活4觸發detect
	global rest_step
	row_top = row
	row_bottom = row
	col_left = col
	col_right = col
	for i in range(5):
		if (mod == 'back'):
			if (not row_top-1 < 0 and not col_left-1 < 0 and not board[row_top-1][col_left-1] == 'X'):
				row_top-=1
				col_left-=1
			else:
				break
		elif (mod == 'normal'):
			if (not row_top-1 < 0 and not col_right+1 > 18 and not board[row_top-1][col_right+1] == 'X'):
				row_top-=1
				col_right+=1
			else:
				break
	for i in range(5):
		if (mod == 'back'):
			if (not row_bottom+1 > 18 and not col_right+1 > 18 and not board[row_bottom+1][col_right+1] == 'X'):
				row_bottom+=1
				col_right+=1
			else:
				break
		elif (mod == 'normal'):
			if (not row_bottom+1 > 18 and not col_left-1 < 0 and not board[row_bottom+1][col_left-1] == 'X'):
				row_bottom+=1
				col_left-=1
			else:
				break
	if (row_bottom - row_top < 5):
		print('不可能')
		return#不可能讓對方連6子
	if(mod == 'normal'):
		print("find slash:("+str(col_right)+","+str(row_top)+")~("+str(col_left)+","+str(row_bottom)+")")
	if(mod == 'back'):
		print("find backslash:("+str(col_left)+","+str(row_top)+")~("+str(col_right)+","+str(row_bottom)+")")
	if(mod == 'back'):
		for row_top in range(row_top,row_bottom-4):
			biggest_top = row_top#最大相連數的左
			biggest_bottom = row_top#最大相連數的右
			biggest_left = col_left
			biggest_right = col_left
			tmp_biggest_top = row_top
			tmp_biggest_bottom = row_top
			tmp_biggest_left = col_left
			tmp_biggest_right = col_left
			total_count = 0
			for i in range(6):
				if (board[row_top+i][col_left+i] == 'O'):
					total_count+=1
					tmp_biggest_bottom+=1
					tmp_biggest_right+=1
				elif(board[row_top+i][col_left+i] == '.'):#'.'
					if (tmp_biggest_bottom - tmp_biggest_top > biggest_bottom - biggest_top +1):
						biggest_top = tmp_biggest_top
						biggest_bottom = tmp_biggest_bottom-1
						biggest_left = tmp_biggest_left
						biggest_right = tmp_biggest_right-1
					tmp_biggest_top = row_top+i+1
					tmp_biggest_bottom = row_top+i+1
					tmp_biggest_left = col_left+i+1
					tmp_biggest_right = col_left+i+1
				elif(board[row_top+i][col_left+i] == 'X'):
					break
			if (tmp_biggest_bottom - tmp_biggest_top > biggest_bottom - biggest_top +1):
				biggest_top = tmp_biggest_top
				biggest_bottom = tmp_biggest_bottom-1
				biggest_left = tmp_biggest_left
				biggest_right = tmp_biggest_right-1
			if (total_count >= 4):#有單活4detect
				middle_row = row_top+2.5
				middle_col = col_left+2.5
				detect_position = [biggest_top,biggest_left,biggest_bottom,biggest_right,middle_row,middle_col]
				detect(detect_position,'back')#防守
				if(rest_step == 0):
					return
			col_left+=1
	elif(mod == 'normal'):
		for row_top in range(row_top,row_bottom-4):
			biggest_top = row_top#最大相連數的左
			biggest_bottom = row_top#最大相連數的右
			biggest_left = col_right
			biggest_right = col_right
			tmp_biggest_top = row_top
			tmp_biggest_bottom = row_top
			tmp_biggest_left = col_right
			tmp_biggest_right = col_right
			total_count = 0
			for i in range(6):
				if (board[row_top+i][col_right-i] == 'O'):
					total_count+=1
					tmp_biggest_bottom+=1
					tmp_biggest_left-=1
				elif(board[row_top+i][col_right-i] == '.'):#'.'
					if (tmp_biggest_bottom - tmp_biggest_top > biggest_bottom - biggest_top +1):
						biggest_top = tmp_biggest_top
						biggest_bottom = tmp_biggest_bottom-1
						biggest_right = tmp_biggest_right
						biggest_left = tmp_biggest_left+1
					tmp_biggest_top = row_top+i+1
					tmp_biggest_bottom = row_top+i+1
					tmp_biggest_left = col_right-i-1
					tmp_biggest_right = col_right-i-1
				elif(board[row_top+i][col_right-i] == 'X'):
					break
			if (tmp_biggest_bottom - tmp_biggest_top > biggest_bottom - biggest_top +1):
				biggest_top = tmp_biggest_top
				biggest_bottom = tmp_biggest_bottom-1
				biggest_right = tmp_biggest_right
				biggest_left = tmp_biggest_left+1
			if (total_count >= 4):#有單活4detect
				middle_row = row_top+2.5
				middle_col = col_right-2.5
				detect_position = [biggest_top,biggest_right,biggest_bottom,biggest_left,middle_row,middle_col]
				detect(detect_position,'normal')#防守
				if(rest_step == 0):
					return
			col_right-=1
	return#目前還沒有危險|已經防守	
def contain_live_four():
	global opponent
	global rest_step
	#橫
	if(rest_step == 0):
		return
	if (board[opponent[0][0]].count('O')>=4):
		print("call find col"+"("+str(opponent[0][0])+","+str(opponent[0][1])+")")
		find_col(opponent[0][0],opponent[0][1])
	if(rest_step == 0):
		return
	if (board[opponent[1][0]].count('O')>=4):
		print("call find col"+"("+str(opponent[1][0])+","+str(opponent[1][1])+")")
		find_col(opponent[1][0],opponent[1][1])
	#直
	if(rest_step == 0):
		return
	count = 0
	for i in range(19):
		if (board[i][opponent[0][1]] == 'O'):
			count+=1
			if (count>=4):
				print("call find row"+"("+str(opponent[0][0])+","+str(opponent[0][1])+")")
				find_row(opponent[0][0],opponent[0][1])
	if(rest_step == 0):
		return
	count = 0
	for i in range(19):
		if (board[i][opponent[1][1]] == 'O'):
			count+=1
			if (count>=4):
				print("call find row"+"("+str(opponent[1][0])+","+str(opponent[1][1])+")")
				find_row(opponent[1][0],opponent[1][1])
	if(rest_step == 0):
		return
	#slash
	row_i = opponent[0][0]
	col_i = opponent[0][1]
	count = 0
	while True:#左下
		if(col_i < 0 or row_i > 18):
			break
		if(board[row_i][col_i] == 'O'):
			count+=1
		col_i-=1
		row_i+=1
	row_i = opponent[0][0]-1
	col_i = opponent[0][1]+1
	while True:#右上
		if(col_i > 18 or row_i < 0):
			break
		if(board[row_i][col_i] == 'O'):
			count+=1
		col_i+=1
		row_i-=1
		if(count >= 4):
			print("call find slash"+"("+str(opponent[0][0])+","+str(opponent[0][1])+")")
			find_slash(opponent[0][0],opponent[0][1],'normal')
			break
	if(rest_step == 0):
		return
	row_i = opponent[1][0]
	col_i = opponent[1][1]
	count = 0
	while True:#左下
		if(col_i < 0 or row_i > 18):
			break
		if(board[row_i][col_i] == 'O'):
			count+=1
		col_i-=1
		row_i+=1
	row_i = opponent[1][0]-1
	col_i = opponent[1][1]+1
	while True:#右上
		if(col_i > 18 or row_i < 0):
			break
		if(board[row_i][col_i] == 'O'):
			count+=1
		col_i+=1
		row_i-=1
		if(count >= 4):
			print("call find slash"+"("+str(opponent[1][0])+","+str(opponent[1][1])+")")
			find_slash(opponent[1][0],opponent[1][1],'normal')
			break
	if(rest_step == 0):
		return
	#backslash
	row_i = opponent[0][0]
	col_i = opponent[0][1]
	count = 0
	while True:#右下
		if(col_i > 18 or row_i > 18):
			break
		if(board[row_i][col_i] == 'O'):
			count+=1
		col_i+=1
		row_i+=1
	row_i = opponent[0][0]-1
	col_i = opponent[0][1]-1
	while True:#左上
		if(col_i < 0 or row_i < 0):
			break
		if(board[row_i][col_i] == 'O'):
			count+=1
		col_i-=1
		row_i-=1
		if(count >= 4):
			print("call find backslash"+"("+str(opponent[0][0])+","+str(opponent[0][1])+")")
			find_slash(opponent[0][0],opponent[0][1],'back')
			break
	if(rest_step == 0):
		return
	row_i = opponent[1][0]
	col_i = opponent[1][1]
	count = 0
	while True:#右下
		if(col_i > 18 or row_i > 18):
			break
		if(board[row_i][col_i] == 'O'):
			count+=1
		col_i+=1
		row_i+=1
	row_i = opponent[1][0]-1
	col_i = opponent[1][1]-1
	while True:#左上
		if(col_i < 0 or row_i < 0):
			break
		if(board[row_i][col_i] == 'O'):
			count+=1
		col_i-=1
		row_i-=1
		if(count >= 4):
			print("call find backslash"+"("+str(opponent[1][0])+","+str(opponent[1][1])+")")
			find_slash(opponent[1][0],opponent[1][1],'back')
			break
	return
def utility():
	weight=0
	dict={}
	col=0
	row=0
	while(row<=18):
		while(col<=18):
			if board_weight[row][col]>weight:
				weight=board_weight[row][col]
				try:
					dict[weight]=[row,col]
				except KeyError:
					dict[weight]=[row,col]
			col+=1
		row+=1
		col=0
	# if weight==0:
		# dict[weight]=[9,9]
	return dict[weight]
	
#更新攻擊權重 
def update_attack_weight(row,col):
	board_weight[row][col]=0
	#計算橫向權重
	#-----------------------------------------------------------------------------
	sum=0
	End=False
	#相連棋子數
	count=1
	color='X'
	col1=col
	col2=col
	leftc=col
	rightc=col
	blank_right=0
	blank_left=0
	# 0:沒被擋 1:被擋1邊 2:被擋2邊 x|o....o.x 
	check_block=0
	#找左右
	try:
		while (rightc<=18 and rightc-col<6):    
			if board[row][rightc]=='O':
				check_block+=1
				break
			else:
				rightc+=1
		while (leftc>=0 and col-leftc<6): 
			if board[row][leftc]=='O':
				check_block+=1
				break
			else:
				leftc-=1
		#print('check_block',check_block,'rightc',rightc,'leftc',leftc)
		#有贏的機會 非死路    下這只後連的數量+ (6-剩幾只達成連六)=分散的部分  oo o..    ooO o   |o.oo.oO.o.oo|xooo     oo o
		if rightc-leftc>6:
			if (leftc==-1 or rightc==19) and rightc-leftc<9:
				check_block+=1
			#檢查連著
			#檢查右橫
			while(col1<rightc-1):
				
				if board[row][col1+1]==color:
					count+=1
				else:
					break
				col1+=1
			#檢查左橫
			while(col2>leftc+1):
				
				if board[row][col2-1]==color:
					count+=1
				else:
					break
				col2-=1
			
			#先加連的數量
			sum=(count)*2-check_block
			if count==3:
				sum+=count
			if count==4 or count==5:
				sum+=count*2
			if count==6:
				sum+=count*3
			count_right=count
			count_left=count
			#weight.append(count)
			switch=0
			#往左左或往右(分散的部分) 6-剩幾只達成連六 count:目前多少+假設
			#print('col1',col1,'col2',col2)
			while(1):
				#吃到下一個空白就換邊找:找最佳化
				#右col1
		
				while(1):
					if (board[row][col1]=='.' and count_right>count) or count_right==6:
						break
					elif col1==rightc-1:
						if board[row][col1]=='X':
							count_right+=1
						if board[row][col1]=='.' and (count_right==5 or count_left==5):
							count_right+=1
							blank_right+=1
						break	
					else:
						count_right+=1
						
						if board[row][col1]=='.':
							blank_right+=1
						col1+=1
				#左col2
				while(1):
					if (board[row][col2]=='.' and count_left>count) or count_left==6:
					
						break
					elif col2==leftc+1:
						if board[row][col2]=='X':
							count_left+=1
						if board[row][col2]=='.' and (count_right==5 or count_left==5):
							blank_left+=1
							count_left+=1
						break	
					else:
						count_left+=1
						
						if board[row][col2]=='.':
							blank_left+=1
						col2-=1
				#print('col1',col1,'col2',col2)
				#print('count',count,'count_right',count_right,'blank_right',blank_right,'count_left',count_left,'blank_left',blank_left)

				#到底是右好還是左好? count_right-count:到底移動多少格
				
				#if same, have to make progress
				if count_right-blank_right==count_left-blank_left:
					if (count_right==6 or count_left==6):
						sum+=count_left-count-blank_left
						board_weight[row][col]+=sum
						break
					elif count_right>count_left:
						sum+=count_right-count-blank_right
						col2+=count_left-count
						count=count_right
						count_left=count
					else:
						sum+=count_left-count-blank_left
						col1-=count_right-count
						count=count_left
						count_right=count
				#右好，左邊回歸
				elif count_right-blank_right>count_left-blank_left:
					sum+=count_right-count-blank_right
					col2+=count_left-count
					count=count_right
					count_left=count
					#print('right sum',sum)
					
				else:
					sum+=count_left-count-blank_left
					col1-=count_right-count
					count=count_left
					count_right=count
				blank_left=0
				blank_right=0
				if count==6:
					board_weight[row][col]+=sum
					break
				#print('after:','col1',col1,'col2',col2)
				#print('after: count',count,'count_right',count_right,'blank_right',blank_right,'count_left',count_left,'blank_left',blank_left)
				#print('sum',sum)
		else:
			board_weight[row][col]+=0
	except KeyboardInterrupt:
		print('update col wrong:',row,col)
	#print('board_weight',board_weight[row][col])
	#計算垂直權重
	#---------------------------------------------------------------------------
	sum=0
	End=False
	#相連棋子數
	count=1
	color='X'
	row1=row
	row2=row
	leftr=row
	rightr=row
	blank_right=0
	blank_left=0
	# 0:沒被擋 1:被擋1邊 2:被擋2邊 x|o....o.x 
	check_block=0
	#找左右
	try:
		while (rightr<=18 and rightr-row<6):    
			if board[rightr][col]=='O':
				check_block+=1
				break
			else:
				rightr+=1
		while (leftr>=0 and row-leftr<6): 
			#print(leftr)
			if board[leftr][col]=='O':
				check_block+=1
				break
			else:
				leftr-=1
		
		#print('check_block',check_block,'rightr',rightr,'leftr',leftr)
		#有贏的機會 非死路    下這只後連的數量+ (6-剩幾只達成連六)=全部  oo o..    ooO o   |o.oo.oO.o.oo|xooo     oo o
		if rightr-leftr>6:
			if (leftr==-1 or rightr==19)or rightr-leftr<9:
				check_block+=1
			#檢查連著
			#檢查右橫
			while(row1<rightr-1):
				
				if board[row1+1][col]==color:
					count+=1
				else:
					break
				row1+=1
			#檢查左橫
			while(row2>leftr+1):
				
				if board[row2-1][col]==color:
					count+=1
				else:
					break
				row2-=1
			#先加連的數量
			sum=(count)*2-check_block
			if count==3:
				sum+=count
			if count==4 or count==5:
				sum+=count*2
			if count==6:
				sum+=count*3
			count_right=count
			count_left=count
			#print('count',count,'count_right',count_right,'count_left',count_left)
			#weight.append(count)
			switch=0
			#往左左或往右(分散的部分) 6-剩幾只達成連六 count:目前多少+假設
			#print('row1',row1,'row2',row2)
			while(1):
				#吃到下一個空白就換邊找:找最佳化
				#右col1
		
				while(1):
					if (board[row1][col]=='.' and count_right>count) or count_right==6 :
						break
					elif row1==rightr-1:
						if board[row1][col]=='X':
							count_right+=1
						if board[row1][col]=='.' and (count_right==5 or count_left==5):
							count_right+=1
							blank_right+=1
						break
					else:
						count_right+=1
						
						if board[row1][col]=='.':
							blank_right+=1
						row1+=1
				#左col2
				while(1):
					if (board[row2][col]=='.' and count_left>count) or count_left==6 :
						break
					elif row2==leftr+1:
						if board[row2][col]=='X':
							count_left+=1
						if board[row2][col]=='.'and (count_right==5 or count_left==5):
							count_left+=1
							blank_left+=1
						break
					else:
						count_left+=1
						if board[row2][col]=='.':
							blank_left+=1
						row2-=1
				#print('row1',row1,'row2',row2)
				#print('count',count,'count_right',count_right,'blank_right',blank_right,'count_left',count_left,'blank_left',blank_left)

				#到底是右好還是左好? count_right-count:到底移動多少格
				
				#if same, have to make progress
				if count_right-blank_right==count_left-blank_left:
					if (count_right==6 or count_left==6):
						sum+=count_left-count-blank_left
						board_weight[row][col]+=sum
						break
					elif count_right>count_left:
						sum+=count_right-count-blank_right
						row2+=count_left-count
						count=count_right
						count_left=count
					else:
						sum+=count_left-count-blank_left
						row1-=count_right-count
						count=count_left
						count_right=count
				#右好，左邊回歸
				elif count_right-blank_right>count_left-blank_left:
					sum+=count_right-count-blank_right
					row2+=count_left-count
					count=count_right
					count_left=count
					#print('right sum',sum)
					
				else:
					sum+=count_left-count-blank_left
					row1-=count_right-count
					count=count_left
					count_right=count
				blank_left=0
				blank_right=0
				if count==6:
					board_weight[row][col]+=sum
					break
				#print('after:','row1',row1,'row2',row2)
				#print('after: count',count,'count_right',count_right,'blank_right',blank_right,'count_left',count_left,'blank_left',blank_left)
				#print('sum',sum)
		else:
			board_weight[row][col]+=0
	except KeyboardInterrupt:
		print('update row wrong',row,col)
	#print('board_weight',board_weight[row][col])
	#計算左上右下斜權重
	#---------------------------------------------------------------------------
	weight=[]
	sum=0
	End=False
	#相連棋子數
	count=1
	color='X'
	blank_right=0
	blank_left=0
	# 0:沒被擋 1:被擋1邊 2:被擋2邊 x|o....o.x 
	check_block=0
	try:
		if col>row:
			col2=row
			col1=col-row
			row1=0
		else:
			col2=col
			row1=row-col
			col1=0	
		while(1):
			if col1<=18 and row1<=18:
				weight.append(board[row1][col1])
				col1+=1
				row1+=1
			else:
				break
		size=len(weight)-1
		fake_col=col2
		col1=col2
		leftc=col2
		rightc=col2
		#print('board_weight',board_weight[row][col])
		#print('weight',weight,len(weight))
		#print('fake_col',fake_col)
		#找左右
		while (rightc<=size and rightc-fake_col<6):    
			if weight[rightc]=='O':
				check_block+=1
				break
			else:
				rightc+=1
		while (leftc>=0 and fake_col-leftc<6): 
			if weight[leftc]=='O':
				check_block+=1
				break
			else:
				leftc-=1
		
		#print('check_block',check_block,'rightc',rightc,'leftc',leftc)
		#有贏的機會 非死路    下這只後連的數量+ (6-剩幾只達成連六)=分散的部分  oo o..    ooO o   |o.oo.oO.o.oo|xooo     oo o
		if rightc-leftc>6:
			if (leftc==-1 or rightc==size+1) and rightc-leftc<9:
				check_block+=1
			#檢查連著
			#檢查右橫
			while(col1<rightc-1):
				
				if weight[col1+1]==color:
					count+=1
				else:
					break
				col1+=1
			#檢查左橫
			while(col2>leftc+1):
				
				if weight[col2-1]==color:
					count+=1
				else:
					break
				col2-=1
			#先加連的數量
			sum=(count)*2-check_block
			if count==3:
				sum+=count
			if count==4 or count==5:
				sum+=count*2
			if count==6:
				sum+=count*3
			count_right=count
			count_left=count
			#往左左或往右(分散的部分) 6-剩幾只達成連六 count:目前多少+假設
			#print('col1',col1,'col2',col2,'count',count,'check_block',check_block)
			while(1):
				#吃到下一個空白就換邊找:找最佳化
				#右col1
		
				while(1):
					if (weight[col1]=='.' and count_right>count) or count_right==6:
						break
					elif col1==rightc-1:
						if weight[col1]=='X':
							count_right+=1
						if weight[col1]=='.' and (count_right==5 or count_left==5):
							count_right+=1
							blank_right+=1
						break
					else:
						count_right+=1
						
						if weight[col1]=='.':
							blank_right+=1
						col1+=1
				#左col2
				while(1):
					if (weight[col2]=='.' and count_left>count) or count_left==6 :
						break
					elif col2==leftc+1:
						if weight[col2]=='X':
							count_left+=1
						if weight[col2]=='.'and (count_right==5 or count_left==5):
							count_left+=1
							blank_left+=1
						break
					else:
						count_left+=1
						
						if weight[col2]=='.':
							blank_left+=1
						col2-=1
				#print('col1',col1,'col2',col2)
				#print('count',count,'count_right',count_right,'blank_right',blank_right,'count_left',count_left,'blank_left',blank_left)

				#到底是右好還是左好? count_right-count:到底移動多少格
				#if same, have to make progress
				if count_right-blank_right==count_left-blank_left:
					if (count_right==6 or count_left==6):
						sum+=count_left-count-blank_left
						board_weight[row][col]+=sum
						break
					elif count_right>count_left:
						sum+=count_right-count-blank_right
						col2+=count_left-count
						count=count_right
						count_left=count
					else:
						sum+=count_left-count-blank_left
						col1-=count_right-count
						count=count_left
						count_right=count
				#右好，左邊回歸
				elif count_right-blank_right>count_left-blank_left:
					sum+=count_right-count-blank_right
					col2+=count_left-count
					count=count_right
					count_left=count
					#print('right sum',sum)
					
				else:
					sum+=count_left-count-blank_left
					col1-=count_right-count
					count=count_left
					count_right=count
				blank_left=0
				blank_right=0
				if count==6:
					board_weight[row][col]+=sum
					break
				# print('after:','col1',col1,'col2',col2)
				# print('after: count',count,'count_right',count_right,'blank_right',blank_right,'count_left',count_left,'blank_left',blank_left)
				# print('sum',sum)
		else:
			board_weight[row][col]+=0
	except KeyboardInterrupt:
		print('update diagonal (左上右下) wrong',row,col)
	#計算左下右上斜權重
	#---------------------------------------------------------------------------
	#print(show_board())
	weight=[]
	sum=0
	End=False
	#相連棋子數
	count=1
	color='X'
	col1=col
	row1=row
	blank_right=0
	blank_left=0
	# 0:沒被擋 1:被擋1邊 2:被擋2邊 x|o....o.x 
	check_block=0
	try:
		while(1):
			if col1<=18 and row1<=18:
				weight.append(board[row1][col1])
				col1-=1
				row1+=1
			else:
				break
		weight.reverse()
		fake_col=len(weight)-1
		col1=col+1
		row1=row-1
		while(1):
			if col1<=18 and row1<=18:
				weight.append(board[row1][col1])
				col1+=1
				row1-=1
			else:
				break
		size=len(weight)
		col1=fake_col
		col2=fake_col
		leftc=fake_col
		rightc=fake_col
		#print('board_weight',board_weight[row][col])
		# print('weight',weight,len(weight))
		# print('fake_col',fake_col)
		#找左右
		while (rightc<=size-1 and rightc-fake_col<6):    
			if weight[rightc]=='O':
				check_block+=1
				break
			else:
				rightc+=1
		while (leftc>=0 and fake_col-leftc<6): 
			if weight[leftc]=='O':
				check_block+=1
				break
			else:
				leftc-=1
		
		#print('check_block',check_block,'rightc',rightc,'leftc',leftc)
		#有贏的機會 非死路    下這只後連的數量+ (6-剩幾只達成連六)=分散的部分  oo o..    ooO o   |o.oo.oO.o.oo|xooo     oo o
		if rightc-leftc>6:
			if (leftc==-1 or rightc==size) and rightc-leftc<9:
				check_block+=1
			#檢查連著
			#檢查右橫
			while(col1<rightc-1):
				
				if weight[col1+1]==color:
					count+=1
				else:
					break
				col1+=1
			#檢查左橫
			while(col2>leftc+1):
				
				if weight[col2-1]==color:
					count+=1
				else:
					break
				col2-=1
			#先加連的數量
			sum=(count)*2-check_block
			if count==3:
				sum+=count
			if count==4 or count==5:
				sum+=count*2
			if count==6:
				sum+=count*3
			count_right=count
			count_left=count
			#往左左或往右(分散的部分) 6-剩幾只達成連六 count:目前多少+假設
			#print('col1',col1,'col2',col2,'count',count,'check_block',check_block)
			while(1):
				#吃到下一個空白就換邊找:找最佳化
				#右col1
		
				while(1):
					if (weight[col1]=='.' and count_right>count) or count_right==6 :
						break
					elif col1==rightc-1:
						if weight[col1]=='X':
							count_right+=1
						if weight[col1]=='.' and (count_right==5 or count_left==5):
							count_right+=1
							blank_right+=1
						break
					else:
						count_right+=1
						
						if weight[col1]=='.':
							blank_right+=1
						col1+=1
				#左col2
				while(1):
					if (weight[col2]=='.' and count_left>count) or count_left==6 :
						break
					elif col2==leftc+1:
						if weight[col2]=='X':
							count_left+=1
						if weight[col2]=='.' and (count_right==5 or count_left==5):
							count_left+=1
							blank_left+=1
						break
					else:
						count_left+=1
						
						if weight[col2]=='.':
							blank_left+=1
						col2-=1
				#print('col1',col1,'col2',col2)
				#print('count',count,'count_right',count_right,'blank_right',blank_right,'count_left',count_left,'blank_left',blank_left)

				#到底是右好還是左好? count_right-count:到底移動多少格
				#if same, have to make progress
				if count_right-blank_right==count_left-blank_left:
					if (count_right==6 or count_left==6):
						sum+=count_left-count-blank_left
						board_weight[row][col]+=sum
						break
					elif count_right>count_left:
						sum+=count_right-count-blank_right
						col2+=count_left-count
						count=count_right
						count_left=count
					else:
						sum+=count_left-count-blank_left
						col1-=count_right-count
						count=count_left
						count_right=count
				#右好，左邊回歸
				elif count_right-blank_right>count_left-blank_left:
					sum+=count_right-count-blank_right
					col2+=count_left-count
					count=count_right
					count_left=count
					#print('right sum',sum)
					
				else:
					sum+=count_left-count-blank_left
					col1-=count_right-count
					count=count_left
					count_right=count
				blank_left=0
				blank_right=0
				if count==6:
					board_weight[row][col]+=sum
					break
				# print('after:','col1',col1,'col2',col2)
				# print('after: count',count,'count_right',count_right,'blank_right',blank_right,'count_left',count_left,'blank_left',blank_left)
				# print('sum',sum)
		else:
			board_weight[row][col]+=0
	except KeyboardInterrupt:
		print('update diagonal (左下右上斜) wrong',row,col)
	#防守位置
def attack_direct():
	for i in range(19):
		if (board[i].count('X')>=4):
			print("probably win row:"+str(i))
	for i in range(19):
		count = 0
		for j in range(19):
			if (board[j][i] == 'X'):
				count+=1
				if (count>=4):
					print("probably win col:"+str(i))
	count = 0
	#backslash
	for i in range(14):#左下
		count = 0
		for j in range(14):
			if(i+j>18):
				break
			if(board[i+j][j] == 'X'):
				count+=1
			if(count>=4):
				print("left_down_probably win:"+str(j)+str(i+j))
	for i in range(1,14):#右上
		count = 0
		for j in range(14):
			if(i+j>18):
				break
			if(board[j][i+j] == 'X'):
				count+=1
			if(count>=4):
				print("right_up_probably win:"+str(i+j)+str(j))
	#slash
	for i in range(5,19):#左上
		count = 0
		for j in range(14):
			if(i+j>18):
				break
			if(board[i+j][j] == 'X'):
				count+=1
			if(count>=4):
				print("left_down_probably win:"+str(j)+str(i+j))
	for i in range(1,14):#右下
		count = 0
		for j in range(14):
			if(i+j>18):
				break
			if(board[j][i+j] == 'X'):
				count+=1
			if(count>=4):
				print("right_up_probably win:"+str(i+j)+str(j))
	
def show_board():
	print('   ',end='')
	for i in range(19):
		print('%2d' % (i),end=' ')
	print()
	for i in range(len(board)):
		print('%2d' % (i),end=' ')
		for j in range(len(board[i])):
			print ('%2s' %(board[i][j]),end=' ')
		print()
def improve_first_step():
	for i in range(len(board)):
		for j in range(len(board[i])):
			#print(j,end='')
			if board[i][j]=='O':
				#print(i,j)
				if i>0 and j>0:
					board[i-1][j-1]='X'
					board_weight[i-1][j-1]=-10
					print("AI put:",i-1,j-1)
					find_step(i-1,j-1)
					show_board()
				else:
					AI(1)
	for i in range(len(board_weight)):
				#print('%2d' % (i),end=' ')
		for j in range(len(board_weight[i])):
			print ('%2s' %(board_weight[i][j]),end=' ')
		print()
#玩家下固定白子( O )
def player(s):
	global opponent
	print("玩家第", step , '-',s+1, "步：")
	print("輸入要下位置:")
	y=int(input("y:"))
	x=int(input("x:"))
	while (int(x)<0 or int(x)>18 or int(y)<0 or int(y)>18 or not CheckIsDot(board[int(y)][int(x)])):
		print("錯誤位置")
		print("輸入要下位置:")
		y=int(input("y:"))
		x=int(input("x:"))
	board[int(y)][int(x)]='O'
	show_board()
	board_weight[int(y)][int(x)]=-10
	#尋找所有須更新權重的點
	find_step(y,x)
	opponent[s] = [int(y),int(x)]
	if(check_finish(int(y),int(x))):
		print("玩家勝利")
		return True
	return False
#機器下固定黑子( X )
def AI(s):
	#根據權重值判斷要下位置
	global rest_step
	rest_step = s
	#attack_direct()
	contain_live_four()
	if (rest_step > 0):
		for i in range(rest_step):
			point=utility()
			print('weight',board_weight[point[0]][point[1]])
			if board[point[0]][point[1]]!='.':
				print("AI wrong",point[0],point[1])
			else:
				board[point[0]][point[1]]='X'
				board_weight[point[0]][point[1]]=-10
				print("AI put: ",point[0],',',point[1])
			if(check_finish(point[0],point[1])):
				show_board()
				print("AI勝利")
				return True
			#尋找所有須更新權重的點
			
			
			for i in range(len(board_weight)):
				#print('%2d' % (i),end=' ')
				for j in range(len(board_weight[i])):
					print ('%2s' %(board_weight[i][j]),end=' ')
				print()

			find_step(point[1],point[0])
	return False
def start(mod):
	global step	
	while(1):
		#玩家下第一步
		if mod == 1:	
			show_board()
			is_finish=player(0)
			if is_finish:
				break
			if step !=1:
				is_finish=player(1)
				if is_finish:
					break
			if step==1:
				#改良偏遠問題
				improve_first_step()
				is_finish=AI(1)
			else:
				is_finish=AI(2)
			if is_finish:
				break
			step+=1
		#機器下第一步		
		else:
			if step==1:
				draw(9,9)
			else:
				is_finish=AI(2)
				if is_finish:
					break
			show_board()
			is_finish=player(0)
			if is_finish:
				break
			is_finish=player(1)
			if is_finish:
				break
			step+=1
			
def main(range=19):
	init(range)
	while(1):
		print("請輸入:\n 1:玩家先攻\n 2:機器先攻\n Q:離開")
		mod=input()
		if mod == "1" or mod == "2":
			start(int(mod))
		elif mod == "Q":
			break
		else:
			print("請輸入正確數字")
		break
if __name__=="__main__":
	#main(sys.argv[1])
	main()

