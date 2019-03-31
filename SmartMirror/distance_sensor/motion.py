import RPi.GPIO as GPIO
import time


def average_distance(TRIGGER_PIN, ECHO_PIN):
    '''Measure distance 5 times and return average'''
    distance = 0
    for i in range(5):
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
      # add all measured distances together
      distance += (t_elapsed * 34300)/2

      time.sleep(0.1)
    # return average
    distance = distance/5
    return distance


def motion(TRIGGER_PIN, ECHO_PIN, ave_distance):
    '''Report any severe deviation of ave_distance
    RETURN    bool, if a 'motion' is detected'''

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
    distance = (t_elapsed * 34300)/2

    if abs(distance - ave_distance) > 4:
      return True
    else:
      return False


def setup(GPIO_TRIGGER, GPIO_ECHO):
    # set pin notation (BOARD/BCM)
    GPIO.setmode(GPIO.BOARD)

    # set gpio direction (IN/OUT)
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)


def main():

    # set pin numbers
    GPIO_TRIGGER = 12
    GPIO_ECHO = 18

    setup(GPIO_TRIGGER, GPIO_ECHO)

    ave_distance = average_distance(GPIO_TRIGGER, GPIO_ECHO)
    print(ave_distance)

    try:
        while True:
            got_ya = motion(GPIO_TRIGGER, GPIO_ECHO, ave_distance)
            if got_ya:
              print('Motion detected: YES')
            else:
              print('Motion detected: NO')
            time.sleep(1)
    # stop by pressing CTRL+C
    except KeyboardInterrupt:
        print('Measurement stopped by user')
        GPIO.cleanup()


if __name__ == '__main__':
    main()
