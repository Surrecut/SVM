import pygame
import random
# инициализация Pygame
pygame.init()

# Переменные для работы функций
FPS = 30  # Количество кадров в секунду
ship_speed = 10  # скорость корабля
enemy_speed = 3  # скорость врагов
bullet_speed = 10  # скорость пули
len_enemies = 10  # кол-во врагов
player_size = 64  # размер корабля
score = 0
score_win = 20
score_lose = -5
# Шрифт и его размер
font = pygame.font.Font(None, 100)

# задаем размер и изображение заднего фона
screen_x = 1920
screen_y = 1080
screen = pygame.display.set_mode((screen_x, screen_y))
background_image = pygame.image.load(r'C:\Users\1\Desktop\SVM\Pictures\BackGround.jpg')

# загрузка изображения космического корабля
player_img = pygame.image.load(r'C:\Users\1\Desktop\SVM\Pictures\player.png')
player_width = player_size
player_height = player_size

# загрузка изображения вражеского корабля
enemy_img = pygame.image.load(r'C:\Users\1\Desktop\SVM\Pictures\enemy.png')
enemy_width = 115
enemy_height = 100

# загрузка изображения пули
bullet_img = pygame.image.load(r'C:\Users\1\Desktop\SVM\Pictures\bullet.png')
bullet_width = 7
bullet_height = 16

# списоки врагов и пуль
enemies = []
bullets = []

# задаем начальное положение космического корабля
player_x = screen_x // 2 - player_width - 100
player_y = screen_y - player_height - 200

# прямоугольник корабля
player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
player_rect.clamp_ip(pygame.Rect(0, 0, screen_x, screen_y))
player_x, player_y = player_rect.x, player_rect.y

# прямоугольник заднего фона
background_rect = background_image.get_rect()


# функция для создания вражеских кораблей

def create_enemy():
    enemy_x = random.randint(-screen_x, screen_x)
    enemy_y = random.randint(-1000, -enemy_height)
    enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
    enemy_hitbox = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
    enemies.append([enemy_x, enemy_y, enemy_rect, enemy_hitbox])


# функция для создания пуль
def create_bullet():
    bullet_x = player_x + 6.5
    bullet_y = player_y
    bullet_rect = pygame.Rect(bullet_x, bullet_y, bullet_width, bullet_height)
    bullet_hitbox = pygame.Rect(bullet_x, bullet_y, bullet_width, bullet_height)
    bullets.append([bullet_x, bullet_y, bullet_rect, bullet_hitbox])


def draw_objects():
    # отрисовка заднего фона
    screen.blit(background_image, background_rect)

    # отрисовка космического корабля
    screen.blit(player_img, (player_x, player_y))

    # отрисовка вражеских кораблей
    for enemy in enemies:
        screen.blit(enemy_img, (enemy[0], enemy[1]))

    # отрисовка снарядов и проверка столкновений
    for bullet in bullets:
        bullet_rect = pygame.Rect(bullet[0] + 163, bullet[1] + 52, bullet_width, bullet_height)
        screen.blit(bullet_img, (bullet[0], bullet[1]))

        for enemy in enemies:
            enemy_rect = pygame.Rect(enemy[0] + 220, enemy[1] + 240, enemy_width, enemy_height)

            # удаление врагов и пуль после столкновения
            if bullet_rect.colliderect(enemy_rect):
                bullets.remove(bullet)
                enemies.remove(enemy)
                global score
                score += 1


# основной игровой цикл
running = True
clock = pygame.time.Clock()
while running:
    # обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # создание нового снаряда на кнопку пробел
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_x = player_x + 6.5
                bullet_y = player_y
                bullets.append([bullet_x, bullet_y])
            # быстрое завершение игры
            elif event.key == pygame.K_ESCAPE:
                running = False

    # отрисовка объектов
    draw_objects()

    # счётчик уничтоженных врагов
    text = font.render(f"Score: {score}", True, (0, 80, 20))
    screen.blit(text, (screen_x - text.get_width() - 10, 100))

    # кнопки движения корабля влево и вправо соответственно
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_x -= ship_speed
    elif keys[pygame.K_d]:
        player_x += ship_speed

    # движение снарядов
    for bullet in bullets:
        bullet[1] -= bullet_speed

        # удаление за пределами экрана
        if bullet[1] < -bullet_height:
            bullets.remove(bullet)

        # ограничение количества пуль
        if len(bullets) > 3:
            bullets.remove(bullet)

    # создание ограниченного количества вражеских кораблей
    if len(enemies) < len_enemies:
        create_enemy()

    # движение врагов
    for enemy in enemies:
        enemy[1] += enemy_speed

        # удаление врагов за пределами экрана
        if enemy[1] > screen_y - 360:
            enemies.remove(enemy)
            score -= 1
        if enemy[0] > screen_x - 340:
            enemies.remove(enemy)
        if enemy[0] < screen_x - 2200:
            enemies.remove(enemy)

    # Функция для победы
    if score == score_win:
        running = False
        print("You win")

    # Функция для поражения
    if score == score_lose:
        running = False
        print("Game over")




    # ограничение количества кадров в секунду
    clock.tick(FPS)


    # обновление экрана
    pygame.display.flip()

# завершение Pygame
pygame.quit()