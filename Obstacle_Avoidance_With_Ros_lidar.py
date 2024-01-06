#!/usr/bin/env python3

import rospy                            # -> Bu ifade, ROS üzerinde çalışmak için gerekli olan rospy modülünü içeri aktarır. rospy modülü, ROS ile Python programlama dili arasında iletişimi sağlar.

from geometry_msgs.msg import Twist     # -> Bu ifade, ROS tarafından tanımlanan Twist mesaj türünü içeri aktarır.

from sensor_msgs.msg import LaserScan   # -> Bu ifade, ROS'un sensor_msgs paketinde tanımlanan LaserScan mesaj türünü içeri aktarır ve lazer tarama sensöründen alınan verileri içerir.

import sys, select, termios, tty        # -> Bu ifadeler, Python'da terminal girişi (klavye girişi) ve terminal kontrolü için kullanılan standart kütüphaneleri içeri aktarır. 

import time                             # -> time modülünü ekledik, çünkü 'time.sleep()' fonksiyonunu kullanıyoruz

# Global Değişken olarak msg değişkenini tanımlıyoruz.
msg = """
          TURTLEBOT3 KONTROL MERKEZİ
*---------------------------------------------*
*                                             *  
* w : TurtleBot3 için Otonom Modu Başlat      *
* s : TurtleBot3' ü Durdur (EMERGENCY)        *
* CTRL-C ile programdan çıkış yapabilirsiniz! *
*                                             *
*---------------------------------------------*

"""

# Global sabitler
# Aracın Doğrusal hızını buradan ayarlayabiliriz.
LINEAR_VEL = 0.25

# Aracın Açısal hızını buradan ayarlayabiliriz.
ANGULAR_VEL = 0.6
    
# Global sabitler
# Aracın sol ön, ön ve sağ ön tarafındaki uzaklıkların değişkenlerin tanımlanması burada yapılmıştır.
laser_FC_ = 0
laser_FL_ = 0
laser_FR_ = 0

# getKey Fonksiyonu, kullanıcının klavyeden bir tuşa basmasını bekleyen ve ardından basılan tuşu döndüren bir fonksiyondur. 
# Bu fonksiyon, genellikle kullanıcıdan girdi almak ve programın çalışma modunu değiştirmek gibi interaktif senaryolarda kullanılır. 
# Örneğin, yukarıdaki kod örneğinde "w" tuşuna basıldığında otonom modu başlatma veya "s" tuşuna basıldığında acil durumu tetikleme gibi durumları kontrol etmek için kullanılmıştır.
def getKey():

    # tty.setraw(sys.stdin.fileno()) -> Bu satır, terminal girişini karakter karakter almak için ayarlar yapar. 
    # Normalde, terminal girişi satır satır okunur, ancak bu ayarla karakter karakter okuma sağlanır.
    tty.setraw(sys.stdin.fileno())

    # rlist, _, _ = select.select([sys.stdin], [], [], LINEAR_VEL): Bu satır, terminal girişini (klavye) dinlemek için select fonksiyonunu kullanır. 
    # LINEAR_VEL süresince bekler ve klavyeden bir tuşa basılıp basılmadığını kontrol eder.
    rlist, _, _ = select.select([sys.stdin], [], [], LINEAR_VEL)

    # if rlist:: Eğer klavyeden bir tuşa basılmışsa, rlist dolu olacaktır ve bu durumda bir sonraki adıma geçilir.
    if rlist:
        # key = sys.stdin.read(1) -> Bu satır, klavyeden bir karakter okur. 1 parametresi, sadece bir karakter okunmasını sağlar.
        key = sys.stdin.read(1)

    # else: key = '' -> Eğer klavyeden bir tuşa basılmamışsa, key değişkenine boş bir karakter dizisi atanır.
    else:
        key = ''

    # termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings) -> Bu satır, terminal ayarlarını başlangıçtaki ayarlara geri döndürür.
    # settings değişkeni, fonksiyonun başında termios.tcgetattr(sys.stdin) ile alınan başlangıç terminal ayarlarını içerir.
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

    # return key -> okunan tuşu döndürür.
    return key

def callback(data):
    global laser_FC_, laser_FL_, laser_FR_
    
    # Ön taraftan gelen lazer tarama verilerini kontrol ediyoruz.
    if data.ranges[0] > data.range_min and data.ranges[0] < data.range_max:
        laser_FC_ = data.ranges[0]

    # Sol ön taraftan 30 derece açı ile gelen lazer tarama verilerini kontrol ediyoruz.
    if data.ranges[30] > data.range_min and data.ranges[30] < data.range_max:
        laser_FL_ = data.ranges[30]

    # Sağ ön taraftan 30 derece açı ile gelen lazer tarama verilerini kontrol ediyoruz.
    if data.ranges[330] > data.range_min and data.ranges[330] < data.range_max:
        laser_FR_ = data.ranges[330]
        
if __name__=="__main__":
    settings = termios.tcgetattr(sys.stdin)

    rospy.init_node('turtlebot3_auto')
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
       
    sub = rospy.Subscriber("/scan", LaserScan, callback, queue_size=10)
    
    state = 0 
    
    status = 0
    
    control_linear_vel = 0
    control_angular_vel = 0
    try:
        print (msg)
        while(1):
            key = getKey()
            if key == 'w' :
                if state != 1:
                    state = 1
                    print("Otonom Mod Başlatılıyor")
                    status = status + 1                 
            elif key == 's' :
                if state != 0:
                    state = 0
                    print("Araç DURDURULDU")
                    status = status + 1
            else:
                if (key == '\x03'):
                    break
                            ## sol ön, ön, sağ ön
            show_sensor = "\n*-----------------------------*\nSol Ön Taraftaki Engele Uzaklık: {:.3f}".format(laser_FL_) + " \n\n" + "Ön Taraftaki Engele Uzaklık: {:.3f}".format(laser_FC_) + " \n\n" + "Sağ Ön Taraftaki Engele Uzaklık: {:.3f}".format(laser_FR_)
            if state == 1 :
                if laser_FC_ > 0.6 and laser_FL_ > 0.4 and laser_FR_ > 0.4:
                    control_linear_vel = LINEAR_VEL
                    control_angular_vel = 0
                    print(show_sensor + "  TurtleBot3 Waffle İleri Gidiyor!")
                    status = status + 1
                    # Burada status değerini 1 arttırıyoruz, çünkü aracın mesaj verme değeri olan 15' e gelmesi için.
                elif laser_FL_ > laser_FR_:
                    control_linear_vel = 0
                    control_angular_vel = ANGULAR_VEL
                    print(show_sensor + "  TurtleBot3 Waffle Sola Dönüyor!")
                    status = status + 1
                    # Burada status değerini 1 arttırıyoruz, çünkü aracın mesaj verme değeri olan 15' e gelmesi için.
                else:
                    control_linear_vel = 0
                    control_angular_vel = -ANGULAR_VEL
                    print(show_sensor + "  TurtleBot3 Waffle Sağa Dönüyor!")
                    status = status + 1 
                    # Burada status değerini 1 arttırıyoruz, çünkü aracın mesaj verme değeri olan 15' e gelmesi için.
            else:
                control_linear_vel = 0
                control_angular_vel = 0
            
            if status >= 15:
                print (msg)
                # Status değeri 15 oldu mesaj ekrana verildi. Şimdi ise status değerini 0 yapıyoruz çünkü tekrar 15 olsun ve ekrana yine aynı mesajı yazdırsın.
                status = 0
            
            twist = Twist()
            twist.linear.x = control_linear_vel; twist.linear.y = 0; twist.linear.z = 0
            twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = control_angular_vel
            pub.publish(twist)

    except Exception as e:
        print (e)

    finally:
        twist = Twist()
        twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
        twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
        pub.publish(twist)
        rospy.sleep(0.3)

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    # Bu fonksiyon, terminal I/O (Input/Output - Giriş/Çıkış) ayarlarını değiştirmek için kullanılan bir termios fonksiyonudur. 
    # Fonksiyon içindeki parametrelerin açıklamaları şu şekildedir:

    # sys.stdin ->  Bu, standart giriş (klavye girişi) dosya tanımlayıcısını temsil eder. termios modülü, terminal ayarlarını bu dosya tanımlayıcısı üzerinden kontrol eder.

    # termios.TCSADRAIN ->  Bu, tcsetattr fonksiyonuna verilen ayarların değiştirilmesi için kullanılan flag'dir. 

    # TCSADRAIN -> flag'i, ayarların değiştirilmesi için beklenmesi gereken işlemleri ifade eder. Örneğin, bu flag kullanıldığında, yazma işlemi tamamlanana kadar beklenir.

    # settings ->  Bu, önceki terminal ayarlarını içeren bir nesnedir. Bu ayarlar, termios.tcgetattr(sys.stdin) ile alınmış ve bir önceki durumu temsil eder.