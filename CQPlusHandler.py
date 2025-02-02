# -*- coding:utf-8 -*-

import cqplus
import os
from random import sample


class Handle():

    def pathinit(self):
        '''初始化路径'''
        path = 'app/me.cqp.kizx.rollgames/activities'
        if not os.path.exists(path):
            os.mkdir(path)
        mess = '初始化路径成功'
        return mess

    def menu(self):
        '''查看所有命令'''
        mess = '\n'.join(['\n====本插件命令如下====',
                          inst['1'],
                          inst['7'],
                          inst['3']+'+游戏名',
                          inst['4']+'+游戏名',
                          inst['5'],
                          inst['6']+'+游戏名',
                          inst['11']+'+开启/关闭'
                          '='*20,
                          '[CQ:face,id=29]注意以上命令中+表示换行'])
        return mess

    def view_acti(self):
        '''查看当前活动'''
        path = 'app/me.cqp.kizx.rollgames/activities'
        acti = []
        for filename in os.listdir(path):
            acti.append(os.path.splitext(filename)[0])
        if acti == []:
            mess = '当前没有活动哦~要不你来整一个[CQ:face,id=178]'
        else:
            mess = '当前有如下活动：\n' + '\n'.join(acti)
        return mess

    def wantroll(self):
        '''我要roll游戏格式'''
        mess = '\n'.join(['欢迎老板roll游戏！',
                          '====请按以下格式新建活动====',
                          inst['2'],
                          '游戏名称（注意相同名称会覆盖）',
                          '描述（如15号开奖）'])
        return mess

    def view_memb(self, game):
        '''查看已报名参加人员名单'''
        path = 'app/me.cqp.kizx.rollgames/activities/' + game + '.txt'
        with open(path, 'r') as f:
            mastqq = f.readline().split('：')[1].split(' - ')[0]
            mastqqan = mastqq[:3] + '****' + mastqq[7:]
            f.seek(0, 0)
            messlist = []
            for index, line in enumerate(f):
                if index == 0:
                    line = line.replace(mastqq, mastqqan)
                    messlist.append(line)
                elif index >= 3:
                    messlist.append(line[:3] + '****' + line[7:])
                else:
                    messlist.append(line)
        mess = '\n' + ''.join(messlist)
        return mess

    def how_roll(self):
        '''roll游戏格式'''
        mess = '\n'.join(['\n===请按以下格式roll游戏===',
                          inst['9'],
                          '游戏名',
                          '中奖人数(不写默认为1)'])
        return mess


class Handlein:

    def __init__(self, Env, QQ, Group):
        self.qq = QQ
        self.group = Group
        self.env = Env

    def create(self, game, desc):
        '''新建活动'''
        path = 'app/me.cqp.kizx.rollgames/activities/' + game + '.txt'
        with open(path, 'w') as f:
            info = cqplus._api.get_group_member_info(
                self.env, self.group, self.qq, True)
            name = info['card'] if info['card'] != '' else info['nickname']
            f.write('金主：' + str(self.qq) + ' - ' +
                    name + '\n游戏：' + game + '\n描述：' + desc)
        mess = '\n'.join(['\n您已成功发起roll<' + game + '>活动！',
                          '===发送以下命令参加活动===', inst['3'], game,
                          '===发送以下命令查看名单===', inst['4'], game])
        return mess

    def join(self, game):
        '''参加活动'''
        path = 'app/me.cqp.kizx.rollgames/activities/' + game + '.txt'
        memb = []
        with open(path, 'r') as f:
            for line in f:
                memb.append(line.split(' - ')[0])
        if str(self.qq) not in memb:
            with open(path, 'a') as f:
                info = cqplus._api.get_group_member_info(
                    self.env, self.group, self.qq, True)
                name = info['card'] or info['nickname']
                f.write('\n' + str(self.qq) + ' - ' + name)
            mess = '恭喜您已成功报名参加roll<' + game + '>'
        else:
            mess = '你已经参加过了哦，请勿重复报名'
        return mess

    def roll(self, game, num=1):
        '''roll游戏'''
        path = 'app/me.cqp.kizx.rollgames/activities/' + game + '.txt'
        with open(path, 'r') as f:
            mastqq = f.readline().split('：')[1].split(' - ')[0]
        if str(self.qq) == mastqq or str(self.qq) == inst['10']:
            with open(path, 'r') as f:
                memb = f.readlines()
            memb.pop(0)
            memb.pop(0)
            memb.pop(0)
            lucky = sample(memb, int(num))
            mess = ''
            for each in lucky:
                lucky_qq = each.split(' - ')[0]
                mess = mess+'[CQ:at,qq='+lucky_qq+']'
            mess = '\n[CQ:face,id=99]恭喜欧皇' + mess + '获得了' + game + \
                '\n[CQ:face,id=30]没有获奖的小伙伴也不要沮丧哦~\nPS.确认无误后请用结束活动命令删除活动'
        else:
            mess = '你没有这个权限哦'
        return mess

    def endgame(self, game):
        '''结束活动'''
        path = 'app/me.cqp.kizx.rollgames/activities/' + game + '.txt'
        with open(path, 'r') as f:
            mastqq = f.readline().split('：')[1].split(' - ')[0]
        if str(self.qq) == mastqq or str(self.qq) == inst['10']:
            os.remove(path)
            mess = '已成功删除' + game + '活动！'
        else:
            mess = '你没有这个权限哦'
        return mess

    def timer_swich(self, isoff):
        '''定时播报开关'''
        path = 'app/me.cqp.kizx.rollgames/setting.ini'
        if isoff == '开启' or isoff == '关闭':
            if str(self.qq) == inst['10']:
                with open(path, 'w') as f:
                    f.write(str(self.group) + ' - ' + isoff)
                    mess = '定时播报已' + isoff
            else:
                mess = '你没有这个权限哦'
        else:
            mess = '输入的指令格式有误！'
        return mess


class MainHandler(cqplus.CQPlusHandler):
    def handle_event(self, event, params):
        # 处理群聊消息
        if event == "on_group_msg":
            msg = params['msg']
            mess = ''
            if msg in dic1:
                msgHandle = Handle()
                mess = dic1[msg](msgHandle)
            else:
                strlist = msg.splitlines()
                if strlist[0] in dic2:
                    msgHandlein = Handlein(
                        params['env'], params['from_qq'], params['from_group'])
                    try:
                        if strlist[0] == inst['2']:
                            mess = msgHandlein.create(strlist[1], strlist[2])
                        elif strlist[0] == inst['3']:
                            mess = msgHandlein.join(strlist[1])
                        elif strlist[0] == inst['4']:
                            msgHandle = Handle()
                            mess = msgHandle.view_memb(strlist[1])
                        elif strlist[0] == inst['9']:
                            if len(strlist) == 2:
                                mess = msgHandlein.roll(strlist[1])
                            else:
                                mess = msgHandlein.roll(strlist[1], strlist[2])
                        elif strlist[0] == inst['6']:
                            mess = msgHandlein.endgame(strlist[1])
                        elif strlist[0] == inst['11']:
                            mess = msgHandlein.timer_swich(strlist[1])
                    except IndexError:
                        mess = '输入的指令不完整！'
                    except ValueError:
                        mess = '输入的指令格式有误！'
                    except FileNotFoundError:
                        mess = '输入的活动不存在！'
            if mess != '':
                mess = '[CQ:at,qq=' + str(params['from_qq']) + ']' + mess
                self.api.send_group_msg(params['from_group'], mess)

        # 定时器消息
        if event == 'on_timer':
            if params['name'] == 'timer01':
                path = 'app/me.cqp.kizx.rollgames/setting.ini'
                with open(path, 'r') as f:
                    setting = f.readline().split(' - ')
                    if setting[1] == '开启':
                        msgHandle = Handle()
                        mess = msgHandle.view_acti()
                        if mess != '当前没有活动哦~要不你来整一个[CQ:face,id=178]':
                            self.api.send_group_msg(int(setting[0]), mess)

        # 菜单动作
        # if event == 'on_menu':
        #     if params['name'] == 'menu01':
        #         self.api.send_group_msg(562360425, '菜单01被点击')

        # 处理私聊消息
        # if event == "on_private_msg":
        #     msg = params['msg']
        #     qq = params['from_qq']
        #     self.api.send_private_msg(int(inst['10']), str(qq) + '发送了：' + msg)


inst = {'0': '查看命令', '1': '我要roll游戏', '2': '#我要roll游戏#', '3': '我要参加roll游戏',
        '4': '查看名单', '5': '开始roll游戏', '6': '结束活动', '7': '查看当前活动', '8': '初始化',
        '9': '#开始roll游戏#', '10': '3317200497', '11': '定时器'}
dic1 = {'查看命令': Handle.menu, '我要roll游戏': Handle.wantroll, '查看当前活动': Handle.view_acti,
        '开始roll游戏': Handle.how_roll, '初始化': Handle.pathinit}
dic2 = {'#我要roll游戏#': Handlein.create, '我要参加roll游戏': Handlein.join, '查看名单': Handle.view_memb,
        '#开始roll游戏#': Handlein.roll, '结束活动': Handlein.endgame, '定时器': Handlein.timer_swich}
