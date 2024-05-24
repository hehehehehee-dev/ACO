import pygame
import numpy as np

screen_width = 1200
screen_height = 800
move=0

class Screen:
    def __init__(self):
        self.screen = pygame.display.set_mode((screen_width,screen_height))
        #các giai đoạn
        self.mode = np.array(["setup", "create_matrix", "it's_aco_time"])
        self.loop = 100 # số con kiến 

        #mảng lưu vị trí các node
        self.arr = np.empty((10,), dtype='object') #10 là giới hạn mảng

        #mảng 2d lưu khoảng cách giữa các node ( với dis_matrix[i][j] là giữa node i và j của arr)
        self.dis_matrix = np.zeros((10,10))
        self.size = 0

        #mảng 2d các đường đi
        self.move = np.empty((10, 10), dtype=object)

        #mảng 2d pheromone
        self.pher_matrix = np.ones((10,10))

        #mảng 2d weight
        self.weight = np.ones((10,10))

        #mảng 2d prob
        self.prob = np.ones((10,10))


        self.pos=0
        self.alpha = 1
        self.beta = 1
        self.decay_speed = 0.1

        #mảng path 
        self.path = np.empty((10,), dtype='object')
        self.length = 0
        #ans
        self.ans = np.empty((10,), dtype='object')
        self.shortest = np.inf

        #màu
        self.white = (255,255,255)
        self.black = (0,0,0)
        self.gray = (169,169,169)

        self.dumme = 0 #dumme (dumb+me), not dummy 
        self.pos= 0
        self.rects_array = np.empty((10,), dtype=object)

    def Background(self):
        self.screen.fill(self.black)

    def Create_node(self, pos):
        #tạo node và lưu vào mảng chứa vị trí các node
        self.arr[self.size] = pos
        pygame.draw.circle(self.screen, self.white, pos, 5)
        #tạo rect để tránh các điểm quá gần nhau
        self.rects_array[self.size] = pygame.Rect(pos, (50,50))
        self.size +=1
    
    def Create_matrix(self):
        #tạo ra ma trận khoảng cách giữa 2 điểm bất kì
        self.move = np.empty((self.size, self.size), dtype=tuple)
        self.dis_matrix = np.zeros((self.size, self.size))
        for i in range(self.size):
            for j in range(i, self.size):
                # khoảng cách giữa 2 điểm bất kì * (0.5 => 1.5) ( ngẫu nhiên )
                if i == j:
                    self.dis_matrix[i][j] = np.inf # nếu cùng 1 điểm thì bỏ qua
                if i != j:
                    self.dumme = np.sqrt( (self.arr[i][0]-self.arr[j][0])**2 + (self.arr[i][1]-self.arr[j][1])**2 ) / 10
                    self.dis_matrix[i][j] = round( self.dumme * (np.random.random()+2.0) / 2, 2 ) # từ i -> j
                    self.dis_matrix[j][i] = round( self.dumme * (np.random.random()+2.0) / 2, 2 ) # từ j -> i
                    # vì np.random.random() chọn ra 1 giá trị bất kì trong khoảng 0->1 => khoảng cách * (2->3) /2
                    # chiều đi và về có thể khác nhau nên giá trị cx cho bừa khác nhau luôn :3
                    pygame.draw.line(self.screen, self.gray, self.arr[i], self.arr[j], width = 2 )
                self.move[i][j] = (i, j)
                self.move[j][i] = (j, i)
        print(self.dis_matrix)
        #ngol r
    
    #ACO part
    def ACO(self):
        self.path = np.empty((self.size,), dtype=tuple)
        self.pher_matrix = np.ones((self.size, self.size))
        self.Update_prob()
        # lặp n lần đống này
        #kiến bắt đầu ( vì trong thực tế thường mn hay bắt đầu từ nơi gần nhất nên sẽ cho luôn là từ self.arr[0])
        #kiến chọn đường theo pheromone
        #kiến đi đến 1 điểm mà chưa đi qua và thêm pheromone
        #hết điểm đi lại từ đầu và thêm pheromone
        #so sánh và lưu trữ đường đi ngắn nhất
        #cho pheromone chim cút
        for i in range(self.loop):
            self.length = 0
            self.pos = 0 
            for j in range(self.size-1):
                self.Select_move(j)
                
            #từ điểm cuối cùng được chọn đến điểm đầu    
            self.length = self.length + self.dis_matrix[self.pos][0]
            self.path[self.size-1] = (self.pos, 0)

            if self.shortest > self.length:
                self.shortest = self.length
                self.ans = self.path
            self.Update_pheromone()
            self.Update_prob()
        print(self.ans)
        print(self.shortest)
            
    
    def Select_move(self, curr_move):
        move = np.random.choice(self.move[self.pos] , p=self.prob[self.pos])

        #bỏ khả năng đi lại điểm bắt đầu và đi từ điểm bắt đầu

        for i in range(self.size):
            self.prob[self.pos][i] = 0 
            self.prob[i][self.pos] = 0 
        
        self.pos = int(move[1])

        self.length = self.length + self.dis_matrix[move[0]][move[1]]
        self.path[curr_move] = move

        #tính lại tỉ lệ
        for i in range(self.size):
            self.dumme = self.prob[i].sum()
            for j in range(self.size):
                if self.dumme != 0:
                    self.prob[i][j] /= self.dumme
        self.prob = np.nan_to_num(self.prob, nan=0.0)


    
        
        
    def Update_pheromone(self):
        for i in range(self.size):
            self.pher_matrix[self.path[i][0]] *= (1-self.decay_speed)
            self.pher_matrix[self.path[i][0]] += (1.0/self.length)

    def Update_prob(self):
        self.weight = (self.pher_matrix ** self.alpha) * ((1.0 / self.dis_matrix) ** self.beta)
        self.prob = self.weight / self.weight.sum(axis=1, keepdims=True) 
        # tỉ lệ tại điểm i đến 1 trong các điểm còn lại bất kì = trọng số của điểm đó ( 1 trong các điểm còn lại )/ tổng trọng số
        self.prob = np.nan_to_num(self.prob, nan=0.0)
        
        for i in range(self.size):
            for j in range(self.size):
                if self.prob[i].sum() ==0:
                    self.prob[i][j] = 0
                else:
                    self.prob[i][j] /= self.prob[i].sum()

        self.prob = np.nan_to_num(self.prob, nan=0.0)
        


            

        
    

    