import random
from tkinter import *
from model import *
class Reader(Frame):
    """
    처음 로그인 화면을 보여주며 사용자 정보를 기억하고 컨트롤러를 불러 게임을 실행시킴.
    메뉴에서 사용하는 함수들도 이 클래스에 저장되어 있음.
    """
    def __init__(self, master):
        super().__init__(master, width=500, height=570)
        self.place(x=0, y=0)
        photo = PhotoImage(file = './images/main.gif')
        bg = Label(self, image=photo)
        bg.image = photo
        bg.place(x=0, y=0)
        self.create_widgets()
        self.master = master

    def create_widgets(self):
        self.entry = Entry(self, width=10, bg='gray')
        self.entry.place(x=170, y=500)
        self.log_in = Button(self, text="LOGIN", command=self.login, highlightbackground='gray')
        self.log_in.place(x=270, y=500)

    def load_members(self):
        file = open("members.txt", "r")
        self.members = {}
        for line in file:
            name, tries, wins, chips = line.strip('\n').split(',')
            self.members[name] = int(tries), float(wins), int(chips)
        file.close()

    def store_members(self):
        file = open("members.txt", "w")
        self.names = self.members.keys()
        for name in self.names:
            tries, wins, chips = self.members[name]
            line = name + ',' + str(tries) + ',' + str(wins) + "," + str(chips) + '\n'
            file.write(line)
        file.close()

    def login(self):
        self.name = self.entry.get()
        self.load_members()
        if self.name in self.members.keys():
            self.tries = self.members[self.name][0]
            self.wins = self.members[self.name][1]
            self.chips = self.members[self.name][2]

        else:
            self.members[self.name] = 0,0,100
            self.tries = self.members[self.name][0]
            self.wins = self.members[self.name][1]

            self.chips = self.members[self.name][2]

        self.place_forget()
        self.bj = BlackJackController(self.master,'green')

    def stat(self):
        """
        메뉴의 stat을 누르면 실행되는 함수로 새로운 창을 생성하고 현재 사용자의 정보를 보여준다.
        """
        master = Tk()
        master.title('Stats')
        master.geometry('200x170')
        frame = Frame(master, width=200, height=170)
        frame.place(x=0,y=0)
        name_label = Label(frame, text='Name : ' + str(self.name))
        name_label.place(x=10, y=10)
        tries_label = Label(frame, text='You played game ' + str(self.tries) + ' times.')
        wins_label = Label(frame, text='Wins : ' + str(int(self.wins)))
        winning_rate = 100 * self.wins / self.tries if self.tries > 0 else 0
        winning_rate = round(winning_rate,1)
        winning_rate_label = Label(frame,text='Winning Rate : '+str(winning_rate)+'%')
        chips_label = Label(frame,text='You have '+str(self.chips)+' dollars.')
        tries_label.place(x=10,y=30)
        wins_label.place(x=10,y=50)
        winning_rate_label.place(x=10,y=70)
        chips_label.place(x=10,y=90)
        quit_button = Button(frame,text='OK',command=master.destroy)
        quit_button.place(x=70,y=120)
        master.mainloop()

    def show_top5(self):
        """
        메뉴의 Ranking 탭을 누르면 실행되는 함수로, 새로운 창에서 상위 5명의 이름과 보유 달러를 보여줌.
        """
        master = Tk()
        master.title('Ranking')
        master.geometry('200x170')
        frame = Frame(master,width=200,height=170)
        frame.place(x=0,y=0)
        sorted_members = sorted(self.members.items(),key=lambda x: x[1][2],reverse=True)
        text_label = Label(frame,text="Play Of The Game Top 5")
        text_label.place(x=10,y=10)
        rank = 1
        for member in sorted_members[:5]:
            chips = member[1][2]
            if chips <= 0:
                break
            Label(frame,text=str(rank)+' . ' + member[0] +' : (' +str(chips)+')'+'$').place(x=10,y=10+20*rank)
            rank += 1
        quit_button = Button(frame,text='OK',command=master.destroy)
        quit_button.place(x=70,y=140)
        master.mainloop()

    def help(self):
        """
        메뉴에서 help 탭을 누르면 실행되는 함수로, 새로운 창에서 도움말을 보여준다.
        """
        master = Tk()
        master.title('Help')
        txtbox = Text(master)
        txtbox.pack()
        summary = "Welcome to BlackJack Game!\nNew players have 10$.\nIf you win, you will receive twice the amount you betted.\nIf you are blackjack,you will receive 3 times the amount you betted."
        txtbox.insert(0.0,summary)
        quit_button = Button(master,text='OK',command=master.destroy)
        quit_button.pack(padx=30,pady=20)
        master.mainloop()

    def option(self):
        """
        메뉴에서 Theme 탭을 누르면 실행되는 함수로, 새로운 창에서 배경색을 선택할 수 있다.
        단, 게임을 새로 시작하므로, 게임이 종료되지 않았을 때 배경을 바꿀 시 베팅한 돈은 돌려받을 수 없다.
        """
        master = Tk()
        master.title('Theme')
        master.geometry('200x200')
        black_button = Button(master,text='Black',command=lambda:self.change('black'))
        black_button.place(x=70,y=20)
        green_button = Button(master,text='Green',command=lambda:self.change('green'))
        green_button.place(x=70,y=100)
        yellow_button = Button(master,text='Yellow',command=lambda:self.change('yellow'))
        yellow_button.place(x=70,y=60)
        quit_button = Button(master,text='OK',command=master.destroy)
        quit_button.place(x=70,y=140)

    def change(self,txt):
        self.bj.destroy()
        self.bj = BlackJackController(self.master,txt)

class BlackJackController(Frame):
    """
    블랙잭 게임을 실행하는 컨트롤러 클래스이다. Reader로부터 배경색을 인자로 받아 게임을 실행시킨다.
    먼저 베팅할 금액을 선택하고 Deal 버튼을 누르면 게임이 시작되며, 카드를 더 받고싶으면 Hit, 그만 받고 싶으면 Stand를 누른다.
    게임의 결과가 나타나고 보상을 받는다. 다시 베팅을 하고 Deal 버튼을 누르면 새 게임을 할 수 있다.
    한 게임이 진행되는 동안에는 Deal 버튼이 비활성화 되며, 게임 시작 전에는 Hit 와 Stand 버튼이 비활성화 된다.
    배당율은 승리시 2배, 블랙잭시 3배이다.
    """
    def __init__(self,master,bgcolor):
        super().__init__(master,width=500,height=570)
        master.geometry('500x570')
        self.bgcolor = bgcolor
        self.place(x=0,y=0)
        self.frame = Frame(width=500,height=500,bg=self.bgcolor)
        self.frame.place(x=0,y=0)
        self.deck = Deck()
        self.var = IntVar()
        self.bet = self.var.get()
        self.end = Label(self,text='Welcome to BlackJack!')
        self.end.place(x=210,y=250)

        button_frame = Frame(self,width=500,height=70,bg='gray')
        button_frame.place(x=0,y=500)
        self.how_money = Label(button_frame,bg='gray',width=5,height=2,relief=RIDGE,font=('Times',20),anchor=E)

        self.how_money.config(text='%d$'% reader.chips)
        self.how_money.place(x=10,y=10)
        one_dollar = Radiobutton(button_frame,text='5$',variable=self.var,value=5,bg='gray')
        one_dollar.place(x=80,y=25)
        five_dollar = Radiobutton(button_frame,text='10$',variable=self.var,value=10,bg='gray')
        five_dollar.place(x=130,y=25)
        ten_dollar = Radiobutton(button_frame,text='50$',variable=self.var,value=50,bg='gray')
        ten_dollar.place(x=180,y=25)
        betting = Label(button_frame,text='Bet',bg='gray')
        betting.place(x=130,y=5)
        self.deal_button = Button(button_frame,text='Deal',highlightbackground='gray',command=self.play_card)
        self.deal_button.place(x=240,y=25)
        self.hit_button = Button(button_frame,text='Hit',highlightbackground='gray',command=self.hit,state=DISABLED)
        self.hit_button.place(x=300,y=25)
        self.stand_button = Button(button_frame,text='Stand',highlightbackground='gray',command=self.stand,state=DISABLED)
        self.stand_button.place(x=360,y=25)



    def hit(self):
        self.player.get(self.deck.next())
        if self.dealer.point <= 16:
            self.dealer.get(self.deck.next(False))
        if self.player.point == 21:
            if self.dealer.point == 21:
                self.state('Push')
            else:
                self.state('Win')
        elif self.player.point > 21:
            self.state('Lose')

    def stand(self):
        while self.dealer.point <= 16:
            self.dealer.get(self.deck.next(False))
        if self.player.point < 21:
            if self.dealer.point > 21:
                self.state('Win')
            elif self.dealer.point == 21:
                self.state('Lose')
            elif self.dealer.point < 21:
                if self.player.point > self.dealer.point:
                    self.state('Win')
                elif self.player.point == self.dealer.point:
                    self.state('Push')
                else:
                    self.state('Lose')

    def play_card(self):
        self.hit_button['state'] = NORMAL
        self.stand_button['state'] = NORMAL
        self.deal_button['state'] = DISABLED
        self.frame.destroy()
        self.frame = Frame(width=500,height=500,bg=self.bgcolor)
        self.frame.place(x=0,y=0)

        self.player = Hand(self.frame,reader.name)
        self.dealer = Hand(self.frame)
        self.bet = self.var.get()
        if reader.chips - self.bet < 0:
            self.end = Label(self.frame,text='No Money!',bg=self.bgcolor,fg='red',font=('Helvetica',40))
            self.end.place(x=180,y=210)
            self.deal_button['state'] = NORMAL
            self.hit_button['state'] = DISABLED
            self.stand_button['state'] = DISABLED
        else:
            reader.chips -= self.bet
            self.how_money.config(text='%d$'% reader.chips)
            self.player.get(self.deck.next())
            self.dealer.get(self.deck.next())
            self.player.get(self.deck.next())
            self.dealer.get(self.deck.next(False))
            if self.player.point == 21 and self.dealer.point == 21:
                self.state('Push')
            elif self.player.point == 21 and self.dealer.point < 21:
                self.state('BlackJack')
            elif self.player.point < 21 and self. dealer.point == 21:
                self.state('Lose')

    def state(self,txt):
        reader.tries += 1
        if txt == 'Win':
            reader.wins += 1
            reader.chips += self.bet * 2
        if txt == 'BlackJack':
            reader.wins += 1
            reader.chips += self.bet * 3
        if txt == 'Push':
            reader.chips += self.bet
            reader.wins += 0.5
        self.end = Label(self.frame,text=txt,bg=self.bgcolor,fg='red',font=('Helvetica',40))
        self.end.place(x=210,y=210)
        self.dealer.open()
        reader.members[reader.name] = reader.tries,reader.wins,reader.chips
        reader.store_members()
        self.how_money.config(text='%d$'% reader.chips)
        if reader.chips == 0:
            self.end = Label(self.frame,text='Game Over!(+50$)',bg=self.bgcolor,fg='red',font=('Helvetica',40))
            self.end.place(x=140,y=210)
            reader.chips = 50
            self.how_money.config(text='%d$'% reader.chips)


        self.hit_button['state'] = DISABLED
        self.stand_button['state'] = DISABLED
        self.deal_button['state'] = NORMAL

root = Tk()
root.title("BlackJack")
root.geometry("500x570")
reader = Reader(root)

"""
메뉴 만들기
"""
menubar = Menu(root)
root.config(menu=menubar)
submenu = Menu(menubar)
submenu.add_command(label='Stat',command =reader.stat)
submenu.add_command(label='Ranking',command=reader.show_top5)
submenu.add_command(label='Help',command=reader.help)
submenu.add_command(label='Theme',command =reader.option)
submenu.add_command(label='Exit',command=exit)
menubar.add_cascade(label="Game",menu=submenu)

root.mainloop()
