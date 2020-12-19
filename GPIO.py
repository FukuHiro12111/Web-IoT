import RPi.GPIO as GPIO
import picamera
import time

gpio_led = 17
gpio_sw = 26

GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_led,GPIO.OUT)
GPIO.setup(gpio_sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)

CAM_DIR = "/home/pi/Web-IoT-/"

camera = picamera.PiCamera()

try:
	while True:
		if GPIO.input(26) == 0:
			filename = ("sample") + ".jpg"
			save_dir_filename = CAM_DIR + filename
			camera.capture(save_dir_filename)
			GPIO.output(gpio_led,1)
			time.sleep(5)
			GPIO.output(gpio_led,0)
except KeyboardInterrupt:
    GPIO.cleanup(gpio_sw)
    GPIO.cleanup(gpio_led)
