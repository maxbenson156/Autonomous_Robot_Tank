#import imu_sensor
#import i2c_class
import encoders
import encoder_matrix_test as emt
import numpy as np
import time
import datetime
import robot_logging as rl

# define variables
x_0 = 0
y_0 = 0
theta = 0
X = np.array([x_0, y_0])
dt_start = time.time()
dt_end = time.time()
start_time = time.time()
freq = 4
dt = 1/freq # only logging every dt seconds (so log isn't full of repeated info!)
motor_ticks = [0, 0]

date = datetime.datetime.now().strftime("%H-%M-%S-%B-%d-%Y")
path = "sensor_tests/"
file = "motor_ticks_"
extension = ".csv"
file_num = 1
log_file_path = path + file + date + extension
counter = 1

# initiate classes (i2c - LIDAR and Encoders, IMU) - perhaps not in this main script actually... rather in sub-scripts
enc = encoders.encoder_handler()

# arduino = i2c_class.I2C(0x08)
# imu = i2c_class.I2C(0x40)

ticks, ticks_last, ticks_dt = [0, 0], [0, 0], [0, 0]

def get_ticks_dt(ticks, ticks_last):
#	print("TEST: Ticks - {}\t Ticks_Last: {}".format(ticks, ticks_last))
	ticks_dt[0] = ticks[0] - ticks_last[0]
	ticks_dt[1] = ticks[1] - ticks_last[1]
	return ticks_dt


while True:
	if (dt_end - dt_start) >= dt:
		time_at_reading = time.time() - start_time
#		motor_ticks[0] = enc.last_ticks[0] + enc.dt_ticks[0]
		ticks_dt = get_ticks_dt(ticks, ticks_last)
		print("Ticks: {}\tLast Ticks: {}\tDt Ticks: {}".format(ticks, ticks_last, ticks_dt))
#		motor_ticks[1] = enc.last_ticks[1] + enc.dt_ticks[1]
#		print("L: {}\tR: {}".format(enc.dt_ticks[0], enc.dt_ticks[1]))
#		X, theta = emt.return_new_pose(X, theta, enc.dt_ticks[0], enc.dt_ticks[1])
#		print("x: {}\ty: {}\ttheta: {}".format(X[0], X[1], theta))
		rl.log_motor_ticks(log_file_path, time_at_reading, ticks)
#		enc.print_ticks()
#		print("Time: {}s".format(time_at_reading))
		dt_start = time.time()
		ticks_last = ticks
		print("TEST - Last Ticks: {}".format(ticks_last))
		ticks = enc.update()
		print("TEST - Ticks: {}".format(ticks))
	else:
		enc.update()

	dt_end = time.time()

	# compute position from IMU linear acceleration data (and other data e.g. orientation, rotation etc.?) + save values
	# compute optimal estimate for position based on encoders and IMU + save values

