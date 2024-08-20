from random import randint


class BoardOutException(Exception):

    def __init__(self, message=None):
        if message:
            self.message = message
        else:
            self.message = 'Выстрел за пределы поля !'


class SecShotException(Exception):

    def __init__(self, message=None):
        if message:
            self.message = message
        else:
            self.message = 'Повторный выстрел невозможен!'


class ShipAddException(Exception):

    def __init__(self, message=None):
        if message:
            self.message = message
        else:
            self.message = 'Корабль не может бать размещен !'


class RandomizeException(Exception):

    def __init__(self, message=None):
        if message:
            self.message = message
        else:
            self.message = 'Достигнут лимит подбора '


class Dot:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)


class Ship:
    SHIP_DIRECTION_VERT = 1
    SHIP_DIRECTION_HORIZ = 0
    SHIP_DESCRIPTION = {'1': 'однопалубный корабль', '2': 'двупалубный корабль', '3': 'трехпалубный корабль'}

    def __init__(self, head_dot, board_len, direction):
        self.head_dot = head_dot
        self.board_len = board_len
        self.direction = direction
        self.lives = board_len

    def hit(self):
        if self.lives > 0:
            self.lives -= 1

    @property
    def dots(self):
        result = []
        for i in range(self.board_len):
            if self.direction == Ship.SHIP_DIRECTION_HORIZ:
                new_dot = Dot(self.head_dot.x + i, self.head_dot.y)
            else:
                new_dot = Dot(self.head_dot.x, self.head_dot.y + i)
            result.append(new_dot)

        return result

    @property
    def stern_dot(self):
        if self.direction == Ship.SHIP_DIRECTION_VERT:
            return Dot(self.head_dot.x, self.head_dot.y + self.board_len - 1)
        else:
            return Dot(self.head_dot.x + self.board_len - 1, self.head_dot.y)

    @property
    def description(self):
        return Ship.SHIP_DESCRIPTION[str(self.board_len)]


class Board:
    EMPTY_SLOT = 'О'
    SHIP_SLOT = '■'
    DESTROY_SLOT = 'X'
    MISS_SLOT = 'T'
    CONTOUR = '*'

    def __init__(self, size):
        self.size = size
        self.ships = []
        self.ship_alive = 0
        self.ship_hide = False
        self._dots = [[self.EMPTY_SLOT for j in range(self.size)] for j in range(size)]

    def out(self, dot):
        return not(self.size > dot.x >= 0 and self.size > dot.y >= 0 and self.size > dot.x >= 0
                   and self.size > dot.y >= 0)

    def add_ship(self, new_ship):
        if self.out(new_ship.head_dot) or self.out(new_ship.stern_dot):
            raise ShipAddException
        for ship in self.ships:
            for dot in new_ship.dots:
                if (ship.stern_dot.x + 1) >= dot.x >= (ship.head_dot.x - 1) and \
                        (ship.stern_dot.y + 1) >= dot.y >= (ship.head_dot.y - 1):
                    raise ShipAddException
        for dot in new_ship.dots:
            self._dots[dot.y][dot.x] = self.SHIP_SLOT
        self.ships.append(new_ship)
        self.ship_alive += 1

    def print_board(self, hide_ship=False):
        print(' ', '|'.join([str(i) for i in range(self.size)]))
        for i in range(len(self._dots)):
            row = self._dots[i]
            if hide_ship:
                row = map(lambda sm: self.EMPTY_SLOT if sm == self.SHIP_SLOT else sm, row)
            print('{:d}|{:s}'.format(i, '|'.join(row)))

    def shot(self, shot_dot):
        if self.out(shot_dot):
            raise BoardOutException
        if self._dots[shot_dot.y][shot_dot.x] == self.DESTROY_SLOT \
                or self._dots[shot_dot.y][shot_dot.x] == self.MISS_SLOT:
            raise SecShotException
        else:
            for ship in self.ships:
                if shot_dot in ship.dots:
                    self._dots[shot_dot.y][shot_dot.x] = self.DESTROY_SLOT
                    ship.hit()
                    if ship.lives == 0:
                        self.ship_alive -= 1
                    return ship
        self._dots[shot_dot.y][shot_dot.x] = self.MISS_SLOT
        return None

    def contour(self, ship):
        if ship.direction == Ship.SHIP_DIRECTION_HORIZ:
            max_x = ship.board_len + 2
            max_y = 3
        else:
            max_x = 3
            max_y = ship.board_len + 2
        for y in range(max_y):
            for x in range(max_x):
                dot_x = ship.head_dot.x - 1 + x
                dot_y = ship.head_dot.y - 1 + y
                if self.size > dot_x >= 0 and self.size > dot_y >= 0\
                        and self._dots[dot_y][dot_x] == self.EMPTY_SLOT:
                    self._dots[dot_y][dot_x] = self.CONTOUR


class Player:

    def __init__(self, own_board, enemy_board):
        self.own_board = own_board
        self.enemy_board = enemy_board

    def ask(self):
        pass

    def move(self):

        def random_shot(interation):
            if interation == 0:
                raise RandomizeException('Конец игры. Нет точек для выстрела !')
            else:
                try:
                    dot = Dot(randint(0, self.enemy_board.size - 1), randint(0, self.enemy_board.size - 1))
                    print(f'\nВыстрел в точнку {dot} ...')
                    return self.enemy_board.shot(dot)
                except (BoardOutException, BoardOutException, SecShotException):
                    return random_shot(interation - 1)

        return random_shot(10000)


class User(Player):

    def ask(self):
        try:
            coord = list(map(int, input('\nВведите координаты цели в формате "X"-"пробел"-"Y": ').split()))
            shot_dot = Dot(coord[0], coord[1])
            return shot_dot
        except (IndexError, ValueError):
            print('Цель указана неверно!')
            self.ask()

    def move(self):
        try:
            return self.enemy_board.shot(self.ask())
        except (BoardOutException, SecShotException) as exception:
            print(exception.message)
            return self.move()


class Game:
    SHIPS_LIST = [3, 2, 2, 1, 1, 1, 1]

    def __init__(self):
        self.user_board = self.random_board(6)
        self.ai_board = self.random_board(6)
        self.user = User(self.user_board, self.ai_board)
        self.ai_player = Player(self.ai_board, self.user_board)

    def random_board(self, size):
        MAX_INTERATION = 10000
        board_interation = 0
        while True:
            new_board = Board(size)
            # Идем по списку размеров корбалей
            for length in Game.SHIPS_LIST:
                # Пытаемся разместить на поле случайный корабль MAX_INTERATION раз
                i = 0
                while i < MAX_INTERATION:
                    try:
                        head_dot = Dot(randint(0, size - 1), randint(0, size - 1))
                        new_board.add_ship(Ship(head_dot, length, randint(0, 1)))
                        break
                    except ShipAddException:
                        i += 1
            # Если все корабли созданы возрващаем доску
            if new_board.ship_alive == len(Game.SHIPS_LIST):
                return new_board
            else:
                # Если заполнить доску не получилось пытаемся создать доску еще MAX_INTERATION раз
                board_interation += 1
                if board_interation >= MAX_INTERATION:
                    raise RandomizeException

    def greet(self):
        print('\nМОРСКОЙ БОЙ')
        print('-'*20)
        print('\nНа поле 6х6 клеток размещается 7 кораблей - один трехпалубный, два двухпалубных  и четыре однопалубных')
        print('Расстановка кораблей на поле автоматическая в случайном порядке.')
        print('Вы ходите первым , далее соперник , ход по первого промаха')


    def loop(self):

        def print_boards():
            print('\nПоле игрока:')
            self.user_board.print_board()
            print('\nПоле компьютера:')
            self.ai_board.print_board(hide_ship=True)

        while True:
            while True:
                while self.user_board.ship_alive and self.ai_board.ship_alive:
                    print_boards()
                    ship = self.user.move()
                    if ship:
                        if not ship.lives:
                            print(f'\nПопал ! Вражеский {ship.description} уничтожен !')
                            self.ai_board.contour(ship)
                        else:
                            print('\nПопал ! Корабль противника подбит!')
                        if self.ai_board.ship_alive:
                            print('Отличная работа ! Стреляйте еще раз !')
                        else:
                            print('\nВы победили !')
                            break
                    else:
                        print('\nК сожалению вы промахнулись ! Компьютер наносит ответный удар ...')
                        break

                while self.user_board.ship_alive and self.ai_board.ship_alive:
                    ship = self.ai_player.move()
                    print_boards()
                    if ship:
                        if not ship.lives:
                            print(f'\nПопадание ! Ваш {ship.description} уничтожен !')
                        else:
                            print(f'\nПопадание ! Ваш {ship.description} подбит!')
                        if self.user_board.ship_alive:
                            pass

                        else:
                            print('\nВы проиграли !')
                            break
                    else:
                        print('\nВраг промахнулся ! Ваша очередь стрелять.')
                        input('Нажимет [ЕNTER] ... ')
                        break

                if not self.user_board.ship_alive or not self.ai_board.ship_alive:
                    break

            if input('\nПопробовать еще раз [y/n] ? : ').upper() == 'Y':
                self.user_board = self.random_board(6)
                self.ai_board = self.random_board(6)
            else:
                quit()

    def start(self):
        self.greet()
        self.loop()


game = Game()

game.start()
