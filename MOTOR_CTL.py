import Jetson.GPIO as GPIO
import time

class MOTOR_CTL:
	def __init__(self):
		#GPIO MODE SETUP
		GPIO.setmode(GPIO.BOARD)

		#SET PIN Number
		self.APWM = 32
		self.AIN1 = 15
		self.AIN2 = 16
		self.BPWM = 33
		self.BIN1 = 23
		self.BIN2 = 24
		self.STBY = 18

		#SETUP GPIO PIN
		GPIO.setup(self.APWM, GPIO.OUT)
		GPIO.setup(self.AIN1, GPIO.OUT)
		GPIO.setup(self.AIN2, GPIO.OUT)
		GPIO.setup(self.BPWM, GPIO.OUT)
		GPIO.setup(self.BIN1, GPIO.OUT)
		GPIO.setup(self.BIN2, GPIO.OUT)
		GPIO.setup(self.STBY, GPIO.OUT)
		
		#SETUP PWM
		self.pA = GPIO.PWM(self.APWM, 500)
		self.pB = GPIO.PWM(self.BPWM, 500)
		
		#Create Variable
		self.duty = 0
		self.duty_Atmp = 0
		self.duty_Btmp = 0
		self.acc = 10		#加速度はここで指定
		self.tol = -5		#必要に応じて公差を指定する

	def set_STBY(self, status):	#モータースタンバイ切替メソッド
		if status == 1:
			GPIO.output(self.STBY, GPIO.HIGH)
		else:
			GPIO.output(self.STBY, GPIO.LOW)
			
	def set_direction(self,dir):	#方向指定メソッド
		if dir == 1:	#1前進
			GPIO.output(self.AIN1, 1)
			GPIO.output(self.AIN2, 0)
			GPIO.output(self.BIN1, 1)
			GPIO.output(self.BIN2, 0)
		elif dir == 2:	#2後退
			GPIO.output(self.AIN1, 0)
			GPIO.output(self.AIN2, 1)
			GPIO.output(self.BIN1, 0)
			GPIO.output(self.BIN2, 1)
		elif dir == 3:	#3右超信地旋回
			GPIO.output(self.AIN1, 1)
			GPIO.output(self.AIN2, 0)
			GPIO.output(self.BIN1, 0)
			GPIO.output(self.BIN2, 1)
		elif dir == 4:	#4左超信地旋回
			GPIO.output(self.AIN1, 1)
			GPIO.output(self.AIN2, 0)
			GPIO.output(self.BIN1, 0)
			GPIO.output(self.BIN2, 1)
		else:		#0ブレーキ（停止固定）
			GPIO.output(self.AIN1, 1)
			GPIO.output(self.AIN2, 1)
			GPIO.output(self.BIN1, 1)
			GPIO.output(self.BIN2, 1)

	def accORdec(self, ch, duty, flag):	#加減速メソッド(ch:"A"=左ch,"B"=右ch, "AB"=左右同時, duty:目標デューティ比, flag:"acc"=加速,"dec"=減速)
		if flag=="dec":	#減速処理
			p = self.duty		#pは逐次パワーを表す
			while p >= duty:
				if self.tol<0:
					p_tol=p+self.tol
				else:
					p_tol=p-self.tol
				if p_tol<0: p_tol=0
				if ch=="A":
					if self.tol<0:
						self.pA.start(p_tol)
					else:
						self.pA.start(p)
					self.duty_Atmp = p
				elif ch =="B":
					if self.tol>0:
						self.pB.start(p_tol)
					else:
						self.pB.start(p)
					self.duty_Btmp = p
				else:
					if self.tol>0:
						self.pA.start(p)
						self.pB.start(p_tol)
					elif self.tol<0:
						self.pA.start(p_tol)
						self.pB.start(p)
					else:
						self.pA.start(p)
						self.pB.start(p)
					self.duty,self.duty_Atmp,self.duty_Btmp=p,p,p
				time.sleep(0.1)
				p-=self.acc
			if p<0: p=0
			if ch=="A":
				if self.tol<0:
					self.pA.start(p_tol)
				else:
					self.pA.start(p)
				self.duty_Atmp = duty
			elif ch=="B":
				if self.tol>0:
					self.pB.start(p_tol)
				else:
					self.pB.start(p)
				self.duty_Btmp = duty
			else:
				if self.tol<0:
					self.pA.start(p_tol)
					self.pB.start(p)
				elif self.tol>0:
					self.pA.start(p)
					self.pB.start(p_tol)
				else:
					self.pA.start(p)
					self.pB.start(p)
				self.duty,self.duty_Atmp,self.duty_Btmp=duty,duty,duty
			if self.duty_Atmp <= 10:
				self.pA.stop()
			elif self.duty_Btmp <= 10:
				self.pB.stop()
		else:		#加速処理
			if ch=="A":			#
				p = self.duty_Atmp	#
			elif ch=="B":			#pを新たに現在のパワーに更新
				p = self.duty_Btmp	#
			else:				#
				p = self.duty		#
			while p<=duty:
				if self.tol<0:
					p_tol=p+self.tol
				else:
					p_tol=p-self.tol
				if p_tol<0: p_tol=0
				if ch=="A":
					if self.tol<0:
						self.pA.start(p_tol)
					else:
						self.pA.start(p)
					self.duty_Atmp = p
				elif ch=="B":
					if self.tol>0:
						self.pB.start(p_tol)
					else:
						self.pB.start(p)
					self.duty_Btmp = p
				else:
					#if self.duty_Atmp!=self.duty_Btmp:
					if self.tol<0:
						self.pA.start(p_tol)
						self.pB.start(p)
					elif self.tol>0:
						self.pA.start(p)
						self.pB.start(p_tol)
					else:
						self.pA.start(p)
						self.pB.start(p)
					self.duty,self.duty_Atmp,self.duty_Btmp=p,p,p
				time.sleep(0.1)
				p+=self.acc
			if ch=="A":
				if self.tol<0:
					self.pA.start(duty+self.tol)
				else:
					self.pA.start(duty)
				self.duty_Atmp = duty
			elif ch=="B":
				if self.tol>0:
					self.pB.start(duty-self.tol)
				else:
					self.pB.start(duty)
				self.duty_Btmp = duty
			else:
				if self.tol<0:
					self.pA.start(duty+self.tol)
					self.pB.start(duty)
				elif self.tol>0:
					self.pA.start(duty)
					self.pB.start(duty-self.tol)
				else:
					self.pA.start(duty)
					self.pB.start(duty)
				self.duty,self.duty_Atmp,self.duty_Btmp=duty,duty,duty

	def turn(self, r_or_l, diff):	#旋回メソッド(r_or_l:"r"=右旋回,"l"=左旋回, diff:左右出力差(duty比の差))
		if self.duty_Atmp!=self.duty_Btmp:
			print("先にfin_turnを実行してください。")
			return ""
		#duty_diff = self.duty*diff
		duty_diff = self.duty - diff
		if duty_diff<=0:
			duty_diff=0
		#内側となる側をdiff%減速
		if r_or_l=="r":
			self.accORdec("B",duty_diff,"dec")
		elif r_or_l=="l":
			self.accORdec("A",duty_diff,"dec")
		else:
			pass

	def fin_turn(self):
		self.accORdec("A", self.duty, "acc")
		self.accORdec("B", self.duty, "acc")

	def close_CTL(self):
		print("Deceleratig now...")
		self.fin_turn()
		self.accORdec("AB",0,"dec")
		self.pA.stop()
		self.pB.stop()
		GPIO.cleanup()
		print("Process Complete!")


"""
try:
	CTL = MOTOR_CTL()

	CTL.set_STBY(1)
	CTL.set_direction(1)
	while True:
		CTL.accORdec("AB",100,"acc")

finally:
	#CTRL+Cで停止
	#動作停止
	CTL.close_CTL()
"""
