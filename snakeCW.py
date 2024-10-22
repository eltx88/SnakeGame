# Game Resolution is 1280x720
from tkinter import Tk, Canvas, PhotoImage, Label, Button
from tkinter import *
from random import randint as rand
import time
import os

# Global Variables
width, height = 1280, 720
snake = []
snakeS = 30
speed = 80
speedDisp = ''
pauseText = ''
directions = ['left', 'right', 'up', 'down']
random = rand(0, 3)
direction = directions[random]
scoreBoard = ''
score = 0
playerName = ''
sc_const=5

run = True
default_ctrl = True


def bosskey():
    global run
    run = False
    boss = Toplevel()
    boss.title('Spreadsheet')
    bossC = Canvas(boss, bg='white', width=1900, height=900)
    bossC.pack()
    bossImg = PhotoImage(file=r'boss.png')
    boss.bossImg = bossImg
    bossC.create_image(0, 0, image=bossImg, anchor='nw')
    boss.attributes('-topmost', 'true')


def score_display():
    global scoreBoard, score
    canvas.delete(scoreBoard)
    scoreBoard = canvas.create_text(
        640, 10, font='Terminal 30 bold', text=(
            'Score:' + str(score)), fill='blue', anchor='n')


def grow():
    tail = len(snake) - 1
    tail_pos = canvas.coords(snake[tail])
    snake.append(canvas.create_oval(0, 0, snakeS, snakeS, fill='#2e856e'))
    if(direction == 'left'):
        canvas.coords(snake[tail + 1], tail_pos[0] + snakeS,
                      tail_pos[1], tail_pos[2] + snakeS, tail_pos[3])
    elif(direction == 'right'):
        canvas.coords(snake[tail + 1], tail_pos[0] - snakeS,
                      tail_pos[1], tail_pos[2] - snakeS, tail_pos[3])
    elif(direction == 'up'):
        canvas.coords(snake[tail + 1],
                      tail_pos[0],
                      tail_pos[1] + snakeS,
                      tail_pos[2],
                      tail_pos[3] + snakeS)
    elif(direction == 'down'):
        canvas.coords(snake[tail + 1],
                      tail_pos[0],
                      tail_pos[1] - snakeS,
                      tail_pos[2],
                      tail_pos[3] - snakeS)


def move_food():
    global food, foodX, foodY
    canvas.move(food, (foodX * -1), (foodY * -1))
    foodX = rand(100, 1100)
    foodY = rand(100, 600)
    canvas.move(food, foodX, foodY)


def collision(a, b):
    if a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]:
        return True

    return False


def move_snake():
    global food, score, speed, run, positions,sc_const,snake_coords
    canvas.pack()  # updates of objects to canvas here
    positions = []
    positions.append(canvas.coords(snake[0]))
    if positions[0][0] < 0:
        gameover = True
        canvas.create_text(
            width / 2,
            height / 2,
            fill="red",
            font="Terminal 50 italic bold",
            text="GAME OVER")

    elif positions[0][2] > width:
        gameover = True
        canvas.create_text(
            width / 2,
            height / 2,
            fill="red",
            font="Terminal 50 italic bold",
            text="GAME OVER")

    elif positions[0][3] > height:
        gameover = True
        canvas.create_text(
            width / 2,
            height / 2,
            fill="red",
            font="Terminal 50 italic bold",
            text="GAME OVER")

    elif positions[0][1] < 0:
        gameover = True
        canvas.create_text(
            width / 2,
            height / 2,
            fill="red",
            font="Terminal 50 italic bold",
            text="GAME OVER")

    snakehead_pos = canvas.coords(snake[0])
    foodPos = canvas.coords(food)
    newfood_pos = [foodPos[0], foodPos[1], foodPos[0] + 27, foodPos[1] + 30]

    if collision(snakehead_pos, newfood_pos):  # collide food logic
        score += sc_const
        speed -= 5
        show_speed()
        score_display()
        move_food()
        grow()

    if direction == "left":
        canvas.move(snake[0], -30, 0)

    elif direction == "right":
        canvas.move(snake[0], 30, 0)

    elif direction == "up":
        canvas.move(snake[0], 0, -30)

    elif direction == "down":
        canvas.move(snake[0], 0, 30)

    for i in range(1, len(snake)):
        if collision(snakehead_pos, canvas.coords(
                snake[i])):  # Head collides with body
            gameover = True
            canvas.create_text(
                width / 2,
                height / 2,
                fill="red",
                font="Terminal 50 italic bold",
                text="GAME OVER",
                anchor='n')

    for i in range(1, len(snake)):
        positions.append(canvas.coords(snake[i]))  # to add to snake head
        snake_coords=positions     
    for i in range(len(snake) - 1):
        canvas.coords(snake[i + 1],
                      positions[i][0],
                      positions[i][1],
                      positions[i][2],
                      positions[i][3])
        # to update body coords so it follows head

    if 'gameover' not in locals() and run:
        window.after(speed, move_snake)  # loop snake move function


def placefood():
    global food, foodX, foodY
    foodimg = PhotoImage(file=r'apple.png')
    window.foodimg = foodimg
    food = canvas.create_image(0, 30, image=foodimg, anchor='nw')
    #canvas.itemconfigure(food, image=apple)
    foodX = rand(100, 600)
    foodY = rand(100, 600)
    canvas.move(food, foodX, foodY)


def moveleft(event):
    global direction
    direction = "left"


def moveright(event):
    global direction
    direction = "right"


def moveup(event):
    global direction
    direction = "up"


def movedown(event):
    global direction
    direction = "down"


def show_speed():
    global speedDisp
    canvas.delete(speedDisp)
    speedDisp = canvas.create_text(
        0,
        15,
        font='Eccentric 20',
        text=f'Speed: {100-speed}',
        fill='#0492c2',
        anchor='nw')


def down_speed(_):
    global speed
    if speed < 100:
        speed += 1
        show_speed()


def pause_game(_):
    global run, pauseText
    if not run:
        run = True
        window.after(speed, move_snake)
        canvas.delete(pauseText)
    elif run:
        run = False
        pauseText = canvas.create_text(
            640,
            300,
            font='STSong 30',
            fill='red',
            text='Press SPACE to continue game',
            anchor='n')


def menu():
    global name, menu, run, default_ctrl
    run = False
    menu = Toplevel()
    menu.geometry('700x700')
    menu.title('Menu')
    menu.attributes('-topmost', 'true')
    menuC = Canvas(menu, bg='black', width=width, height=700)
    menuC.create_text(
        350,
        100,
        text="Welcome to my snake game!",
        fill='white',
        font='Escentric 25')
    menuC.create_text(
        330,
        200,
        text="Enter your initials",
        fill='white',
        font='Escentric 15',
        anchor='n')
    name = Entry(menu)
    menuC.create_window(320, 240, window=name)
    name_button = Button(
        menu,
        height=1,
        width=5,
        text='Enter',
        bg='white',
        command=lambda: get_name())
    name_button.place(x=420, y=225)
    start_button = Button(
        menu,
        height=3,
        width=20,
        text='START',
        bg='green',
        command=lambda: start())
    start_button.place(x=350, y=450, anchor='n')

    menuC.create_text(
        350,
        280,
        text="Please choose prefered controls",
        fill='white',
        font='Escentric 15')
    WASDbutton = Button(
        menu,
        height=3,
        width=20,
        text='WASD controls',
        bg='#33FFFF',
        command=lambda: wasd())
    WASDbutton.place(x=160, y=300)
    arrow_button = Button(
        menu,
        height=3,
        width=20,
        text='Arrow key controls',
        bg='#33CC99',
        command=lambda: arrow())
    arrow_button.place(x=380, y=300)

    menuC.create_text(
        10,
        550,
        text="Instructions: B for bosskey,Arrows/WASD for movement,SPACE to pause game",
        fill='white',
        font='Escentric 12',
        anchor='nw')
    menuC.create_text(
        100,
        600,
        text='Cheat code: Press key <E> to decrease speed of snake,Press <Q> to increase point per apple eaten',
        fill='white',
        anchor='nw',
        font='Times 10')

    menuC.pack()


def get_name():
    global playerName, name
    playerName = name.get()


def start():
    global run, menu, window
    run = True
    window.after(speed, move_snake)
    menu.destroy()


def wasd():
    global default_ctrl
    default_ctrl=True
    if default_ctrl==True:
        window.bind("<a>", moveleft)
        window.bind("<d>", moveright)
        window.bind("<w>", moveup)
        window.bind("<s>", movedown)

    elif default_ctrl == False:
        default_ctrl = True


def arrow():
    global default_ctrl
    default_ctrl=False
    if default_ctrl == False:
        window.bind("<Left>", moveleft)
        window.bind("<Right>", moveright)
        window.bind("<Up>", moveup)
        window.bind("<Down>", movedown)

    if default_ctrl==True:
        default_ctrl=False

def cheat_score(_):
    global sc_const
    if sc_const<20:
        sc_const+=5

def startgame():
    show_speed()
    window.bind('<space>', pause_game)
    window.bind("<b>", lambda event: bosskey())
    window.bind('<e>', down_speed)
    window.bind('<q>',cheat_score)
    canvas.focus_set()
    global snake
    snake.append(
        canvas.create_oval(
            350,
            350,
            380,
            380,
            fill="#006a4e",
            tag='snakehead',
        ))
    placefood()
    move_snake()


# Canvas config
window = Tk()
window.title("Snake Game")
window.geometry('1280x720')
canvas = Canvas(window, bg="#64d859", width=1280, height=720)
backdrop = PhotoImage(file='background.png', width='1280', height='720')
canvas.create_image(0, 0, image=backdrop, anchor='nw')

menu()
startgame()
window.mainloop()

#LEADERBOARD SYSTEM
pScore = playerName + ' ' + str(score) + '\n'
file = open('highscore.txt', 'a')
file.write(pScore)
file.close()

window2 = Tk()
window2.title('Leaderboard')
window2.geometry('700x500')
leaderboard = Canvas(window2, bg='black', width=700, height=500)
leaderboard.pack()

leaderboard.create_text(
    350,
    50,
    text='Leaderboard',
    font='Courier 40 bold underline',
    fill='white')
file = open('highscore.txt', 'a')
file.close()
totallist = []
file = open('highscore.txt', 'r')
for line in file:
    totallist.append(line)

totallist = [x[:-1]for x in totallist]

playerList = []
scoreList = []
# separating score from playername
for element in totallist:
    name = element[0:element.find(' ')]
    score = element[element.find(' '):]
    playerList.append(name)
    scoreList.append(score)

# Converting the two lists into a dictionary and arranging from highest
# scorer to lowest
scoredict = dict(zip(playerList, scoreList))
descendingDictionary = dict(
    sorted(
        scoredict.items(),
        key=lambda item: int(
            item[1]),
        reverse=True))
# Putting back to a list after sorting
names = []
scores = []
for i in descendingDictionary:
    name = i
    score = descendingDictionary[i]

    scores.append(score)
    names.append(name)

name1, score1 = names[0], scores[0]
name2, score2 = names[1], scores[1]
name3, score3 = names[2], scores[2]

top1 = "1." + name1 + ':' + score1 + ' points'
top2 = "2." + name2 + ':' + score2 + ' points'
top3 = "3." + name3 + ':' + score3 + ' points'

leaderboard.create_text(
    350,
    100,
    text='TOP 3 PLAYERS',
    fill='white',
    font='Courier 30')
leaderboard.create_text(350, 200, text=top1, fill='white', font='Escentric 20')
leaderboard.create_text(350, 250, text=top2, fill='white', font='Escentric 20')
leaderboard.create_text(350, 300, text=top3, fill='white', font='Escentric 20')

window2.mainloop()