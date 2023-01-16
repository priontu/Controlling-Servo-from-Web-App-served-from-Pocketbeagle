from flask import Flask, render_template, request, redirect, url_for
import Adafruit_BBIO.PWM as PWM

pwm_pin = "P1_8"
servo_state = "OFF"

class servo_drive:
	def __init__(self):
		self.pwm_pin = "P1_8"
		self.servo_state = "OFF"
		self.prev_servo_state = "OFF"

		self.angle = 0

		self.duty_min = 3
		self.duty_max = 14.5

		self.duty_span = self.duty_max - self.duty_min

		PWM.start(self.pwm_pin, (100 - self.duty_min), 60.0, 1)

	
	def trigger_servo(self):
		if self.servo_state != self.prev_servo_state:
			self.prev_servo_state = self.servo_state
			if self.servo_state == "ON":
				print("ON Clicked!")
				self.angle = 180
			elif self.servo_state == "OFF":
				self.angle = 0
				print("OFF Clicked!")
			duty = 100 - (self.angle/180 * self.duty_span + self.duty_min)
			PWM.set_duty_cycle(self.pwm_pin, duty)
		else:
			print("Previous State: ", self.servo_state)


servo = servo_drive()

app = Flask(__name__)
@app.route('/', methods = ['GET', 'POST'])
def index():
	if request.method == 'POST':
		servo.servo_state = request.form.get('option')
		servo.trigger_servo()
		return redirect('/')

	return render_template("index.html", radio_val = servo.servo_state)



if __name__ == '__main__':
	app.run(debug=True, host = "0.0.0.0", port = 5000)
