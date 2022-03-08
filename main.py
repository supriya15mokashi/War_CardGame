# Python implementation of 'War' - a card game;
# UI built using - Tkinter
# Author - Supriya Mokashi

from tkinter import *
import random
from PIL import Image, ImageTk

# Upon exit button closes the gameboard modal
def exitGame(gameBoard):
    gameBoard.after(100, gameBoard.destroy())


# If its a tie, display 3 cards faced down
def displayStack3(x1, y1, x2, y2):
    Label(gameBoard, image=deckImage1).place(x=x1, y=y1)
    Label(gameBoard, image=deckImage2).place(x=x2, y=y2)


# Displays updated score for every player above his/her deck
def displayScore():
    Label(gameBoard, text=player1 + ' score: ' + str(len(player1_deck)), font=("Helvetica", 14),
                   bg='teal').place(x=120, y=50)
    Label(gameBoard, text=player2 + ' score: ' + str(len(player2_deck)), font=("Helvetica", 14),
                   bg='teal').place(x=730, y=50)


# Calculates score after every move from both players; also handles actions if its a tie
def calculateScore(p1, p2, stack1, stack2):
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
        displayStack3(335, 205, 555, 205)
        displayStack3(350, 220, 570, 220)
        displayStack3(365, 235, 585, 235)

        if(len(player1_deck) > 3 and len(player2_deck) > 3):
            stack1 = player1_deck[0:3]
            stack2 = player2_deck[0:3]
            del player1_deck[:3]
            del player2_deck[:3]
            calculateScore(player1_deck[0], player2_deck[0], stack1, stack2)
        else:
            winner = ''
            if (len(player1_deck) > len(player2_deck)):
                winner = player1 + ' wins! Yayyy!'
            elif (len(player1_deck) < len(player2_deck)):
                winner = player2 + ' wins! Yayyy!'
            else:
                winner = player1 + ' and ' + player2 + ' both win! Yayy!'
            Label(gameBoard, text=winner, font=("Helvetica", 14), bg='teal').place(x=440, y=480)
            #gameBoard.destroy()

    displayScore()

    if(player1_deck==[] or player2_deck==[]):
        winner = ''
        if (len(player1_deck) > len(player2_deck)):
            winner = player1 + ' wins! Yayyy!'
        elif (len(player1_deck) < len(player2_deck)):
            winner = player2 + ' wins! Yayyy!'
        else:
            winner = player1 + ' and ' + player2 + ' both win! Yayy!'
        Label(gameBoard, text=winner, font=("Helvetica", 14), bg='teal').place(x=440, y=480)
        #gameBoard.destroy()


# crops the card images to be displayed
def resizeCard(card):
    raw_image = Image.open(card)
    raw_image.mode = 'RGBA'
    resize_image = raw_image.resize((130, 200))
    global final_image
    final_image = ImageTk.PhotoImage(resize_image)
    return final_image


# Builds a deck for each player having 26 randomly dealed cards
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


# Makes a move, by displaying the topmost card from every player's deck; calculates score
def makeMove(gameBoard):
    player1_card = player1_deck.pop(0)
    global player1_image
    player1_image = resizeCard(f'Images/{player1_card}.png')
    player2_card = player2_deck.pop(0)
    global player2_image
    player2_image = resizeCard(f'Images/{player2_card}.png')
    Label(gameBoard, image=player1_image).place(x=320, y=190)
    Label(gameBoard, image=player2_image).place(x=540, y=190)
    calculateScore(player1_card, player2_card, None, None)


# Registers players and initiates the game board
def registerNames(player1_name, player2_name):
    global player1, player2
    player1 = player1_name.get()
    player2 = player2_name.get()
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
    Label(gameBoard, image=deckImage1).place(x=120, y=90)
    Label(gameBoard, image=deckImage2).place(x=740, y=90)
    dealCards()
    exit_button = Button(gameBoard, text="Exit game", bg='DarkSeaGreen', width=11, font=('Helvetica 11 bold'), command=lambda: exitGame(gameBoard)).place(x=450, y=568)
    showCards_button = Button(gameBoard, text="Show cards", bg='DarkSeaGreen', width=11, font=('Helvetica 11 bold'), command=lambda: makeMove(gameBoard)).place(x=450, y=520)
    gameBoard.mainloop()


# Displays welcome page with player name fields and labels
def displayWelcomePage():

    global welcomePage
    welcomePage = Tk()
    welcomePage.title('War-Game')
    welcomePage.geometry("800x550")
    welcomePage.configure(background="teal")
    canvas = Canvas(welcomePage, width=1000, height=750, bg="teal")
    canvas.create_text(400, 50, text="Enter player names", fill="black", font=('Helvetica 15 bold'))
    canvas.pack()
    Label(welcomePage, text="Player 1:", bg='teal', font=('Helvetica 11 bold')).place(x=235, y=140)
    Label(welcomePage, text="Player 2:", bg='teal', font=('Helvetica 11 bold')).place(x=235, y=200)
    player1_name = Entry(welcomePage, width=30)
    player1_name.place(x=320, y=140)
    player2_name = Entry(welcomePage, width=30)
    player2_name.place(x=320, y=200)
    register_button = Button(welcomePage, text="Submit", bg='white', width=9, font=('Helvetica 10 bold'), command=lambda:registerNames(player1_name, player2_name)).place(x=370, y=250)
    welcomePage.mainloop()


if __name__ == '__main__':
    # To view the welcome page - entry point to game
    displayWelcomePage()