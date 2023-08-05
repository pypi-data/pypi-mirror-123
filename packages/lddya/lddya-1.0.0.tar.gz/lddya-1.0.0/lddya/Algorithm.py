import copy 
import random
import numpy as np
from numpy.lib.function_base import average
import pygame as py
from pygame import pixelcopy
import pygame
from pygame.transform import flip
from pygame.draw import line
from pygame.version import ver

# Ant只管通过地图数据以及信息素数据，输出一条路径。其他的你不用管。
class Ant():
    def __init__(self,max_step,pher_imp,dis_imp) -> None:
        self.max_step = max_step    # 蚂蚁最大行动力
        self.pher_imp = pher_imp    # 信息素重要性系数
        self.dis_imp = dis_imp      # 距离重要性系数
        self.destination = [19,19]  # 默认的终点节点
        self.successful = True      #标志蚂蚁是否成功抵达终点
        self.record_way = [[0,0]]   #路径节点信息记录
        

    def run(self,map_data,pher_data):
        #Step 0:把蚂蚁放在起点处
        self.position = [0,0]       #蚂蚁初始位置[y,x] = [0,0],考虑到列表索引的特殊性，先定y，后定x
        #Step 1:不断找下一节点，直到走到终点或者力竭 
        for i in range(self.max_step):
            r = self.select_next_node(map_data,pher_data)
            if r == False:
                self.successful = False
                break
            else:
                if self.position == self.destination:
                    break
        else:
            self.successful = False
    
    def select_next_node(self,map_data,pher_data):
        '''
        Function:
        ---------
        选择下一节点，结果直接存入self.postion，仅返回一个状态码True/False标志选择的成功与否。
        '''
        y_1 = self.position[0]
        x_1 = self.position[1]
        #Step 1:计算理论上的周围节点
        node_be_selected = [[y_1-1,x_1-1],[y_1-1,x_1],[y_1-1,x_1+1],     #上一层
                            [y_1,x_1-1],              [y_1,x_1+1],       #同层
                            [y_1+1,x_1-1],[y_1+1,x_1],[y_1+1,x_1+1],     #下一层
                        ]
        #Step 2:排除非法以及障碍物节点    
        node_be_selected_1 = []
        for i in node_be_selected:
            if i[0]<0 or i[1]<0:
                continue
            if i[0]>=len(map_data) or i[1]>=len(map_data):
                continue
            if map_data[i[0]][i[1]] == 0:
                node_be_selected_1.append(i)
        if len(node_be_selected_1) == 0:    # 如果无合法节点，则直接终止节点的选择
            return False
        if self.destination in node_be_selected_1:   # 如果到达终点旁，则直接选中终点
            self.position = self.destination
            self.record_way.append(copy.deepcopy(self.position))
            map_data[self.position[0]][self.position[1]] = 1
            return True
        #Step 3:计算节点与终点之间的距离，构建距离启发因子
        dis_1 = []    # 距离启发因子
        for i in node_be_selected_1:
            dis_1.append(((self.destination[0]-i[0])**2+(self.destination[1]-i[1])**2)**0.5)
        #Step 3.1:使用偏差放大策略
        #dis_min = min(dis_1)
        #for j in range(len(dis_1)):
        #    dis_1[j] = dis_1[j]-0.80*dis_min
        #Step 3.2:倒数反转
        for j in range(len(dis_1)):
            dis_1[j] = 1/dis_1[j]

        #Step 4:计算节点被选中的概率
        prob = []
        for i in range(len(node_be_selected_1)):
            p = (dis_1[i]**self.dis_imp) * (pher_data[y_1*len(map_data)+x_1][node_be_selected_1[i][0]*len(map_data)+node_be_selected_1[i][1]]**self.pher_imp)
            prob.append(p)
        #Step 5:轮盘赌选择某节点
        prob_sum = sum(prob)
        for i in range(len(prob)):
            prob[i] = prob[i]/prob_sum
        rand_key = random.random()
        select_index = 0
        for k,i in enumerate(prob):
            if rand_key<=i:
                select_index = k
                break
            else:
                rand_key -= i
        #Step 6:更新当前位置，并记录新的位置，将之前的位置标记为不可通过
        self.position = copy.deepcopy(node_be_selected_1[k])
        self.record_way.append(copy.deepcopy(self.position))
        map_data[self.position[0]][self.position[1]] = 1
        return True



class ACO():
    def __init__(self,max_iter = 100,pher_imp = 1,dis_imp = 10,evaporate = 0.7,pher_init = 8) -> None:
        '''
            Params:
            --------
                pher_imp : 信息素重要性系数
                dis_imp  : 距离重要性系数
                evaporate: 信息素挥发系数(指保留的部分)
                pher_init: 初始信息素浓度
        '''
        #Step 0: 参数定义及赋值
        self.max_iter = max_iter       #最大迭代次数
        self.ant_num  = 50         #蚂蚁数量
        self.ant_gener_pher = 1    #每只蚂蚁携带的最大信息素总量
        self.pher_init = pher_init #初始信息素浓度
        self.ant_params = {        #生成蚂蚁时所需的参数
            'dis_imp':dis_imp,
            'pher_imp': pher_imp
        }
        self.map_data = []         #地图数据
        self.pher_data =[]         #信息素浓度数据
        self.evaporate = evaporate #信息素挥发系数
        self.map_lenght = 0        #地图尺寸,用来标定蚂蚁的最大体力，在loading_map()中给出
        self.generation_aver = []  #每代的平均路径(大小)，绘迭代图用
        self.generation_best = []  #每代的最短路径(大小)，绘迭代图用
        self.way_len_best = 999999 
        self.way_data_best = []     #最短路径对应的节点信息，画路线用 

        

    def load_map(self,filepath ='res\\map.dll',reverse = False):
        with open(filepath,'r') as f:
            a_1 = f.readlines()
        self.map_lenght = len(a_1)
        for i in range(self.map_lenght):
            a_1[i] = a_1[i].strip('\n')
        for i in a_1:
            l = []
            for j in i:
                if j == '0':
                    l.append(0)
                else:
                    l.append(1)
            self.map_data.append(l)
        if reverse == True:
            self.map_data.reverse()
        self.init_pher(self.pher_init)  #初始化信息素浓度
    
    def init_pher(self,pher_init):
        self.pher_data = pher_init*np.ones(shape=[self.map_lenght*self.map_lenght,self.map_lenght*self.map_lenght])
        self.pher_data = self.pher_data.tolist()


        
    def run(self):
        #总迭代开始
        for i in range(self.max_iter):      
            success_way_list = []
            print('第',i,'代: ',end = '')
            #Step 1:当代若干蚂蚁依次行动
            for j in range(self.ant_num):   
                ant = Ant(max_step=self.map_lenght*3,pher_imp=self.ant_params['pher_imp'],dis_imp=self.ant_params['dis_imp'])
                ant.run(map_data=copy.deepcopy(self.map_data),pher_data=self.pher_data)
                if ant.successful == True:  #若成功，则记录路径信息
                    success_way_list.append(ant.record_way)
            print(' 成功率:',len(success_way_list),end= '')
            #Step 2:计算每条路径对应的长度，后用于信息素的生成量
            way_lenght_list = []
            for j in success_way_list:
                way_lenght_list.append(self.calc_total_lenght(j))
            #Step 3:更新信息素浓度
            #  step 3.1: 挥发
            self.pher_data = np.array(self.pher_data)
            self.pher_data = self.evaporate*self.pher_data
            self.pher_data = self.pher_data.tolist()
            #  step 3.2: 叠加新增信息素
            for k,j in enumerate(success_way_list):
                for t in range(len(j)-1):
                    self.pher_data[j[t][0]*self.map_lenght+j[t][1]][j[t+1][0]*self.map_lenght+j[t+1][1]] += self.ant_gener_pher/way_lenght_list[k]
            #Step 4: 当代的首尾总总结工作
            self.generation_aver.append(average(way_lenght_list))
            self.generation_best.append(min(way_lenght_list))
            if self.way_len_best>min(way_lenght_list):
                a_1 = way_lenght_list.index(min(way_lenght_list))
                self.way_len_best = way_lenght_list[a_1]
                self.way_data_best = copy.deepcopy(success_way_list[a_1])
            print('平均长度:',average(way_lenght_list),'最短:',min(way_lenght_list))
            

    
    def calc_total_lenght(self,way):
        lenght = 0
        for j1 in range(len(way)-1):
            a1 = abs(way[j1][0]-way[j1+1][0])+abs(way[j1][1]-way[j1+1][1])
            if a1 == 2:
                lenght += 1.41421
            else:
                lenght += 1
        return lenght




#############################################################################################################
            

class ShanGeTu():
    def __init__(self,map_path = 'map.dll',reverse = False):
        self.grid_size = 0
        self.cell_size = 0
        self.line_size = 0
        self.load_map(map_path,reverse = reverse)                        #读取地图数据
        self.pic_backgroud = self.backgroud()  #画网格
        self.draw_barrier()                    #画障碍物方格，跟上一步共同组合成完整的背景图片
        #self.draw_way(way_data=way_data)
        #self.save()                            #保存起来
        
    def backgroud(self):
        '''
            Function:
            ---------
                绘制栅格图的背景(即不包含路径线条的栅格图),并以返回Surface形式返回

            Params:
            -------
                None

            Return:
            -------
                backgroud : pygame.Surface
                    栅格图背景
        '''
        size = self.grid_size
        if size == 20:
            self.cell_size = 25
            self.line_size = 1
            pic_size = size*self.cell_size+(size+1)*self.line_size
            self.backgroud_size = pic_size
            backgroud = py.Surface([pic_size,pic_size])
            backgroud.fill([255,255,255])
            for i in range(size+1):
                py.draw.line(backgroud,[0,0,0],[i*(self.cell_size+self.line_size),0],[i*(self.cell_size+self.line_size),pic_size])
                py.draw.line(backgroud,[0,0,0],[0,i*(self.cell_size+self.line_size)],[pic_size,i*(self.cell_size+self.line_size)])
            return backgroud
        elif size == 30:
            self.cell_size = 15
            self.line_size = 1
            pic_size = size*self.cell_size+(size+1)*self.line_size
            self.backgroud_size = pic_size
            backgroud = py.Surface([pic_size,pic_size])
            backgroud.fill([255,255,255])
            for i in range(size+1):
                py.draw.line(backgroud,[0,0,0],[i*(self.cell_size+self.line_size),0],[i*(self.cell_size+self.line_size),pic_size])
                py.draw.line(backgroud,[0,0,0],[0,i*(self.cell_size+self.line_size)],[pic_size,i*(self.cell_size+self.line_size)])
            return backgroud

    def load_map(self,map_path,reverse = False):
        '''
        Function:
        ---------
            读取map数据存于self.map_data，数据为0-1矩阵，位置同栅格图节点位置，默认左上角为起点，右下角为终点。
        
        Params:
        -------
            None
        
        Return:
        -------
            None
        '''
        with open(map_path,'r') as f:
            self.map_data = f.readlines()
        for k,i in enumerate(self.map_data):
            self.map_data[k]= i.strip('\n')
        if reverse == True:
            self.map_data.reverse()
        self.grid_size = len(self.map_data[0])

    def draw_barrier(self):
        for i in range(len(self.map_data[0])):
            for j in range(len(self.map_data[0])):
                if self.map_data[i][j] == '1':
                    x_1 = (j+1)*self.line_size + j*self.cell_size
                    y_1 = (i+1)*self.line_size + i*self.cell_size
                    py.draw.rect(self.pic_backgroud,[0,0,0],[x_1,y_1,self.cell_size,self.cell_size])

    def draw_way(self,way_data):
        self.pic_shangetu = self.pic_backgroud.copy()
        # 转换成二维坐标格式
        way_data_1 = way_data
        '''
        一维格式
        way_data_1 = []
        for i in way_data:
            way_data_1.append([i%self.grid_size,i//self.grid_size])
        '''
        # 画线喽
        for k,i in enumerate(way_data_1):
            try:
                j = way_data_1[k+1]
            except:
                return None
            point_1_y = (i[0]+1)*self.line_size + i[0]*self.cell_size+self.cell_size/2
            point_1_x = (i[1]+1)*self.line_size + i[1]*self.cell_size+self.cell_size/2
            point_2_y = (j[0]+1)*self.line_size + j[0]*self.cell_size+self.cell_size/2
            point_2_x = (j[1]+1)*self.line_size + j[1]*self.cell_size+self.cell_size/2
            # 下面两行起到上下翻转的目的
            #point_1_y = self.backgroud_size - point_1_y
            #point_2_y = self.backgroud_size - point_2_y
            py.draw.line(self.pic_shangetu,[0,0,0],[point_1_x,point_1_y],[point_2_x,point_2_y],2)
                
    def save(self,filename = '栅格图.jpg',reverse = False):
        '''
            Function:
            ---------
                将画好的栅格图存储起来。

            Params:
            -------
                文件存放路径(含文件名)
        '''
        
        try:
            if  reverse == True:
                self.pic_shangetu = flip(self.pic_shangetu,False,True)
            py.image.save(self.pic_shangetu,filename)
        except:
            if  reverse == True:
                self.pic_backgroud = flip(self.pic_backgroud,False,True)
            py.image.save(self.pic_backgroud,filename)

    def seek_corner_point(self,way_data = [1,2,3,4]):
        '''
            Function:
            ---------
                找到所有的变异点，并返回。
            
            Params:
            -------
                way_data : list
                    路径的节点列表

            Return:
            -------
                special_pot_list : list
                    可疑节点信息列表，元素为数值则为转折点，否则若为size=2列表，则为擦边点。
                special_pot_key_list : list
                    节点标记信息，元素为1，2 
        '''
        #Step 1:找到转折点，以及擦边点，统称变异点，转折点用1标记，擦边点用2标记
        a_1 = way_data[1]-way_data[0]    # 通过分析两节点之间的数值差的变化，来得到转折点信息。
        special_pot_list = [0]                #存放变异点的列表,初始添加起点
        special_pot_key_list = [1]
        for i in range(len(way_data)-1):
            if way_data[i+1]-way_data[i] != a_1:   # 数值差不一样了
                special_pot_list.append(way_data[i])
                special_pot_key_list.append(1)
                a_1 = way_data[i+1]-way_data[i]
                if self.is_near_obstacle(way_data[i],way_data[i+1]):
                    special_pot_list.append([way_data[i],way_data[i+1]])
                    special_pot_key_list.append(2)
        special_pot_list.append((self.grid_size**2)-1)
        special_pot_key_list.append(1)
        print(special_pot_list)
        print(special_pot_key_list)
        return special_pot_list, special_pot_key_list

    def is_near_obstacle(self,point_a,point_b):
        '''
            Function:
            ---------
                用来判定某段路径是否擦肩而过障碍物，该函数仅被设计供sek_corner_point方法使用。
            
            Params:
            -------
                point_a:    int
                    起始节点
                point_b:    int
                    终止节点
            
            Return:
            -------
                result：True or False
        '''
        point_a_x,point_a_y = point_a % self.grid_size, point_a // self.grid_size
        point_b_x,point_b_y = point_b % self.grid_size, point_b // self.grid_size
        if (point_a_x==point_b_x) or (point_a_y == point_b_y):  # 同行或同列直接略过
            return False
        elif (point_b_x == point_a_x + 1):   #水平方向向右(下面的代码中关于y坐标的运算中使用了“self.grid_size-1”，因为列表序数方向是从上往下，而我们对栅格图的y方向定为自下而上)
            if (point_b_y == point_a_y + 1):  #垂直方向向下
                if (self.map_data[self.grid_size-1-(point_a_y+1)][point_a_x] == '1') or(self.map_data[self.grid_size-1-point_a_y][point_a_x+1] == '1'):
                    return True
                else:
                    return False
            else:                             #垂直向上
                if (self.map_data[self.grid_size-1-point_a_y-1][point_a_x] == '1') or(self.map_data[self.grid_size-1-point_a_y][point_a_x+1] == '1'):
                    return True
                else:
                    return False
        elif (point_b_x == point_a_x - 1):   #水平方向向左
            if (point_b_y == point_a_y + 1):  #垂直方向向下
                if (self.map_data[self.grid_size-1-(point_a_y+1)][point_a_x] == '1') or(self.map_data[self.grid_size-1-point_a_y][point_a_x-1] == '1'):
                    return True
                else:
                    return False
            else:                             #垂直向上
                if (self.map_data[self.grid_size-1-(point_a_y-1)][point_a_x] == '1') or(self.map_data[self.grid_size-1-point_a_y][point_a_x-1] == '1'):
                    return True
                else:
                    return False
            
    def calc_abs_x_y(self,point_data = 0):
        '''
            Function:
            ---------
                计算转折点或擦边点的像素坐标。
            
            Params:
                point_data : int or list
                    int时为转折点，list时为擦边点

            Return:
                [x,y] : [int,int]
                    像素坐标值
        '''
        if type(point_data) == int:
            x,y = point_data%self.grid_size,point_data//self.grid_size
            x = x*self.cell_size + (x+1)*self.line_size + self.cell_size//2+1
            y = y*self.cell_size + (y+1)*self.line_size + self.cell_size//2+1
            return x,y
        elif type(point_data) == list:
            x_1,y_1 = point_data[0]%self.grid_size,point_data[0]//self.grid_size
            x_1 = x_1*self.cell_size + (x_1+1)*self.line_size + self.cell_size//2+1
            y_1 = y_1*self.cell_size + (y_1+1)*self.line_size + self.cell_size//2+1

            x_2,y_2 = point_data[1]%self.grid_size,point_data[1]//self.grid_size
            x_2 = x_2*self.cell_size + (x_2+1)*self.line_size + self.cell_size//2+1
            y_2 = y_2*self.cell_size + (y_2+1)*self.line_size + self.cell_size//2+1

            x = abs(x_1 - x_2)//2 + min(x_1,x_2)
            y = abs(y_1 - y_2)//2 + min(y_1,y_2)
            return x,y

    def opti_way(self, way_data = [1,2,3,4]):
        #Step 1:找到转折点，以及擦边点，统称变异点
        a_1,b_1 = self.seek_corner_point(way_data=way_data)
        #Step 2:计算其绝对像素坐标，并打印出来看看
        print('a_1：',a_1)
        print('b_1：',b_1)

        abs_xy_list = []
        try:
            for i in a_1:
                x,y = self.calc_abs_x_y(point_data=i)
                py.draw.circle(self.pic_shangetu,[50,100,200],[x,self.backgroud_size - y],3)
                abs_xy_list.append([x,y])
        except:
            self.pic_shangetu = self.pic_backgroud.copy()
            for i in a_1:
                x,y = self.calc_abs_x_y(point_data=i)
                abs_xy_list.append([x,y])
            #self.draw_pot(x,y)
        # Step 3: 优化
        running = True
        i = 0
        while running:
            if b_1[i+1] == 2:
                print(abs_xy_list[i],abs_xy_list[i+1],abs_xy_list[i+2],'中间点为擦边点！')
                pass    
            else:
                result = self.trigon_opt(abs_xy_list[i],abs_xy_list[i+1],abs_xy_list[i+2],b_1[i:i+3])
                if result == None:
                    print(abs_xy_list[i],abs_xy_list[i+1],abs_xy_list[i+2],'能直接连接！')
                    del abs_xy_list[i+1]
                    del b_1[i+1]
                    i -= 1
                else:
                    print(abs_xy_list[i],abs_xy_list[i+1],abs_xy_list[i+2],'不能直接连接！,添加新节点')
                    if result in abs_xy_list:
                        pass
                    else:
                        abs_xy_list = abs_xy_list[0:i+1]+ [result]+abs_xy_list[i+1:]
                        b_1 = b_1[0:i+1] + [1] + b_1[i+1:]
                    

            i += 1
            if i >= len(abs_xy_list)-2:
                break  
        print('优化后的abs_xy_list:',abs_xy_list)
        # Step 4: 画出优化的线
        self.final_opt_way = abs_xy_list
        for i in abs_xy_list:
            x,y = i[0],i[1]
            py.draw.circle(self.pic_shangetu,[255,150,50],[x,self.backgroud_size - y],3)
        for i in range(len(abs_xy_list)-1):
            py.draw.line(self.pic_shangetu,[255,150,50],[abs_xy_list[i][0],self.backgroud_size-abs_xy_list[i][1]],[abs_xy_list[i+1][0],self.backgroud_size-abs_xy_list[i+1][1]],3)

        #self.save('栅格图优化.jpg')
        
    def trigon_opt(self,pot_1,pot_2,pot_3,key_list):
        '''
            Function:
            --------
                三角形优化，形象的来看，就是把pot_1, pot_2, pot_3组成的三角形尽可能地变得扁。
            
            Params:
            -------
                pot_1 : [int,int]
                    第一点的坐标，pot_2 ,pot_3同
                key_list : list , size = 3
                    三个点的类型标记

            Return:
            -------
                pot: [int,int] or None
                若pot为None，则代表可疑直连，否则pot为三角的极限顶点。
        '''

        result = self.is_accross_barrier(pot_1,pot_3)
        if result[0] == True:
            pot = self.deep_opt(pot_1,pot_2,pot_3)
            #input('wait for ldd...')
            return pot

        else:
            return None
       
    def is_accross_barrier(self,pot_1 ,pot_2):
        '''
            Function:
            ---------
                判断两点之间有否有障碍物存在。微元法，步进尺寸为L/50
        '''
        #if pot_1 == [321,449]:
        #    print('1')
        deta_x = (pot_2[0]-pot_1[0])/50
        deta_y = (pot_2[1]-pot_1[1])/50
        for i in range(1,51):      #步进100个点判断
            x = pot_1[0]+int(deta_x*i)
            y = pot_1[1]+int(deta_y*i)
            if (x-self.line_size)%(self.cell_size+self.line_size) == 0:  #点正好在直线上，故不用考虑这个点了
                continue
            else:                                      #若不在直线上，则需判断它在哪列
                for i_1 in range(0,self.grid_size):
                    a_1 = i_1*self.cell_size+(i_1+1)*self.line_size
                    if a_1<x<=a_1+self.cell_size:
                        x_1 = i_1
                        break
            if (y-self.line_size)%(self.cell_size+self.line_size) == 0:  #点正好在直线上，故不用考虑这个点了
                continue
            else:                                      #若不在直线上，则需判断它在哪列
                for i_1 in range(0,self.grid_size):
                    a_1 = i_1*self.cell_size+(i_1+1)*self.line_size
                    if a_1<y<=a_1+self.cell_size:
                        y_1 = i_1
                        break 
            if self.map_data[self.grid_size-1-y_1][x_1] == '1':         #判断该格子上是否障碍物，是的话就返回True
                print('判断节点:',x_1,y_1,'结果不可通行')
                return [True,[x_1,y_1]]
            #else:
            #    print('判断节点:',self.grid_size-1-y_1,x_1,'结果为可通行')
        return [False,[]]                                #100个点都判断完了，返回False

    def deep_opt(self,pot_1,pot_2,pot_3):
        '''
        function:
        ---------
        深度三角优化，找到越过障碍物的临界状态，并返回新的中间点。

        Params:
            pot_1,pot_2,pot_3 : [int,int]
                起点，中间点、终点

        Return:
            pot : [int, int]
        '''
        print(pot_1,pot_2,pot_3)
        pot_2_1 = [(pot_1[0]+pot_3[0])//2,(pot_1[1]+pot_3[1])//2]
        #pot_1[1] = self.backgroud_size - pot_1[1]
        #pot_2[1] = self.backgroud_size - pot_2[1]
        #pot_2_1[1] = self.backgroud_size - pot_2_1[1]
        #pot_3[1] = self.backgroud_size - pot_3[1]
        #py.draw.line(self.pic_shangetu,[0,0,255],pot_1,pot_3)
        #py.draw.line(self.pic_shangetu,[0,0,255],pot_2,pot_3)
        #py.draw.line(self.pic_shangetu,[0,0,255],pot_1,pot_2)
        #py.draw.line(self.pic_shangetu,[0,0,255],pot_2,pot_2_1)
        #py.draw.circle(self.pic_shangetu,[0,0,255],pot_2_1,3)
        STEP = 50
        deta_x = (pot_2_1[0]-pot_2[0])/STEP        #20步微元法找临界状态
        deta_y = (pot_2_1[1]-pot_2[1])/STEP
        for i in range(1,STEP+1):
            x_1 = pot_2[0] + int(deta_x*i)
            y_1 = pot_2[1] + int(deta_y*i)
            r_1 = self.is_accross_barrier(pot_1,[x_1,y_1])
            r_2 = self.is_accross_barrier([x_1,y_1],pot_3)
            if r_1[0]:
                #print('找到临界障碍物:',r_1[1])
                new_pot_2 = self.seek_shortest_vertice(r_1[1],pot_1,[x_1,y_1],pot_3)
                py.draw.circle(self.pic_shangetu,[255,0,0],[new_pot_2[0],self.backgroud_size - new_pot_2[1]],3)
                #self.save()
                #input('wait...')
                return new_pot_2
            elif r_2[0]:
                #print('找到临界障碍物:',r_2[1])
                new_pot_2 = self.seek_shortest_vertice(r_2[1],pot_1,[x_1,y_1],pot_3)
                py.draw.circle(self.pic_shangetu,[255,0,0],[new_pot_2[0],self.backgroud_size - new_pot_2[1]],3)
                #self.save()
                #input('wait...')
                return new_pot_2
            else:
                pass
                #print('继续...')
        #self.save()
    
    def seek_shortest_vertice(self,grid,pot_1,pot_2,pot_3):
        # Step 1: 先找到四个顶点坐标
        x = grid[0]
        y = grid[1]
        vertices = []
        vertices.append([x*self.cell_size+(x+1)*self.line_size,y*self.cell_size+(y+1)*self.line_size])  #左下角点
        vertices.append([x*self.cell_size+(x+1)*self.line_size,(y+1)*self.cell_size+(y+2)*self.line_size])  #左上角点
        vertices.append([(x+1)*self.cell_size+(x+2)*self.line_size,y*self.cell_size+(y+1)*self.line_size])  #右下角点
        vertices.append([(x+1)*self.cell_size+(x+2)*self.line_size,(y+1)*self.cell_size+(y+2)*self.line_size])  #左下角点
        yuzhi = 99999 
        key = 0
        v1 = [pot_2[0]-pot_1[0],pot_2[1]-pot_1[1]]
        v2 = [pot_2[0]-pot_3[0],pot_2[1]-pot_3[1]]
        for k,i in  enumerate(vertices):
            v1_1 = [i[0]-pot_1[0],i[1]-pot_1[1]]
            v2_1 = [i[0]-pot_3[0],i[1]-pot_3[1]]
            s_1 = abs(v1_1[0]*v1[1]-v1_1[1]*v1[0])
            s_2 = abs(v2_1[0]*v2[1]-v2_1[1]*v2[0])
            print(k,s_1,s_2)
            s = min(s_1,s_2)
            if s<yuzhi:
                key = k
                yuzhi = s
        return vertices[key]
    def calc_way_lenght(self):
        self.way_lenght = 0
        for i in range(len(self.final_opt_way)-1):
            a_1 = self.final_opt_way[i]
            b_1 = self.final_opt_way[i+1]
            self.way_lenght += (((a_1[0]-b_1[0])**2)+((a_1[1]-b_1[1])**2))**0.5
        self.way_lenght = self.way_lenght/self.cell_size







        
        



        
        

        



