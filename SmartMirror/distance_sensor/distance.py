import RPi.GPIO as GPIO
import time


def distance(TRIGGER_PIN, ECHO_PIN):
    '''Send a trigger signal with pin @TRIGGER_PIN and receive the echo with
    @ECHO_PIN
    RETURN      distance in centimeter'''
    # set trigger pin to HIGH
    GPIO.output(TRIGGER_PIN, True)

    # set trigger pin after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(TRIGGER_PIN, False)

    t_start = time.time()
    t_stop = time.time()

    # save start time
    while GPIO.input(ECHO_PIN) == 0:
        t_start = time.time()

    # save time of arrival
    while GPIO.input(ECHO_PIN) == 1:
        t_stop = time.time()

    t_elapsed = t_stop - t_start

    # muliply with speed of sound (34300 cm/s)
    # divide by half, because there and back
    return (t_elapsed * 34300)/2


def main():

    # set pin notation (BOARD/BCM)
    GPIO.setmode(GPIO.BOARD)
    
    # set pin numbers
    GPIO_TRIGGER = 12
    GPIO_ECHO = 18
    
    # set gpio direction (IN/OUT)
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)

    try:
        while True:
            dist = distance(GPIO_TRIGGER, GPIO_ECHO)
            print('Measured Distance = {:.1f} cm'.format(dist))
            time.sleep(1)
    # stop by pressing CTRL+C
    except KeyboardInterrupt:
        print('Measurement stopped by user')
        GPIO.cleanup()

if __name__ == '__main__':
    main()
