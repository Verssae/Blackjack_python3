import random
from tkinter import *
class Card:
    '''
    카드를 만드는 클래스
    '''
    suits = ("diamond", "heart", "spade", "clover")
    ranks = ("a", "2", "3", "4", "5", "6", "7", "8", "9", "10", "j", "q", "k")
    def __init__(self,suit,rank,face_up=True):
        self.suit=suit
        self.rank=rank
        self.face_up=face_up
        self.value = Card.ranks.index(self.rank)+1
        if self.value > 10:
            self.value = 10

    @staticmethod
    def fresh_deck():
        '''
        새로운 덱을 만드는 메소드
        '''
        cards=[]
        for s in Card.suits:
            for r in Card.ranks:
                cards.append(Card(s,r))
        random.shuffle(cards)
        return cards

    def flip(self):
        '''
        카드 앞 뒷면을 바꾸는 메소드
        '''
        self.face_up = not self.face_up

class Deck:
    '''
    덱을 만드는 클래스
    '''
    def __init__(self):
        self.deck = Card.fresh_deck()

    def next(self,face_up=True):
        '''
        덱에서 카드 한장을 뽑아 그 카드를 리턴하는 메소드
        만약 덱이 비었으면 새로 덱을 만들고 뽑아온다.
        '''
        if self.deck == []:
            self.deck = Card.fresh_deck()

        if face_up:
            card = self.deck.pop()
        else:
            card = self.deck.pop()
            card.flip()
        return card

class Hand:
    '''
    핸드를 만드는 클래스
    '''
    def __init__(self, master,name='Dealer'):
        if name=='Dealer':
            self.t = 100
        else:
            self.t = 300
        self.x = 200
        self.num = 0
        self.number = 0
        self.master = master
        self.hand =[]
        self.point = 0
        self.number_of_ace = 0

    def get(self, card):
        suits={'clover':'c','diamond':'d','heart':'h','spade':'s'}
        if card.face_up:
            img = PhotoImage(file="./cardimages/%s%s.gif"%(suits[card.suit],card.rank))
        else:
            img = PhotoImage(file="./cardimages/back.gif")
            self.hand.append((card,self.x+self.num,self.t+self.number))
        label = Label(self.master,image = img)
        label.image = img  # reference를 남겨야 함
        label.place(x=self.x + self.num,y=self.t+self.number)
        self.num += 14
        self.number -= 10
        self.get_point(card)

    def open(self):

        suits={'clover':'c','diamond':'d','heart':'h','spade':'s'}
        for i in self.hand:
            card, xx, yy = i
            img = PhotoImage(file="./cardimages/%s%s.gif"%(suits[card.suit],card.rank))
            label = Label(self.master,image = img)
            label.image = img  # reference를 남겨야 함
            label.place(x=xx,y=yy)


    def get_point(self,card):

        if card.rank == 'a':
            self.point += 11
            self.number_of_ace += 1
        else:
            self.point += card.value
        while self.point > 21 and self.number_of_ace > 0:
            self.point -= 10
            self.number_of_ace -= 1
