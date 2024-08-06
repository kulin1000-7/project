# Крестики нолики


# Поле
Set_app =[
  [1, 2, 3],
  [4, 5, 6],
  [7, 8, 9]
]
count = 0
def game_board(Set_app):
  for i in Set_app:
    print(i)

def game():
  won = check_win(Set_app)
  game_board(Set_app)
  global count
  count += 1
  if not any(d) == True and count < 5:
    x = int(input('Ходит игрок Х,укажите кординаты хода '))
    f_move(x)

    check_win(Set_app)
    print(game_board(Set_app))

    x = int(input('Ходит игрок 0,укажите кординаты хода '))
    s_move(x)

    check_win(Set_app)
    print(game_board(Set_app))

    print(count)
    game()


  else:
      print('game is over')


def f_move(x):
  if x == 9:
    j = 2
    k = 2
    if Set_app[j][k] != 'X' and Set_app[j][k] !='0':
      Set_app[j][k] = 'X'

    else:
      print('Ход невозможен')
  elif x == 3:
    j = 0
    k = 2

    if Set_app[j][k] != 'X' and Set_app[j][k] !='0':
      Set_app[j][k] = 'X'

    else:
      print('Ход невозможен')
  elif x == 6:
    j = 1
    k = 2
    if Set_app[j][k] != 'X' and Set_app[j][k] !='0':
      Set_app[j][k] = 'X'

    else:
      print('Ход невозможен')
  else:
    j = x // 3
    k = x % 3 - 1
    if Set_app[j][k] != 'X' and Set_app[j][k] !='0':
      Set_app[j][k] = 'X'

    else:
      print('Ход невозможен')


#Ход второго
def s_move(x):
  if x == 9:
    j = 2
    k = 2
    if Set_app[j][k] != 'X' and Set_app[j][k] !='0':
      Set_app[j][k] = '0'

    else:
      print('Ход невозможен')
  elif x == 3:
    j = 0
    k = 2

    if Set_app[j][k] != 'X' and Set_app[j][k] !='0':
      Set_app[j][k] = '0'

    else:
      print('Ход невозможен')

  elif x == 6:
    j = 1
    k = 2
    if Set_app[j][k] != 'X' and Set_app[j][k] !='0':
      Set_app[j][k] = '0'

    else:
      print('Ход невозможен')
  else:
    j = x // 3
    k = x % 3 - 1
    if Set_app[j][k] != 'X' and Set_app[j][k] !='0':
      Set_app[j][k] = '0'

    else:
      print('Ход невозможен')

def check_win(Set_app):

    v0 = (Set_app[0][0] == Set_app[0][1] == Set_app[0][2])
    v1 = (Set_app[1][0] == Set_app[1][1] == Set_app[1][2])
    v2 = (Set_app[2][0] == Set_app[2][1] == Set_app[2][2])

    g0 = (Set_app[0][0] == Set_app[1][0] == Set_app[2][0])
    g1 = (Set_app[0][1] == Set_app[1][1] == Set_app[2][1])
    g2 = (Set_app[0][2] == Set_app[1][2] == Set_app[2][2])

    d0 = (Set_app[0][0] == Set_app[1][1] == Set_app[2][2])
    d1 = (Set_app[0][2] == Set_app[1][1] == Set_app[2][0])
    global d
    d = [v0,v1,v2,g0,g1,g2,d0,d1]

    if not any(d) == False:
        return 'Игра закончена'
    else:
        pass




game()

