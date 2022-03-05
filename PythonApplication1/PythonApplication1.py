import pygame

BG = pygame.image.load('fon.jpg')


#класс Игрок
class Player(pygame.sprite.Sprite):
    #первоначальное направление вправо
    right = True

    #методы
    #стандартный конструктор класса
    def __init__(self):
        super().__init__()

        #спрайт игрока
        self.image = pygame.image.load('человек лево 1.png')
        #устанавливаем ссылку
        self.rect = self.image.get_rect()

        #вектор скорости игрока
        self.change_x = 0
        self.change_y = 0

    #передвижение игрока
    def update(self):
        #устанавливаем гравитацию
        self.calc_grav()
        #передвигаем в лево/право
        self.rect.x += self.change_x

        #проверям на столкновение с какими-либо объектами
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        #перебираем каждый объект, с которыми могли столкнуться
        for block in block_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right

        #передвигаемся вверх/вниз
        self.rect.y += self.change_y
		#вверх/вниз
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
            #останавливаем вертикальное движение
            self.change_y = 0

    def calc_grav(self):
		#скорость падения на землю под действием гравитации
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .95

		#если уже на земле, то ставим позицию y как 0
        if self.rect.y >= win_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = win_HEIGHT - self.rect.height

    def jump(self):
		#обработка прыжка
        self.rect.y += 10
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 10

		#если в данный момент прыжка не происходит, то прыжок возможен
        if len(platform_hit_list) > 0 or self.rect.bottom >= win_HEIGHT:
            self.change_y = -16

    # Передвижение игрока
    def go_left(self):
		# Сами функции будут вызваны позже из основного цикла
        self.change_x = -9 # Двигаем игрока по Х
        if(self.right): # Проверяем куда он смотрит и если что, то переворачиваем его
            self.flip()
            self.right = False

    def go_right(self):
		# то же самое, но вправо
        self.change_x = 9
        if (not self.right):
            self.flip()
            self.right = True


    def stop(self):
		# вызываем этот метод, когда не нажимаем на клавиши
        self.change_x = 0

    def flip(self):
		# переворот игрока (зеркальное отражение)
        self.image = pygame.transform.flip(self.image, True, False)








#класс платформы
class Platform(pygame.sprite.Sprite):
    def __init__(self, width, heidth):
        super().__init__()
        #загружаем изображение платформы
        self.image = pygame.image.load('platform.png')
        #ссылка на изображение прямоугольника
        self.rect = self.image.get_rect()


#класс для распрежеления платформ в сцене
class Levels(object):
    def __init__(self, player):
        #группа загруженных спрайтов платформ
        self.platform_list = pygame.sprite.Group()
        #ссылка на игрока
        self.player = player

    #обновление экрана
    def update(self):
        self.platform_list.update()

    #рисование платформ и фона
    def draw(self, win):
        win.blit(BG,(0,0))
        self.platform_list.draw(win)


#класс платформ на определенном уровне игры
class Level(Levels):
    def __init__(self, player):
        Levels.__init__(self, player)

        #данные по расположению платформ:
        #ширина, высота, x, y
        level = [[210,32,500,500],
                 [210,32,500,500],
                 [210,32,500,500],]

        for platform in Levels:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)


#класс стрельба
class Shell():
    def __init__(self, x, y, radius, color, direction):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.direction = direction
        self.v = 8*direction

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)





#основная функция
def main():
    #инициализируем библиотеку
    pygame.init()
    
    #задаем поле
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    win = pygame.display.set_mode(size)  
    
    #называем окно
    pygame.display.set_caption("Game")  

    #создание игрока
    player = Player()   

    #создаем уровни
    level_list = []
    level_list.append(Level(player))

    #обозначаем текущий уровень
    current_level_no = 0
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    player.rect.x = 340
    player.rect.y = 500 - player.rect.height
    active_sprite_list.add(player)

    #работа до выхода из игры
    quit = False

    #часы для управления скоростью обновления экрана
    clock = pygame.time.Clock()




#рисуем окно
def drawWindow():
    global animCount    #счетчик кадров
    win.blit(BG,(0,0))

    if animCount+1 >= 15:   #15 сек
        animCount = 0

    if left:
        win.blit(walkLeft[animCount//5], (x,y))
        animCount +=1
    elif right:
        win.blit(walkRight[animCount//5], (x,y))
        animCount +=1
    else:
        win.blit(playerStop, (x,y))

    for bullet in bullets:
        bullet.draw(win)

    
    #pygame.draw.rect(win,(0,0,255),(x,y,widht,heidht))
    pygame.display.update()



#основной цикл
while not quit:
    #условие выхода
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            quit = True

# Если нажали на стрелки клавиатуры, то двигаем объект
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.go_left()
            if event.key == pygame.K_RIGHT:
                player.go_right()
            if event.key == pygame.K_UP:
                player.jump()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and player.change_x < 0:
                player.stop()
            if event.key == pygame.K_RIGHT and player.change_x > 0:
                player.stop()



    # Обновляем игрока
    active_sprite_list.update()

		# Обновляем объекты на сцене
    current_level.update()

		# Если игрок приблизится к правой стороне, то дальше его не двигаем
    if player.rect.right > SCREEN_WIDTH:
        player.rect.right = SCREEN_WIDTH

		# Если игрок приблизится к левой стороне, то дальше его не двигаем
    if player.rect.left < 0:
        player.rect.left = 0

		# Рисуем объекты на окне
    current_level.draw(screen)
    active_sprite_list.draw(screen)

		# Устанавливаем количество фреймов
    clock.tick(30)

		# Обновляем экран после рисования объектов
    pygame.display.flip()

# Корректное закртытие программы
pygame.quit()

