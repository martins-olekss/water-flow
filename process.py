#Source: https://www.youtube.com/watch?v=wpenAP8gN3c
import RPi.GPIO as GPIO
import time, sys
f = open('FlowData.txt', 'a')

GPIO.setmode(GPIO.BOARD)
input = 13
GPIO.setup(inpt, GPIO.IN)
minutes = 0
constant = 0.006 # need to calibrate
time_new = 0.0
rpt_int = 10

global rate_cnt, tot_cnt
rate_cnt = 0
tot_cnt = 0

def Pulse_cnt(inpt_pin):
    global rate_cnt, tot_cnt
    rate_cnt += 1
    tot_cnt += 1

GPIO.add_event_detect(inpt, GPIO.FALLING, callback = Pulse_cnt, bouncetime = 10)

# Main
print('Water Flow - Approx ', str(time.asctime(time.localtime(time.time()))))
rpt_int = int(input('Input desired report interval in seconds '))
print('Reports every ', rpt_int, ' seconds')
print('Control C to exit')
f.write('\nWater Flox - Approx - Reports every '+ str(rpt_int)+ ' Seconds ' + str(time.asctime(time.localtime(time.time()))))

while True:
    time_new = time.time() + rpt_int
    rate_cnt = 0
    while time.time() <= time_new:
        try:
            None
            print(GPIO.input(inpt), end = '')
        except KeyboardInterrupt:
            print('\nCTRL C - Exiting nicely')
            GPIO.cleanup()
            f.close()
            print('Done')
            sys.exit()
    minutes += 1

    LperM = round(((rate_cnt * constant)/(rpt_int/60)),2)
    TotTLit = rount(tot_cnt * constant, 1)

    # Do bunch of writing and outputing
    f.write('\n1 ' + str(LperM))
    f.write('\n2 ' + str(TotTLit))
    f.write('\ntime ' + str(minutes) + '\t' + str(time.asctime(time.localtime(time.time()))))
    f.flush()

GPIO.cleanup()
f.close()
print('Done')
