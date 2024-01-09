# Lidar ile Engellerden Kaçınma Projesi

Bu proje, Robot Operating System (ROS) ve Gazebo simülasyon ortamını kullanarak lidar sensörü ile engellerden kaçınma yeteneği sağlayan bir robot projesidir.

## Kurulum

Projenin başarılı bir şekilde çalışabilmesi için aşağıdaki adımları izleyin:

1. ROS Melodic veya Noetic sürümünü [ROS resmi web sitesinden](http://wiki.ros.org/ROS/Installation) indirin ve yükleyin.

2. Gazebo'nun yüklü olduğundan emin olun:

    ```bash
    sudo apt-get install gazebo9
    ```

3. Bu depoyu klonlayın:

    ```bash
    git clone https://github.com/Muhammetyilmaz7/Obstacle_Avoidance_With_ROS_and_Gazebo_Lidar.git
    ```
4. İndirdiğiniz kaynak kodun bir ROS'ta çalışma ortamı içinde olması gerektiğini unutmayın

5. Projenin kök dizininde aşağıdaki komutları çalıştırarak paketleri derleyin:

    ```bash
    catkin_make
    ```
    
6. Gazebo simülasyon ortamında TURTLEBOT3 olan dünyayı çalıştırın.

7. Gazebo dünyasında robot geldikten sonra çalışma alanındaki kodu çalıştırın.

## Kullanım

Proje başarıyla kurulduktan ve başlatıldıktan sonra, robotunuz lidar sensörüyle engellerden kaçınma yeteneği sergileyecek ve Gazebo simülasyon ortamında çalışacaktır. Kontroller ve parametreler hakkında daha fazla bilgi için kodu detaylıca inceleyin.

## Katkıda Bulunma

Eğer bu projeye katkıda bulunmak istiyorsanız, lütfen bir konu açarak veya bir çekme isteği göndererek iletişime geçin.

## Lisans

Bu proje MIT Lisansı altında lisanslanmıştır - [LICENSE](LICENSE) dosyasına bakın.

