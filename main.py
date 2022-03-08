from tkinter import *
import random
from PIL import Image, ImageTk


def displayStack3():
    label3 = Label(gameBoard, image=deckImage1).place(x=335, y=205)
    label4 = Label(gameBoard, image=deckImage2).place(x=555, y=205)
    label1 = Label(gameBoard, image=deckImage1).place(x=350, y=220)
    label2 = Label(gameBoard, image=deckImage2).place(x=570, y=220)
    label1 = Label(gameBoard, image=deckImage1).place(x=365, y=235)
    label2 = Label(gameBoard, image=deckImage2).place(x=585, y=235)

def displayScore():
    label3 = Label(gameBoard, text=player1 + ' score:' + str(len(player1_deck)), font=("Helvetica", 14),
                   bg='teal').place(x=120, y=50)
    label4 = Label(gameBoard, text=player2 + ' score:' + str(len(player2_deck)), font=("Helvetica", 14),
                   bg='teal').place(x=730, y=50)


def calculateScore(p1, p2, stack1, stack2):
    if stack1 and stack2: print('stacks',stack1, stack2)
    global scorep1, scorep2, gameBoard
    if (int(p1.split('_')[0]) > int(p2.split('_')[0])):
        player1_deck.append(p1)
        player1_deck.append(p2)
        if stack1 and stack2: player1_deck.extend(stack1+stack2)
    elif (int(p1.split('_')[0]) < int(p2.split('_')[0])):
        player2_deck.append(p2)
        player2_deck.append(p1)
        if stack1 and stack2: player2_deck.extend(stack2+stack1)
    else:
        print('Tie breaker')
        displayStack3()
        if(len(player1_deck) > 3 and len(player2_deck) > 3):
            stack1 = player1_deck[0:3]
            stack2 = player2_deck[0:3]
            del player1_deck[:3]
            del player2_deck[:3]

            player2_image = resizeCard(f'Images/{player2_deck[0]}.png')
            label2 = Label(gameBoard, image=player2_image).place(x=540, y=190)
            player1_image = resizeCard(f'Images/{player1_deck[0]}.png')
            label1 = Label(gameBoard, image=player1_image).place(x=320, y=190)
            calculateScore(player1_deck[0], player2_deck[0], stack1, stack2)
        else:
            gameBoard.destroy()
    displayScore()
    if(player1_deck==[] or player2_deck==[]):
        gameBoard.destroy()


def resizeCard(card):
    our_card_img = Image.open(card)
    our_card_resize_image = our_card_img.resize((130, 200))
    global our_card_image
    our_card_image = ImageTk.PhotoImage(our_card_resize_image)
    return our_card_image


def dealCards():

    global deck
    deck = []
    suits = ["spades", "clubs", "hearts", "diamonds"]
    values = range(2, 15)
    global player1_deck, player2_deck
    player1_deck = []
    for suit in suits:
        for value in values:
            deck.append(f'{value}_of_{suit}')
    for i in range(26):
        elem = random.choice(deck)
        player1_deck.append(elem)
        deck.remove(elem)
    player2_deck = deck

def makeMove(gameBoard):

    player1_card = player1_deck.pop(0)
    global player1_image
    player1_image = resizeCard(f'Images/{player1_card}.png')
    player2_card = player2_deck.pop(0)
    global player2_image
    player2_image = resizeCard(f'Images/{player2_card}.png')
    label1 = Label(gameBoard, image=player1_image).place(x=320, y=190)
    label2 = Label(gameBoard, image=player2_image).place(x=540, y=190)
    calculateScore(player1_card, player2_card, None, None)


def displayWelcomePage():

    welcomePage = Tk()
    welcomePage.title('War-Game')
    welcomePage.geometry("800x550")
    welcomePage.configure(background="teal")

    canvas = Canvas(welcomePage, width=1000, height=750, bg="teal")

    canvas.create_text(400, 50, text="Enter player names", fill="black", font=('Helvetica 15 bold'))
    canvas.pack()

    p1 = Label(welcomePage, text="Player 1:", bg='teal', font=('Helvetica 11 bold')).place(x=235, y=140)

    p2 = Label(welcomePage, text="Player 2:", bg='teal', font=('Helvetica 11 bold')).place(x=235, y=200)

    player1_name = Entry(welcomePage, width=30)
    player1_name.place(x=320, y=140)

    player2_name = Entry(welcomePage, width=30)
    player2_name.place(x=320, y=200)

    def registerNames():
        global player1, player2
        player1 = player1_name.get()
        player2 = player2_name.get()
        print(player1, player2)
        if (not player1): player1 = 'Player1'
        if (not player2): player2 = 'Player2'
        Label(welcomePage, text=f'{player1}, Registered!', pady=20, bg='#ffbf00').pack()
        welcomePage.destroy()
        global gameBoard
        gameBoard = Tk()
        gameBoard.title('Let the game begin!')
        gameBoard.geometry("1000x650")
        gameBoard.configure(background="teal")
        global deckImage1, deckImage2
        deckImage1 = resizeCard(f'Images/player1_deck.PNG')
        deckImage2 = resizeCard(f'Images/player2_deck.PNG')
        label1 = Label(gameBoard, image=deckImage1).place(x=120, y=90)
        label2 = Label(gameBoard, image=deckImage2).place(x=740, y=90)
        dealCards()
        displayScore()
        print(len(player1_deck), len(player2_deck))
        showCardsButton = Button(gameBoard, text="Show cards", bg='DarkSeaGreen', width=11, font=('Helvetica 11 bold'), command= lambda: makeMove(gameBoard)).place(x=450, y=520)

        gameBoard.mainloop()

    submitButton = Button(welcomePage, text="Submit", bg='white', width=9, font=('Helvetica 10 bold'), command=registerNames).place(x=370, y=250)
    welcomePage.mainloop()
    return [player1, player2]

if __name__ == '__main__':

    players = displayWelcomePage()

