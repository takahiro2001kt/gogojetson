import sys
import termios
import tty
import MOTOR_CTL
duty = 65

def getch():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return ch

CTL = MOTOR_CTL.MOTOR_CTL()
CTL.set_STBY(1)
CTL.set_direction(0)

try:
	while True:
	    print(CTL.duty)
	    ch = getch()
	    if ch == 'w':
	        print('Forward')
	        #CTL.fin_turn()
	        CTL.set_direction(1)
	        CTL.accORdec("AB",duty,"acc")
	    elif ch == 'x':
	        print('Back')
	        #CTL.fin_turn()
	        CTL.set_direction(2)
	        CTL.accORdec("AB",duty,"acc")
	    elif ch == 'd':
	        print('Right')
	        CTL.turn('r',duty/2)
	    elif ch == 'a':
	        print('Left')
	        CTL.turn('l',duty/2)
	    elif ch == 'f':
	        print('Fin_TURN')
	        CTL.fin_turn()
	    elif ch == 'q':
	        break
	    else:
	        print("stop")
	        #CTL.fin_turn()
	        CTL.accORdec("AB",0,"dec")

finally:
        CTL.close_CTL()
