import pygame as pg 
pg.init() 

#бэкграунд
mw = pg.display.set_mode((500, 500)) 
background = (200, 255, 255)             
mw.fill(background)                      

clock = pg.time.Clock()            
game_over = False                      

#классы для игр
class Area():                           
    def __init__(self, x=0, y=0, width=10, height=10, color=None):
        self.rect = pg.Rect(x, y, width, height)     #прямоугольная область   
        self.fill_color = background
        if color:
            self.fill_color = color
    
    def color(self, new_color):        
        self.fill_color = new_color
    
    def fill(self):                    
        pg.draw.rect(mw, self.fill_color, self.rect)
    
    def collidepoint(self, x, y):      
        return self.rect.collidepoint(x, y) #координаты столкновения объектов     
    
    def colliderect(self, rect):       
        return self.rect.colliderect(rect) #определение столкновения объектов


class Picture(Area):                   
    def __init__(self, filename, x=0, y=0, width=10, height=10):
        Area.__init__(self, x=x, y=y, width=width, height=height, color=None)
        self.image = pg.image.load(filename)    
    
    def draw(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))


class Label(Area):
    def set_text(self, text, fsize=12, text_color=(0, 0, 0)):  
        self.image = pg.font.SysFont('verdana', fsize).render(text, True, text_color)
    
    def draw(self, shift_x=0, shift_y=0):            
        self.fill()
        mw.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))


platform_x = 200   
platform_y = 350    
platform = Picture('platform.png', platform_x, platform_y, 100, 30)
move_right = False 
move_left = False  

ball_x = 160      
ball_y = 200       
ball = Picture('ball.png', ball_x, ball_y, 50, 50)
ball_speed_x = 3   
ball_speed_y = 3   

n = 9              
x = 5              
y = 5               
enemys = []          
for i in range(3):  
    enemy_y = y + (55 * i)   
    enemy_x = x + (27 * i)   
    for i in range(n):
        enemy = Picture('enemy.png', enemy_x, enemy_y, 50, 50)
        enemys.append(enemy)   
        enemy_x += 55
    n -= 1


while not game_over:   
    ball.fill()
    platform.fill()

    for event in pg.event.get():        
        if event.type == pg.KEYDOWN:  
            if event.key == pg.K_RIGHT:
                move_right = True
            if event.key == pg.K_LEFT:
                move_left = True
        
        elif event.type == pg.KEYUP:    
            if event.key == pg.K_RIGHT:
                move_right = False
            if event.key == pg.K_LEFT: 
                move_left = False
    
    if move_left:
        platform.rect.x -= 3               
    if move_right:
        platform.rect.x += 3                

    ball.rect.x += ball_speed_x             
    ball.rect.y += ball_speed_y             
    
    if ball.rect.y < 0:
        ball_speed_y *= -1                 
    
    if ball.rect.x > 450 or ball.rect.x < 0:    
        ball_speed_x *= -1                  
    
    if ball.rect.colliderect(platform.rect):
        ball_speed_y *= -1               
    
    ball.draw()                           
    platform.draw()                         

    if len(enemys) == 0:                    
        final_text = Label(150, 250, 50, 50, background)
        final_text.set_text('YOU WIN', 60, (0, 255, 0))
        final_text.draw()
        game_over = True                 
    
    if ball.rect.y > 350:
        final_text = Label(150, 250, 50, 50, background)
        final_text.set_text('YOU LOSE', 60, (255, 0, 0))
        final_text.draw()
        game_over = True                    
    
    for enemy in enemys:                      
        enemy.draw()                          
        if enemy.rect.colliderect(ball.rect): 
            enemys.remove(enemy)            
            enemy.fill()
            ball_speed_y *= -1             
    
    clock.tick(40)                         
    pg.display.update()        