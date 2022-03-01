#!/usr/env python3
from smbus2 import SMBus 
import time 
import numpy as npsonar
import rospy
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3

class IMU():

    def __init__(self):
        #Constant
        self.GYRO = 0x68
        self.ACCEL = 0x53
        self.reg_gyro_x = 0x1D
        self.ADXL345_POWER_CTL = 0x2D
        self.DATA_FORMAT = 0x31
        self.bus = SMBus(1)
        time.sleep(1)
        self.b = []
        self.offset = (0,0,0)
        #init ros node
        rospy.init_node("imu_driver")
        self.imu_publisher = rospy.Publisher("imu_data", Imu, queue_size=10)
    #calcul du complement à 2 d'un int
    def twos_comp(self, val):
        if (val & (1 << (15))) != 0: 
            val =(-1)*(65535 + 1 - val)
        return val


    def gyro_cal(self, msb, lsb,offset) :
        a = (msb*256+lsb)
        a = self.twos_comp(a)
        a = a-offset

        return a*0.017453293/65.535

    def accel_cal(self, msb, lsb) :
        #Conversion des données des accelerateurs binaire en float
        # ADC du capteur est en 10 bits on a choisit +/-2g soit 4g de plage de mesure 
        # 4/2^10 = 0.00390625 
        # Obtenir les acceleration en unité SI on multiplie le resultat precedent par 9.81 
        # On obtient la constante de conversion : 0.038320312
        a = (msb*256+lsb)
        a = self.twos_comp(a)

        return a* 0.038320312

    def gyro_offset(self) :
        tot_x = 0
        tot_y = 0
        tot_z = 0
        print("offset")
        iter = 20
        n = 0
        for i in range(iter) :
            try:
                b = self.bus.read_i2c_block_data(self.GYRO, 0x1D, 6)
                time.sleep(1)
                print(b)
                tot_x = tot_x + (b[0]*256+b[1])
                tot_y = tot_y + (b[2]*256+b[3])
                tot_z = tot_z + (b[4]*256+b[5])
                n+=1
            except:
                pass

        #
        tot_x = int(tot_x/n)
        tot_y = int(tot_y/n)
        tot_z = int(tot_z/n)

        #
        tot_x = self.twos_comp(tot_x)
        tot_y = self.twos_comp(tot_y)
        tot_z = self.twos_comp(tot_z)

        print(tot_x)
        print(tot_y)
        print(tot_z)

        return tot_x,tot_y,tot_z

    def setupIMU(self):
        self.bus.write_byte_data(self.GYRO, 0x16, 0x0B)
        time.sleep(0.001)
            #set accel register data address

        self.bus.write_byte_data(self.GYRO, 0x18, 0x32)
            # set accel i2c slave address
        time.sleep(0.001)
        self.bus.write_byte_data(self.GYRO, 0x14, self.ACCEL)
        time.sleep(0.001)

        # Reglage du filtre passe bas de la vitesse angulaire
        self.bus.write_byte_data(self.GYRO, 0x3D, 0x08)

        # Pour le demarrage des mesures il faut set le bit 3 dans le registre Power_ctl 
        # On peut ecrire 0x08
        time.sleep(0.001)
        self.bus.write_byte_data(self.ACCEL, self.ADXL345_POWER_CTL, 0x08)
        time.sleep(0.001)
        self.bus.write_byte_data(self.ACCEL, self.DATA_FORMAT, 0x00) #Write 0x01 for 2G, 0x01 for 4G, 0x0A for 8G,0x0B for 16G
        time.sleep(0.001)
        self.bus.write_byte_data(self.GYRO, 0x3D, 0x28)


        #self.offset = self.gyro_offset()
        
    def busClose(self):
        self.bus.close()

    def runIMU(self):
        # Comme le gyro recupere et stock les 3 acceleration de l'accelerometre
        # On peut lire les 3 vitesse angulaire et les 3 axcel en lisant les 12 registre qui sont comme suivit :
        # x_gyro 15-8 bit, x_gyro 7-0,
        # y_gyro 15-8 bit, y_gyro 7-0,
        # z_gyro 15-8 bit, z_gyro 7-0,
        # x_accel 15-8 bit, x_accel 7-0,
        # y_accel 15-8 bit, y_accel 7-0,
        # z_accel 15-8 bit, z_accel 7-0
        try:
            self.b = self.bus.read_i2c_block_data(self.GYRO, 0x1D, 12)
            
            x_gyro = self.gyro_cal(self.b[0], self.b[1], self.offset[0])
            y_gyro = - self.gyro_cal(self.b[2], self.b[3], self.offset[1])
            z_gyro = self.gyro_cal(self.b[4], self.b[5], self.offset[2])

            x_accel = - self.accel_cal(self.b[7],self.b[6])
            y_accel = - self.accel_cal(self.b[9],self.b[8])
            z_accel = self.accel_cal(self.b[11],self.b[10])

            
            print ('x_gyro = '+ str(x_gyro))
            print ('y_gyro = '+ str(y_gyro))
            print ('z_gyro = '+ str(z_gyro))
            print ('x_accel = '+ str(x_accel))
            print ('y_accel = '+ str(y_accel))
            print ('z_accel = '+ str(z_accel))
            
            message = Imu()
            message.header.stamp = rospy.Time.now()
            message.header.frame_id = "odom"
            message.child_frame_id = "base_link"
            message.linear_acceleration = Vector3(x_accel, y_accel, z_accel)
            message.angular_velocity = Vector3(x_gyro, y_gyro, z_gyro)
            self.imu_publisher.publish(message)
            #attente 1 seconde
        except:
            pass
        time.sleep(0.02)

imu = IMU()
imu.setupIMU()
while 1:
    imu.runIMU()