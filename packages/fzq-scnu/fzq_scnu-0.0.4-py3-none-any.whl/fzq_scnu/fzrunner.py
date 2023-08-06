# coding=<encoding name> ： # coding=utf-8
# 项目名称：硬件仿真器
# 项目组成员：lmq,hjh,wpz,czj,sjw
# --------------------------------------------------------------------------------------------------------
'''
文件名：仿真器运行文件
作者：lmq(1.0),hjh(2.0)
版本：2.0
版本备注：每进行一次小型的修改并测试后，得到一个新的、稳定的、能推出使用的，版本号+0.1；
每有重大修改或者升级的版本号+1，尾数从0开始。
----------------------------------------------------
修改者和测试者信息登记（版本是指每修改连带测试一次在基于原版本号+0.0.1）
修改者：xxx(xx年xx月xx日，版本：2.0.0，修改文件名：xxx,xxx...)，
      xxx
'''
# --------------------------------------------------------------------------------------------------------
import os,threading, sys, logging, traceback
from pgzero.screen import Screen
from pgzero import loaders
from fzq_scnu import fzgpio
from pgzero.actor import Actor
from pgzero.rect import Rect
import pgzrun
import pygame
# --------------------------------------------------------------------------------------------------------
# 设置根路径（也就是仿真所需要的图像路径，此处由change.py写入）
images_path = ''
# --------------------------------------------------------------------------------------------------------
# 设置日志，记录报错内容
images_path_logger = ''
for i in images_path.split('\\'):
    if i == 'files':
        images_path_logger += 'txt'
    else:
        images_path_logger += i + '\\\\'
fzgpio.logger(images_path_logger)
# --------------------------------------------------------------------------------------------------------
# 窗口设置
screen: Screen
WIDTH, HEIGHT = 1300, 700
os.environ['SDL_VIDEO_CENTERED'] = '1'
TITLE = '华光仿真器'
ICON = images_path + 'data\\' + 'hg.png'
# --------------------------------------------------------------------------------------------------------
# 换页，code线程结束控制
pagechange = {'left': 1, 'right': 1}
code_threading_is_over = {'over': 0}
# --------------------------------------------------------------------------------------------------------
# 设置根目录
loaders.set_root(images_path)
# --------------------------------------------------------------------------------------------------------
# 写入文本，需要输入文本字符串(text)，坐标(pos)，颜色(color)默认为黑色，
# 字体（fontname）默认为仿宋（字体需要导入至文件同目录下的fonts文件中），
# 字体大小（fontsize）默认为18.
def draw_t(text, pos, color='black', fontname='fangsong.ttf', fontsize=18):
    screen.draw.text(text, center=pos, color=color, fontname=fontname, fontsize=fontsize)
# --------------------------------------------------------------------------------------------------------
# 角色，背景，赛道、障碍、物品或其他图像的名称与坐标或RGB
elements = {'actors': {1: ['car', (360, 370)]},
            'backgrounds': {0: ['none', (0, 0)],
                            1: ['background1', (0, 0)],
                            2: ['background2', (0, 0)],
                            3: ['background3', (0, 0)]},
            'racetracks': {0: ['none', (0, 0)],
                           1: ['racetrack1', (300, 80)],
                           2: ['racetrack2', (320, 150)]},
            'obstacles': {0: ['none', (255, 255, 255)],
                          1: ['obstacle1', (0, 150, 150)],
                          2: ['obstacle2', (0, 150, 150)]}
            }
# --------------------------------------------------------------------------------------------------------
# 主控
class Update(fzgpio.Mecanum_wheel, fzgpio.hongwai):
    def __init__(self):
        super(Update, self).__init__()
        self.Mecanumcar = Actor(elements['actors'][1][0])
        self.Mecanumcar.pos = (elements['actors'][1][1])

    # 背景清空
    def draw_clear(self):
        screen.clear()
        screen.fill((244, 244, 244))

    # 背景绘制
    def draw_background(self):
        pass
        # screen.blit(elements['backgrounds'][1][0], elements['backgrounds'][1][1])
        # screen.blit(elements['racetracks'][1][0], elements['racetracks'][1][1])
        # screen.blit('obstacle1', (300, 80))

    # 硬件图像刷新
    def draw_sensors(self):
        # 查看小车初始位置的像素点颜色
        # print(pygame.Surface.get_at(screen.surface, [360, 400]))
        if fzgpio.transmit_right != None:
            for key, value in list(fzgpio.transmit_right.items()):
                if key <= 5 and value[8] == 1 and pagechange['right'] == 1:
                    img = Actor(value[0])
                    img.pos = value[1]
                    img.draw()
                    draw_t(value[2], value[3])
                    servo_angle_control(value[2], value[1], value[6][1])
                    for i in range(2):
                        draw_t(value[4][i], value[5][i])
                        draw_t(value[6][i], value[7][i])
                elif key >= 5 and key <= 10 and value[8] == 2 and pagechange['right'] == 2:
                    img = Actor(value[0])
                    img.pos = value[1]
                    img.draw()
                    draw_t(value[2], value[3])
                    servo_angle_control(value[2], value[1], value[6][1])
                    for i in range(2):
                        draw_t(value[4][i], value[5][i])
                        draw_t(value[6][i], value[7][i])
                elif key >= 10 and key <= 15 and value[8] == 3 and pagechange['right'] == 3:
                    img = Actor(value[0])
                    img.pos = value[1]
                    img.draw()
                    draw_t(value[2], value[3])
                    servo_angle_control(value[2], value[1], value[6][1])
                    for i in range(2):
                        draw_t(value[4][i], value[5][i])
                        draw_t(value[6][i], value[7][i])
        if fzgpio.other_pos != None:
            for key, value in fzgpio.text_box.items():
                for key1, value1 in value.items():
                    draw_t(key1, value1)
        # # 小车左红外绘制
        # screen.draw.circle((int(fzgpio.dict['Hongwai_pos']['hongwai_left_x']),
        #                            int(fzgpio.dict['Hongwai_pos']['hongwai_left_y'])), 50, color=(0, 0, 0))
        # # 小车右红外绘制
        # screen.draw.circle((int(fzgpio.dict['Hongwai_pos']['hongwai_right_x']),
        #                            int(fzgpio.dict['Hongwai_pos']['hongwai_right_y'])), 50, color=(0, 0, 0))

    # 小车图像刷新
    def draw_car(self):
        if fzgpio.dict['Mecanumcar'][0] == 1:
            self.Mecanumcar.draw()
            # self.xunxian_run()

    # 获取红外像素点颜色
    def hongwai_position(self):
        # 获取小车左红外坐标处的像素颜色（RGBA）
        fzgpio.dict['car_pos_color_alpha']['left'] = \
            pygame.Surface.get_at(screen.surface,
                                  (int(fzgpio.dict['Hongwai_pos']['hongwai_left_x']),
                                   int(fzgpio.dict['Hongwai_pos']['hongwai_left_y'])))
        # 获取小车右红外坐标处的像素颜色（RGBA）
        fzgpio.dict['car_pos_color_alpha']['right'] = \
            pygame.Surface.get_at(screen.surface,
                                  (int(fzgpio.dict['Hongwai_pos']['hongwai_right_x']),
                                   int(fzgpio.dict['Hongwai_pos']['hongwai_right_y'])))

    # 小车运动刷新
    def update_car(self):
        if fzgpio.dict['Mecanumcar'][0] == 1:
            self.Mecanumcar_rect = Rect((self.Mecanumcar.left, self.Mecanumcar.top),
                                        (self.Mecanumcar.width, self.Mecanumcar.height))
            # 中间画面的大小，小车和物体的放置和运动不能超过此界限
            self.background_rect = Rect((200, 6), (900, 650))
            self.hongwai_rect = Rect((int(fzgpio.dict['Hongwai_pos']['hongwai_right_x']),
                                      int(fzgpio.dict['Hongwai_pos']['hongwai_right_y'])),
                                     (1, 1))
            if self.background_rect.contains(self.Mecanumcar_rect) and self.background_rect.contains(self.hongwai_rect):
                self.car_contr_run()
                try:
                    self.hongwai_position()
                except Exception as result:
                    msg = traceback.format_exc()
                    logging.error(str(msg))
                    print(result)
                    fzgpio.dict['exit'] = True
            else:
                pass

    # 运行监听
    def fzq_over(self):
        if fzgpio.dict['exit'] == True:
            sys.exit(0)

    # 子线程，这里写入新代码，子线程为仿真器画面展示的控制者
    def code(self):
        try:
            pass
            '''
            from fzq_scnu.fzcontrol import fzgpio
            import time
            f = fzgpio.led(3)
            f.openled()
            a = fzgpio.io(1)
            a.setinout('OUT')
            c = fzgpio.hongwai(4)
            c.get_return()
            d = fzgpio.PWM(2)
            d.pwm_start()
            d.change_duty(80)
            d.change_freq(150)
            e = fzgpio.beep(0)
            e.beep_s(1)
            g = fzgpio.tmp_hum(5)
            g.getTemp_Humi()
            h = fzgpio.csb(1)
            h.get_distance()
            l = fzgpio.csb(2)
            l.get_distance()
            i = fzgpio.servo(6)
            i.setServoAngle(60)
            time.sleep(2)
            i.setServoAngle(-60)
            m = fzgpio.Mecanum_wheel()
            m.uart_init()
            c.get_return()
            c.getioin()
            m.before_xunxian(7, 8)
            for i in range(2):
                c.get_return()
                c.getioin()
                print(c.ioin)
                m.xunxian()
                m.car_contr(100, 0, 0)
                time.sleep(2)
                m.car_contr(0,0,0)
            m.car_contr(100, 0, 0)
            time.sleep(1)
            f.closeled()
            e.close_b()
            time.sleep(1)
            e.open_b()
            c.get_return()
            '''
        except Exception as result:
            msg = traceback.format_exc()
            logging.error(str(msg))
            print(msg)
            fzgpio.dict['exit'] = True

    # 子线程控制，控制code线程
    def fzgo(self):
        # daemon参数为True，将子线程设置为守护线程，主线程结束，子线程跟着结束，进而使得进程立即结束
        # 设置daemon参数，最终目的是为了，在点击仿真界面右上角的叉叉关闭仿真器的时候，立即结束进程，避免主线程仍在等待子线程结束
        self.code_threading = threading.Thread(target=self.code, daemon=True)
        self.code_threading.start()
# --------------------------------------------------------------------------------------------------------
# 特殊函数：
# 设置舵机旋转机制
def servo_angle_control(hardwarepos_name, hardwarepos_pos, servo_angle):
    if hardwarepos_name == '舵机':
        img_name = 'steering_engine0'
        hardwarepos_pos = hardwarepos_pos
        servo_angle = int(eval(servo_angle.strip('°').strip(' ')))
        img = Actor(img_name)
        img.pos = hardwarepos_pos
        img.angle = servo_angle
        img.draw()
# --------------------------------------------------------------------------------------------------------
# 设置鼠标或按键事件 (监听)
# 功能一：点击鼠标右键给右边的硬件展示画面翻页
def on_mouse_down(pos,button):
    if button == 3:
        if pos[0]>=1160 and pos[1]<=655:
            if pagechange['right'] <= 2:
                pagechange['right'] += 1
            else:
                pagechange['right'] = 1
        elif pos[0]<=140 and pos[1]<=470:
            if pagechange['left'] <= 2:
                pagechange['left'] += 1
            else:
                pagechange['left'] = 1
# 功能二：
# 待开发
# --------------------------------------------------------------------------------------------------------
# 必须'def draw()'和'def update()',原设定就是如此,即无限循环执行draw()和update()
# 当然，也可以在game.py里的PGZeroGame.mainloop()设置无限循环
# 这里利用return返回调用的对象Update里面的draw(),update(),这样可以实现无限循环执行类中的方法
# 最终目的是实现面向对象开发
def draw():
    Draw0 = Update.draw_clear()
    Draw1 = Update.draw_background()
    Draw2 = Update.draw_sensors()
    Draw3 = Update.draw_car()
    return Draw0, Draw1, Draw2, Draw3

def update():
    Update0 = Update.update_car()
    Update1 = Update.fzq_over()
    return Update0, Update1
# --------------------------------------------------------------------------------------------------------
# 实例化对象
Update = Update()
# 启动子线程code（目的：利用子线程控制主线程的仿真画面）
Update.fzgo()
# --------------------------------------------------------------------------------------------------------
# 开始运行
# pgzrun.go()为死循环,也就是game.py里的PGZeroGame.mainloop()所设置的无限循环。
pgzrun.go()
# 以下语句只能在仿真器结束后执行。
print('仿真器运行结束')
