# Import necessary libraries.
from time import sleep
from math import floor
from Bluetin_Echo import Echo

# Define pin constants
TRIGGER_PIN_1 = 17
ECHO_PIN_1 = 27
TRIGGER_PIN_2 = 23
ECHO_PIN_2 = 24
TRIGGER_PIN_3 = 5
ECHO_PIN_3 = 6
TRIGGER_PIN_4 = 26
ECHO_PIN_4 = 16
TRIGGER_PIN_5 = 20
ECHO_PIN_5 = 21

# Initialise two sensors.
echo = [Echo(TRIGGER_PIN_1, ECHO_PIN_1)
        , Echo(TRIGGER_PIN_2, ECHO_PIN_2)
        , Echo(TRIGGER_PIN_3, ECHO_PIN_3)
        , Echo(TRIGGER_PIN_4, ECHO_PIN_4)
        , Echo(TRIGGER_PIN_5, ECHO_PIN_5)]

def main():
    sleep(0.1)
    result = [0,0,0,0,0]
    for counter in range(1, 12):
        for counter2 in range(0, len(echo)):
            result[counter2] = floor(echo[counter2].read('cm', 3))
            #print('Sensor {} - {} cm'.format(counter2, round(result,2)))
        print(result)

    echo[0].stop()

if __name__ == '__main__':
    main()