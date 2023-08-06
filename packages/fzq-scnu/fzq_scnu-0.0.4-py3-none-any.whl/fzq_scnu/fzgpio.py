# coding=<encoding name> ： # coding=utf-8
import math, time, sys, threading, logging, traceback
from pgzero.actor import Actor

'''
！！！！！
待完成项：超声波的距离计算（可能需要设置障碍物）；
红外被遮挡（可利用rect碰撞,目前使用颜色检测）；巡线待更新；
'''
# --------------------------------------------------------------------------------------------------------
# 设置日志，记录报错内容
# filename = 'C:/Users/86137/Documents/python code/fzq_test/emulator_logging.txt'
class logger():
    def __init__(self, images_path_logger):
        self.images_path_logger= images_path_logger
        logging.basicConfig(filename=self.images_path_logger + 'emulator_logging.txt',
                             format='%(asctime)s - %(name)s - %(levelname)s - %(module)s; %(message)s',
                             datefmt='%Y-%m-%d %H:%M:%S',
                             level=30)
# --------------------------------------------------------------------------------------------------------
# 仿真界面所有固定及关联坐标点
hardwarepos_pic_right = {1:(1235, 70), 2:(1235, 200), 3:(1235, 330), 4:(1235, 460), 5:(1235, 590)}
hardwarepos_pic_left= {1:(71, 55), 2: (71, 225), 3: (71, 380)}
hardwarepos_name_right = {key:(1225, hardwarepos_pic_right[key][1] + 58)
                         for key,a in hardwarepos_pic_right.items()}
hardwarepos_name_left = {'csb':(71, 55+65), 'motor': (71, 225+70), 'wheel': (71, 380+78)}
io_pwm_pos_right = {key:[(hardwarepos_pic_right[key][0] - 102, hardwarepos_pic_right[key][1] - 45),
                         (hardwarepos_pic_right[key][0] - 102, hardwarepos_pic_right[key][1] - 20)]
                          for key,b in hardwarepos_pic_right.items()}
return_data_pos_right = {key:[(hardwarepos_pic_right[key][0] - 102, hardwarepos_pic_right[key][1] + 24),
                              (hardwarepos_pic_right[key][0] - 102, hardwarepos_pic_right[key][1] + 48)]
                         for key,c in hardwarepos_pic_right.items()}
return_data_pos_left = {key:[(hardwarepos_pic_left[key][0] + 96, hardwarepos_pic_left[key][1] - 20),
                              (hardwarepos_pic_left[key][0] + 96, hardwarepos_pic_left[key][1] + 20)]
                         for key,d in hardwarepos_pic_left.items()}
return_data_pos_right_other = {key:[(hardwarepos_pic_right[key][0] - 5, hardwarepos_pic_right[key][1] - 24),
                                    (hardwarepos_pic_right[key][0] - 5, hardwarepos_pic_right[key][1] + 24)]
                               for key,e in hardwarepos_pic_right.items()}
other_pos = {'文本框':(96, 485), '当地温度':[(60, 510), (140, 510)], '当地湿度':[(60, 533), (140, 533)]}
# --------------------------------------------------------------------------------------------------------
# 需要使用到的所有全局数据
dict = {'exit': False,
        'count': {'io': [0,[],9],'pwm': [0,[],4], 'uw': [0,[],2]},
        'num_count': 0,
        'Mecanumcar': [0, {'contr_fb': 0, 'contr_lr': 0, 'contr_tn': 0}],
        'before_xunxian': 0,
        'xunxian': 0,
        'xunxian_stop': 0,
        'Hongwai_pos': {'open': 0, 'left': '', 'right': '',
                    'hongwai_left_x': 0, 'hongwai_left_y': 0,
                    'hongwai_right_x': 0, 'hongwai_right_y': 0},
        'car_pos_color_alpha': {'left': (255,255,255,255), 'right': (255,255,255,255)}
        }
hongwai_quantity = {'left': ['none', 'none'], 'right': ['none', 'none']}
# --------------------------------------------------------------------------------------------------------
# 该字典用于传递给仿真器运行文件所需要的数据
transmit_right = {}
transmit_left = {}
text_box = {}
# --------------------------------------------------------------------------------------------------------
# io口或pwm口的分配，及相应的报错
class gpio_control():
    def __init__(self, io_pwm_uw_num=None, io_pwm_uw='io'):
        self.io_pwm_uw_num = io_pwm_uw_num
        self.io_pwm_uw = io_pwm_uw

    def raise_exception(self):
        try:
            mes = self.count_right()
            return mes
        except Exception as result:
            msg = traceback.format_exc()
            logging.error(str(msg))
            print(result)
            # 传参给主线程，告诉它立即结束，传完后立即执行sys.exit(0)，退出子线程，
            # 这样可以完美避免子线程在进程结束的最后0.5秒内仍在运行
            dict['exit'] = True
            sys.exit(0)

    def count_left(self):
        pass

    def count_right(self):
        assert type(self.io_pwm_uw_num) == int, \
            '未能检测到该{}{}号口,请检查'.format(self.io_pwm_uw, self.io_pwm_uw_num)

        if self.io_pwm_uw == 'io' or self.io_pwm_uw == 'pwm':
            assert self.io_pwm_uw_num in [i for i in range(dict['count'][self.io_pwm_uw][2])], \
                '未能检测到该{}{}号口,请检查'.format(self.io_pwm_uw, self.io_pwm_uw_num)
        elif self.io_pwm_uw == 'uw':
            assert self.io_pwm_uw_num in [i+1 for i in range(dict['count'][self.io_pwm_uw][2])], \
                '未能检测到该{}{}号口,请检查'.format(self.io_pwm_uw, self.io_pwm_uw_num)

        assert self.io_pwm_uw_num not in dict['count'][self.io_pwm_uw][1], \
           '该{}{}号口已被占用,请检查'.format(self.io_pwm_uw, self.io_pwm_uw_num)

        dict['count'][self.io_pwm_uw][0] += 1
        dict['count'][self.io_pwm_uw][1].append(self.io_pwm_uw_num)
        # 给右侧的展示的仿真图像分配坐标和页数
        if dict['count']['io'][0] + dict['count']['pwm'][0] + dict['count']['uw'][0] <= 5:
            dict['num_count'] += 1
            mes = (dict['num_count'], hardwarepos_pic_right[dict['num_count']], 1)
            return mes
        elif dict['count']['io'][0] + dict['count']['pwm'][0] + dict['count']['uw'][0] <= 10:
            dict['num_count'] += 1
            mes = (dict['num_count']-5, hardwarepos_pic_right[dict['num_count']-5], 2)
            return mes
        elif dict['count']['io'][0] + dict['count']['pwm'][0] + dict['count']['uw'][0] <= 15:
            dict['num_count'] += 1
            mes = (dict['num_count']-10, hardwarepos_pic_right[dict['num_count']-10], 3)
            return mes
# --------------------------------------------------------------------------------------------------------
# 进行统一操作，目的是在字典transmit中放入需要传递的所有可以用于绘制文字、图像等的参数
def message(hardwarepos_pic_name,hardwarepos_name,io_pwm,io_pwm_num,text1,text2,mes):
    name_position = hardwarepos_name_right[mes[0]]
    io_pwm_position = io_pwm_pos_right[mes[0]]
    if hardwarepos_name == 'IO' or hardwarepos_name == 'PWM':
        return_datas_position = return_data_pos_right_other[mes[0]]
    else:
        return_datas_position = return_data_pos_right[mes[0]]
    transmit_right[dict['num_count']] = [hardwarepos_pic_name, mes[1], hardwarepos_name,
                                         name_position, [io_pwm, str(io_pwm_num)],
                                         io_pwm_position, [text1, text2],
                                         return_datas_position,
                                         mes[2]]
# --------------------------------------------------------------------------------------------------------

# 主要
# gpio改为fzgpio
class io():
    def __init__(self, io_num=None):
        self.gpioio = io_num
        self.ioin = 404
        self.inorout = '未设置输入输出模式'
        self.dianping = '未设置高低电平'
        self.io_img_name = 'none'
        if self.gpioio != None:
            control = gpio_control(self.gpioio, 'io')
            mes = control.raise_exception()
            message(self.io_img_name, 'IO', 'IO', self.gpioio, ' ', ' ', mes)
            self.iocount = dict['num_count']

    def setinout(self, inorout):
        self.inorout = inorout
        if self.inorout == 'IN':
            transmit_right[self.iocount][6][0]= '模式：IN'
        elif self.inorout == 'OUT':
            transmit_right[self.iocount][6][0]= '模式：OUT'
        else:
            dict['exit'] = True
            print('未设置输入输出模式或是未知错误')
            sys.exit(0)

    def setioout(self, dianping):
        self.dianping = dianping
        if transmit_right[self.iocount][6][0]== '模式：OUT':
            # GPIO输出高or低电平
            if self.dianping == 'HIGH':
                transmit_right[self.iocount][6][1]= '电平：HIGH'
            elif self.dianping == 'LOW':
                transmit_right[self.iocount][6][1]= '电平：LOW'
            else:
                dict['exit'] = True
                print('未设置高低电平或是未知错误')
                sys.exit(0)
        else:
            dict['exit'] = True
            print('IO口未设置为输出模式,请检查')
            sys.exit(0)

    def getioin(self):
        if transmit_right[self.iocount][6][0] == '模式：IN':
            self.ioin = 0
        else:
            self.ioin = 1

    def cleanio(self):
        self.ioin = 404
        self.inorout = '未设置输入输出模式'
        self.dianping = '未设置高低电平'
        transmit_right[self.iocount][6][0] = ' '
        transmit_right[self.iocount][6][1] = ' '


class io2pwm():
    def __init__(self, io_num=None, freq=50, duty=50):
        self.iopwm_io = io_num
        self.iopwm_freq = freq
        self.iopwm_duty = duty
        self.iopwm_img_name = 'none'
        if self.iopwm_io != None:
            control = gpio_control(self.iopwm_io, 'io')
            mes = control.raise_exception()
            message(self.iopwm_img_name, 'IO', 'IO', self.iopwm_io, ' ', ' ', mes)
            self.iopwmcount = dict['num_count']

    def start(self):
        transmit_right[self.iopwmcount][6][0] = 'PWM:' + str(self.iopwm_freq) + 'Hz'
        transmit_right[self.iopwmcount][6][1] = str(self.iopwm_duty) + '%'

    def set_freq(self, pwm_freq):
        self.iopwm_freq = pwm_freq
        transmit_right[self.iopwmcount][6][0] = 'PWM:' + str(self.iopwm_freq) + 'Hz'

    def set_duty(self, pwm_duty):
        self.iopwm_duty = pwm_duty
        transmit_right[self.iopwmcount][6][1] = '占空比:' + str(self.iopwm_duty) + '%'

    def end(self):
        transmit_right[self.iopwmcount][6][0] = 'PWM:' + '0' + 'Hz'
        transmit_right[self.iopwmcount][6][1] = '占空比:' + '0' + '%'

class PWM():
    def __init__(self, pwm_io=None):
        self.pwm_io = pwm_io
        self.pwm_duty = 50
        self.pwm_freq = 262
        self.pwm_img_name = 'none'
        if self.pwm_io != None:
            control = gpio_control(self.pwm_io, 'pwm')
            mes = control.raise_exception()
            message(self.pwm_img_name, 'PWM', 'PWM', self.pwm_io, ' ', ' ', mes)
            self.pwmcount = dict['num_count']

    def pwm_start(self):
        transmit_right[self.pwmcount][6][0] = 'PWM:' + str(self.pwm_freq) + 'Hz'
        transmit_right[self.pwmcount][6][1] = str(self.pwm_duty) + '%'

    def change_duty(self, duty):
        self.pwm_duty = duty
        transmit_right[self.pwmcount][6][1] = '占空比:' + str(self.pwm_duty) + '%'

    def change_freq(self, freq):
        self.pwm_freq = freq
        transmit_right[self.pwmcount][6][0] = 'PWM:' + str(self.pwm_freq) + 'Hz'

    def pwm_stop(self):
        transmit_right[self.pwmcount][6][0] = 'PWM:' + '0' + 'Hz'
        transmit_right[self.pwmcount][6][1] = '占空比:' + '0' + '%'

class csb():
    def __init__(self, uw_num=None):
        self.csbuw = uw_num
        # self.trig_p = uw_num
        # self.echo_p = uw_num
        self.dis = 0
        self.csb_while = True
        self.csb_img_name = 'chaos'
        if self.csbuw != None:
            control = gpio_control(self.csbuw, 'uw')
            mes = control.raise_exception()
            message(self.csb_img_name, '超声波传感器', 'UW', self.csbuw, '关', ' ', mes)
            self.csbcount = dict['num_count']
    # 子线程目的：实现超声波传感器开启后的动画效果
    def csb_theading(self):
        imgs_name = ['chaos1', 'chaos2', 'chaos3', 'chaos4', 'chaos5', 'chaos6', 'chaos7', 'chaos8']
        while True:
            for img in imgs_name:
                if self.csb_while == True:
                    transmit_right[self.csbcount][6][0] = '开'
                    transmit_right[self.csbcount][0] = img
                    time.sleep(1)
                else:
                    sys.exit(0)

    def get_distance(self):
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!待更新
        # print('超声波传感器获取距离的方式待更新')
        self.dis = 20
        self.beep_while = True
        self.beep_thead = threading.Thread(target=self.csb_theading, daemon=True)
        self.beep_thead.start()

class beep():
    def __init__(self, beepio=None):
        self.beepio = beepio
        # self.data = 0
        self.beep_while = True
        self.beep_img_name = 'beep'
        if self.beepio != None:
            control = gpio_control(self.beepio, 'io')
            mes = control.raise_exception()
            message(self.beep_img_name, '蜂鸣器', 'IO', self.beepio, '关', ' ', mes)
            self.beepcount = dict['num_count']
    # 子线程目的：实现蜂鸣器开启后的动画效果
    def beep_theading(self):
        imgs_name = ['beep1', 'beep2', 'beep3']
        while True:
            for img in imgs_name:
                if self.beep_while == True:
                    transmit_right[self.beepcount][6][0] = '开'
                    transmit_right[self.beepcount][0] = img
                    time.sleep(1)
                else:
                    sys.exit(0)

    def beep_s(self, seconds=1):
        self.beep_while = True
        self.beep_thead = threading.Thread(target=self.beep_theading, daemon=True)
        time.sleep(seconds)
        self.beep_thead.start()

    def open_b(self):
        self.beep_while = True
        self.beep_thead = threading.Thread(target=self.beep_theading, daemon=True)
        self.beep_thead.start()

    def close_b(self):
        self.beep_while = False
        transmit_right[self.beepcount][6][0] = '关'
        transmit_right[self.beepcount][0] = 'beep'

class led():
    def __init__(self, ledio=None):
        self.ledio = ledio
        self.led_img_name = 'led_off1'
        if self.ledio != None:
            control = gpio_control(self.ledio, 'io')
            mes = control.raise_exception()
            message(self.led_img_name, 'Led', 'IO', self.ledio, '灭', '', mes)
            self.ledcount = dict['num_count']

    def openled(self):
        transmit_right[self.ledcount][0]= 'led_on1'
        transmit_right[self.ledcount][6][0]= '亮'

    def closeled(self):
        transmit_right[self.ledcount][0]= 'led_off1'
        transmit_right[self.ledcount][6][0] = '灭'

class tmp_hum():
    def __init__(self, t_h_io=None):
        self.tmp_io = t_h_io
        self.temp = None
        self.humi = None
        self.tmp_hum_img_name = 'wsdu1'
        if self.tmp_io != None:
            control = gpio_control(self.tmp_io, 'io')
            mes = control.raise_exception()
            message(self.tmp_hum_img_name, '温湿度传感器', 'IO', self.tmp_io, '关', '', mes)
            self.tmp_humcount = dict['num_count']

    def getTemp_Humi(self):
        # ！！！！！！！！！！！！！！！！！！待更新
        self.temp, self.humi = 26, 30
        if self.temp or self.humi:
            text_box['temp_humi'] = {'文本框': other_pos['文本框'],
                                     '当地温度：': other_pos['当地温度'][0],
                                     str(self.temp) + '℃': other_pos['当地温度'][1],
                                     '当地湿度：': other_pos['当地湿度'][0],
                                     str(self.humi) + '%': other_pos['当地湿度'][1]}
            transmit_right[self.tmp_humcount][6][0] = '开'
        else:
            print("温湿度传感器：获取温湿度失败")

class hongwai():
    def __init__(self, hongwaiio = None, position = '左'):
        # 默认先使用左红外
        self.hongwaiio = hongwaiio
        self.position = position
        self.lr = None
        self.data = 0
        self.ioin = 0
        self.hongwai_img_name = 'hongwai0'
        if self.hongwaiio != None:
            if hongwai_quantity['left'][0] == 'none':
                control = gpio_control(self.hongwaiio, 'io')
                mes = control.raise_exception()
                message(self.hongwai_img_name, '红外传感器', 'IO', self.hongwaiio, 'IN', '0', mes)
                self.hongwaicount = dict['num_count']
                hongwai_quantity['left'][0] = 'true'
                hongwai_quantity['left'][1] = str(self.hongwaicount)
                # 启动子线程
                self.hongwai_thead = threading.Thread(target=self.hongwai_threading, daemon=True)
                self.hongwai_thead.start()
            elif hongwai_quantity['right'][0] == 'none':
                control = gpio_control(self.hongwaiio, 'io')
                mes = control.raise_exception()
                message(self.hongwai_img_name, '红外传感器', 'IO', self.hongwaiio, 'IN', '0', mes)
                self.hongwaicount = dict['num_count']
                hongwai_quantity['right'][0] = 'true'
                hongwai_quantity['right'][1] = str(self.hongwaicount)
                # 启动子线程
                self.hongwai_thead = threading.Thread(target=self.hongwai_threading, daemon=True)
                self.hongwai_thead.start()
            else:
                print('红外数量上限是两个')

    # 用户手动调用，需要反复调用才能持续显示返回值
    def get_return(self):
        if dict['Mecanumcar'][0] == 1:
            imgs_name = ['hongwai1', 'hongwai2']
            if hongwai_quantity['left'][0] == 'true' and hongwai_quantity['left'][1] == str(self.hongwaicount):
                self.lr = 'left'
            elif hongwai_quantity['right'][0] == 'true' and hongwai_quantity['right'][1] == str(self.hongwaicount):
                self.lr = 'right'
            if self.lr:
                a = 0
                # 特别注意：此处必须延时，不然更不上主线程（或者说是主线程里面的子线程code）里面的for循环速度
                time.sleep(0.1)
                for i in range(3):
                    if dict['car_pos_color_alpha'][self.lr][i] == 255:
                        a += 1
                if a == 3:
                    # dict['Hongwai_pos'][lr] = 0
                    transmit_right[self.hongwaicount][0] = imgs_name[1]
                    transmit_right[self.hongwaicount][6][1] = '0'
                    self.data = eval(transmit_right[self.hongwaicount][6][1])
                else:
                    # dict['Hongwai_pos'][lr] = 1
                    transmit_right[self.hongwaicount][0] = imgs_name[0]
                    transmit_right[self.hongwaicount][6][1] = '1'
                    self.data = eval(transmit_right[self.hongwaicount][6][1])
        else:
            print('使用红外，请先初始化小车')

    # 子线程目的：等待一会后，红外不亮，返回值归空
    def hongwai_threading(self):
        time.sleep(1)
        transmit_right[self.hongwaicount][0] = 'hongwai0'

    # 只供麦克纳姆小车调用（有左右红外区分）
    # def get_return_2(self):
    #     imgs_name = ['hongwai1', 'hongwai2']
    #     if self.position == '左':
    #         a = 0
    #         for i in range(3):
    #             if dict['car_pos_color_alpha']['left'][i] >= 170 and dict['car_pos_color_alpha']['left'][i] <= 175:
    #                 a +=1
    #         if a >= 2:
    #             dict['Hongwai_pos']['left'] = 0
    #             self.data = 0
    #             transmit_right[self.hongwaicount][0] = imgs_name[1]
    #             transmit_right[self.hongwaicount][6][1] = '左:0'
    #         else:
    #             dict['Hongwai_pos']['left'] = 1
    #             self.data = 1
    #             transmit_right[self.hongwaicount][0] = imgs_name[0]
    #             transmit_right[self.hongwaicount][6][1] = '左:1'
    #     elif self.position == '右':
    #         b = 0
    #         for i in range(3):
    #             if dict['car_pos_color_alpha']['right'][i] >= 170 and dict['car_pos_color_alpha']['right'][i] <= 175:
    #                 b += 1
    #         if b >= 2:
    #             dict['Hongwai_pos']['right'] = 0
    #             transmit_right[self.hongwaicount][0] = imgs_name[1]
    #             transmit_right[self.hongwaicount][6][1] = '右:0'
    #         else:
    #             dict['Hongwai_pos']['right'] = 1
    #             transmit_right[self.hongwaicount][0] = imgs_name[0]
    #             transmit_right[self.hongwaicount][6][1] = '右:1'

    # 用户调用
    def getioin(self):
        if '0' in transmit_right[self.hongwaicount][6][1]:
            self.ioin = 0
        elif '1' in transmit_right[self.hongwaicount][6][1]:
            self.ioin = 1

class servo():
    def __init__(self, servo_io=None):
        self.servoio = servo_io
        self.duty = 0
        self.servo_img_name = 'steering_engine'
        if self.servoio != None:
            control = gpio_control(self.servoio, 'io')
            mes = control.raise_exception()
            message(self.servo_img_name, '舵机', 'IO', self.servoio, '开', '', mes)
            self.servoiocount = dict['num_count']

    def setServoAngle(self, angle):  # 设置舵机角度
        self.servo_angle = angle
        transmit_right[self.servoiocount][6][1] = ' ' + str(self.servo_angle) + '°'

class Mecanum_wheel():
    def __init__(self):
        self.Mecanumcar = Actor('car')
        # self.Mecanumcar.pos = (360, 400)
        self.Mecanumcar.pos = (360, 370)
        self.car_speed = {'car_go': 0, 'car_back': 0,
                          'car_turn_l': 0, 'car_turn_r': 0,
                          'car_across_l': 0, 'car_across_r': 0}
        # 初始化时，计算小车左右红外的位置
        dict['Hongwai_pos']['hongwai_left_x'] = self.Mecanumcar.x - self.Mecanumcar.height * 6 / 11 * math.sin(
            math.radians(self.Mecanumcar.angle)) - 10 * math.cos(math.radians(self.Mecanumcar.angle)) - 1 / 2
        dict['Hongwai_pos']['hongwai_left_y'] = self.Mecanumcar.y - self.Mecanumcar.height * 6 / 11 * math.cos(
            math.radians(self.Mecanumcar.angle)) + 10 * math.sin(math.radians(self.Mecanumcar.angle)) - 1 / 2
        dict['Hongwai_pos']['hongwai_right_x'] = self.Mecanumcar.x - self.Mecanumcar.height * 6 / 11 * math.sin(
            math.radians(self.Mecanumcar.angle)) + 10 * math.cos(math.radians(self.Mecanumcar.angle)) - 1 / 2
        dict['Hongwai_pos']['hongwai_right_y'] = self.Mecanumcar.y - self.Mecanumcar.height * 6 / 11 * math.cos(
            math.radians(self.Mecanumcar.angle)) - 10 * math.sin(math.radians(self.Mecanumcar.angle)) - 1 / 2

    # 初始化小车，用户直接调用
    def uart_init(self):
        if dict['Mecanumcar'][0] == 0:
            dict['Mecanumcar'][0] = 1
        elif dict['Mecanumcar'][0] == 1:
            print('已经初始化了麦克纳姆小车，无需再初始化')
            dict['exit'] = True
    #-------------------------------------------------------
    # 设置小车速度的所有方法，用户直接调用
    def stop(self):
        self.car_speed['car_go'] = 0
        self.car_speed['car_back'] = 0
        self.car_speed['car_across_l'] = 0
        self.car_speed['car_across_r'] = 0
        self.car_speed['car_turn_l'] = 0
        self.car_speed['car_turn_r'] = 0
        self.car_contr()

    def car_go(self):
        self.car_contr()

    def car_across_l(self):
        self.car_contr()

    def car_turn_l(self):
        self.car_contr()

    def car_back(self):
        self.car_contr()

    def car_across_r(self):
        self.car_contr()

    def car_turn_r(self):
        self.car_contr()

    def car_contr(self):
        if dict['Mecanumcar'][0] == 1:
            dict['Mecanumcar'][1]['contr_fb'] = self.car_speed['car_go']-self.car_speed['car_back']
            dict['Mecanumcar'][1]['contr_lr'] = self.car_speed['car_across_l']-self.car_speed['car_across_r']
            dict['Mecanumcar'][1]['contr_tn'] = self.car_speed['car_turn_l']-self.car_speed['car_turn_r']
    # -------------------------------------------------------
    # car_contr_run是真正在仿真器运行文件里面刷新的函数
    def car_contr_run(self,t=0.01):
        if dict['Mecanumcar'][0] == 1:
            # if self.Mecanumcar.x >= 200 + self.Mecanumcar.width / 2 and \
            #         self.Mecanumcar.x <= 1100 - self.Mecanumcar.width / 2 and \
            #         self.Mecanumcar.y >= 5 + self.Mecanumcar.height / 2 and \
            #         self.Mecanumcar.y <= 650 - self.Mecanumcar.height / 2:
            fb = dict['Mecanumcar'][1]['contr_fb']
            lr = dict['Mecanumcar'][1]['contr_lr']
            tn = dict['Mecanumcar'][1]['contr_tn']
            # 坐标计算，实现移动
            self.Mecanumcar.x -= fb * math.sin(math.radians(self.Mecanumcar.angle)) * t
            self.Mecanumcar.y -= fb * math.cos(math.radians(self.Mecanumcar.angle)) * t
            self.Mecanumcar.x -= lr * math.cos(math.radians(self.Mecanumcar.angle)) * t
            self.Mecanumcar.y -= -lr * math.sin(math.radians(self.Mecanumcar.angle)) * t
            self.Mecanumcar.angle += tn * t
            self.Mecanumcar.pos = (self.Mecanumcar.x, self.Mecanumcar.y)
            # 初始化时，计算小车左右红外的位置
            dict['Hongwai_pos']['hongwai_left_x'] = self.Mecanumcar.x - self.Mecanumcar.height * 6 / 11 * math.sin(
                math.radians(self.Mecanumcar.angle)) - 10 * math.cos(math.radians(self.Mecanumcar.angle)) - 1 / 2
            dict['Hongwai_pos']['hongwai_left_y'] = self.Mecanumcar.y - self.Mecanumcar.height * 6 / 11 * math.cos(
                math.radians(self.Mecanumcar.angle)) + 10 * math.sin(math.radians(self.Mecanumcar.angle)) - 1 / 2
            dict['Hongwai_pos']['hongwai_right_x'] = self.Mecanumcar.x - self.Mecanumcar.height * 6 / 11 * math.sin(
                math.radians(self.Mecanumcar.angle)) + 10 * math.cos(math.radians(self.Mecanumcar.angle)) - 1 / 2
            dict['Hongwai_pos']['hongwai_right_y'] = self.Mecanumcar.y - self.Mecanumcar.height * 6 / 11 * math.cos(
                math.radians(self.Mecanumcar.angle)) - 10 * math.sin(math.radians(self.Mecanumcar.angle)) - 1 / 2
    # # -------------------------------------------------------
    # # 巡线必须先初始化左右两个红外，初始化后，不能更改小车红外io设置。用户直接调用
    # def before_xunxian(self, io_l, io_r):
    #     global io_le, io_ri
    #     io_le = io_l
    #     io_ri = io_r
    #     dict['before_xunxian'] = 1
    #
    # # -------------------------------------------------------
    # # 命令开始巡线，用户直接调用
    # def xunxian(self):
    #     try:
    #         assert dict['before_xunxian'] == 1 or dict['before_xunxian'] == 2, "未设置巡线用的左右红外"
    #         dict['xunxian'] = 1
    #         dict['xunxian_stop'] = 0
    #         print('开始巡线')
    #         while dict['xunxian'] ==1 and dict['xunxian_stop'] == 0:
    #             pass
    #         dict['xunxian'] = 0
    #         print('巡线结束')
    #     except Exception as result:
    #         msg = traceback.format_exc()
    #         logging.error(str(msg))
    #         print(result)
    #         sys.exit(0)
    # # -------------------------------------------------------
    # # xunxian_run是真正在仿真器运行文件里面刷新的函数
    # def xunxian_run(self):
    #     if dict['xunxian'] == 1 and dict['before_xunxian'] == 1:
    #         self.hw_l = hongwai(io_le, '左')
    #         self.hw_r = hongwai(io_ri, '右')
    #         dict['before_xunxian'] = 2
    #     elif dict['xunxian'] == 1 and dict['before_xunxian'] == 2:
    #         self.hw_l.get_return_2()
    #         self.hw_r.get_return_2()
    #         # 左转
    #         if dict['Hongwai_pos']['right'] == 1 and dict['Hongwai_pos']['left'] == 0:
    #             # self.car_contr(0, -100, 200)
    #             dict['Mecanumcar'][1]['contr_fb'] = 0
    #             dict['Mecanumcar'][1]['contr_lr'] = -50
    #             dict['Mecanumcar'][1]['contr_tn'] = 200
    #             # self.car_contr(0, -100, 300)
    #         # 右转
    #         elif dict['Hongwai_pos']['right'] == 0 and dict['Hongwai_pos']['left'] == 1:
    #             # self.car_contr(0, 100, -200)
    #             dict['Mecanumcar'][1]['contr_fb'] = 0
    #             dict['Mecanumcar'][1]['contr_lr'] = 50
    #             dict['Mecanumcar'][1]['contr_tn'] = -200
    #             # self.car_contr(0, 100, -300)
    #         # 前进
    #         elif dict['Hongwai_pos']['right'] == 0 and dict['Hongwai_pos']['left'] == 0:
    #             # self.car_contr(100, 0, 0)
    #             dict['Mecanumcar'][1]['contr_fb'] = 100
    #             dict['Mecanumcar'][1]['contr_lr'] = 0
    #             dict['Mecanumcar'][1]['contr_tn'] = 0
    #         # 停止
    #         elif dict['Hongwai_pos']['right'] == 1 and dict['Hongwai_pos']['left'] == 1:
    #             dict['Mecanumcar'][1]['contr_fb'] = 0
    #             dict['Mecanumcar'][1]['contr_lr'] = 0
    #             dict['Mecanumcar'][1]['contr_tn'] = 0
    #             dict['xunxian_stop'] = 1
    #             transmit_right[self.hw_l.hongwaicount][0] = 'hongwai0'
    #             transmit_right[self.hw_l.hongwaicount][6][1] = ' '
    #             transmit_right[self.hw_r.hongwaicount][0] = 'hongwai0'
    #             transmit_right[self.hw_r.hongwaicount][6][1] = ' '
    #     else:
    #         pass


