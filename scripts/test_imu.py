#!/usr/env python3
from smbus2 import SMBus 
import time 
import numpy as np 



GYRO = 0x68
ACCEL = 0x53
reg_gyro_x = 0x1D
ADXL345_POWER_CTL = 0x2D
DATA_FORMAT = 0x31



def twos_comp(val):
    #Compute the 2's complement of int value val
    if (val & (1 << (15))) != 0: 
        val =(-1)*(65535 + 1 - val)       
    return val   

def gyro_cal(msb, lsb,offset) :
    a= (msb*256+lsb)
    a= twos_comp(a)
    a=a-offset

    return a*0.017453293/65.535 

def accel_cal(msb, lsb) :
    #Conversion des données des accelerateurs binaire en float
    # ADC du capteur est en 10 bits on a choisit +/-2g soit 4g de plage de mesure 
    # 4/2^10 = 0.00390625 
    # Obtenir les acceleration en unité SI on multiplie le resultat precedent par 9.81 
    # On obtient la constante de conversion : 0.038320312
    a= (msb*256+lsb)
    a= twos_comp(a)

    return a* 0.038320312

def gyro_offset() :
    tot_x=0
    tot_y=0
    tot_z=0
    for i in range(20) :
        b= bus.read_i2c_block_data(GYRO,0x1D,6)
        print(b)
        tot_x = tot_x + (b[0]*256+b[1])
        tot_y = tot_y + (b[2]*256+b[3])
        tot_z = tot_z + (b[4]*256+b[5])

    #
    tot_x=int(tot_x/20)
    tot_y=int(tot_y/20)
    tot_z=int(tot_z/20)

    #
    tot_x=twos_comp(tot_x)
    tot_y=twos_comp(tot_y)
    tot_z=twos_comp(tot_z)

    print(tot_x)
    print(tot_y)
    print(tot_z)

    return tot_x,tot_y,tot_z

    



# Configuration de l'accelerometre et du gyroscope
bus=SMBus(1) 
time.sleep(0.001)

bus.write_byte_data(GYRO, 0x16, 0x0B)  
time.sleep(0.001)     
    #set accel register data address

bus.write_byte_data(GYRO, 0x18, 0x32)    
    # set accel i2c slave address
time.sleep(0.001)
bus.write_byte_data(GYRO, 0x14, ACCEL)
time.sleep(0.001)

# Reglage du filtre passe bas de la vitesse angulaire
bus.write_byte_data(GYRO, 0x3D, 0x08)

# Pour le demarrage des mesures il faut set le bit 3 dans le registre Power_ctl 
# On peut ecrire 0x08
time.sleep(0.001)
bus.write_byte_data(ACCEL, ADXL345_POWER_CTL, 0x08)
time.sleep(0.001)
bus.write_byte_data(ACCEL, DATA_FORMAT, 0x00); #Write 0x01 for 2G, 0x01 for 4G, 0x0A for 8G,0x0B for 16G
time.sleep(0.001)
bus.write_byte_data(GYRO, 0x3D, 0x28)


offset= gyro_offset()

b=[]
while 1 :
    # Comme le gyro recupere et stock les 3 acceleration de l'accelerometre
    # On peut lire les 3 vitesse angulaire et les 3 axcel en lisant les 12 registre qui sont comme suivit :
    # x_gyro 15-8 bit, x_gyro 7-0,
    # y_gyro 15-8 bit, y_gyro 7-0,
    # z_gyro 15-8 bit, z_gyro 7-0,
    # x_accel 15-8 bit, x_accel 7-0,
    # y_accel 15-8 bit, y_accel 7-0,
    # z_accel 15-8 bit, z_accel 7-0
    b= bus.read_i2c_block_data(GYRO,0x1D,12)
    print(b)
    
    x_gyro = gyro_cal(b[0],b[1],offset[0])
    y_gyro= - gyro_cal(b[2],b[3],offset[1])
    z_gyro= gyro_cal(b[4],b[5],offset[2])

    y_accel= accel_cal(b[7],b[6])
    x_accel= accel_cal(b[9],b[8])
    z_accel= accel_cal(b[11],b[10])

    
    print ('x_gyro = '+ str(x_gyro))
    print ('y_gyro = '+ str(y_gyro))
    print ('z_gyro = '+ str(z_gyro))
    print ('x_accel = '+ str(x_accel))
    print ('y_accel = '+ str(y_accel))
    print ('z_accel = '+ str(z_accel))

    time.sleep(1)
bus.close()