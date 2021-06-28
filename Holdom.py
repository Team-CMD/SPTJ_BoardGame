import random, sys
import os

cardList = []
player_Card = [] # 플레이어 카드
computer_Card = [] # 컴퓨터 카드
share_Card = [] # 공유 카드
chip = [50, 50] # index[0] = 플레이어, index[1] =  컴퓨터
table_Chip = 0 # 테이블 머니

def Roll():
    # 덱에서 랜덤으로 뽑아 카드를 주는 함수
    # 이하 반복문 공유 카드 리스트에 2장 저장
    # 각 게이머에게 카드 한장씩 지급
    if not cardList:
        for i in range(4):
            for j in range(1,11):
                cardList.append(j)

    for i in range(2):
        tmp = random.choice(cardList)
        share_Card.append(tmp)
        cardList.remove(tmp)

    temp = []
    temp = random.sample(cardList, 2)

    for i in range(0,2):
        if i == 0:
            player_Card.append(temp[i])
        else:
            computer_Card.append(temp[i])
        cardList.remove(temp[i])

def BettingSeedMoney(chip):
    # 게임 시작과 동시에 모든 플레이어들은 기본 배팅 금액을 지불한다.
    # 테이블머니 = 시작배팅머니 * 플레이어 수
    # 플레이어 소유액 -= 시작배팅머니
    for i in range(0,2):
        chip[i] -= 1
        print(i+1,"플레이어의 시드머니 배팅 후 소유액 :",chip[i])

def PlayerBetting(chip):#플레이어 배팅시작
    print('--배팅--\n배팅금액입력(0은 다이입니다.): ',end='')
    b = int(input())
    if b>min(chip):
        b = min(chip)
        print('-올인-')
    return b

def ComputerBetting(chip):#컴퓨터의 배팅시작
    p = share_Card+player_Card
    p.sort()
    if len(p)==1:#플레이어가 '트리플' 아주낮은 확률로 배팅
        r = random.randrange(1, 6)
        if r == 1:
            return random.randrange(1, 10)#컴퓨터 뻥카
        else:
            return 0

    elif len(p)==2:#플레이어가 '더블' 낮은확률로 배팅
        r = random.randrange(1, 4)
        if r == 1:
            return random.randrange(1, 5)
        else:
            return 0

    if player_Card[0] < 3:#플레이어 카드낮음
        return random.randrange(1, 5)

    return random.randrange(1, 5)

def CardReset():
    # 공유된 카드, 플레이어 카드, 컴퓨터 카드 리셋
    share_Card.clear()
    player_Card.clear()
    computer_Card.clear()

def Rule():
    print("\n\n\n\t\t\t\t\t[ 게임 진행 및 설명 ]\n")
    print(" - 게임 참여는 칩 1개를 배팅함으로 시작합니다.")
    print(" - 40장의 카드 중 2장은 모두가 볼 수 있도록 오픈합니다.")
    print(" - 이후 각 플레이어들에게 상대방은 볼 수 있지만, 자기 자신은 볼 수 없는 카드를 한 장씩 받습니다.")
    print(" - 공개되어있는 카드 두 장과 플레이어가 가지고 있는 카드 한 장의 조합으로 게임의 승패를 결정짓습니다.")
    print(" - 이후 승자는 배팅된 서로의 칩을 모두 가져갑니다.")
    print(" - 게임은 플레이어 중 한명의 칩이 0이 될 때까지 계속합니다.\n")
    print(" * 게임 진행 도중 덱이 모두 소모된다면 덱은 다시 40장으로 초기화됩니다.")
    print(" * 무승부가 나온다면 배팅된 칩은 다음판으로 이전되어 게임이 진행됩니다.")
    print(" * 기본적으로 각 플레이어들은 칩 50개를 가지고 시작합니다.")
    print(" * 1부터 10까지 쓰여있는 카드를 숫자별로 4장씩, 총 40장의 카드를 가지고 게임을 진행합니다.\n\n\n")
    print("\t\t\t\t\t[ 카드 조합 및 우선 순위 ]\n")
    print(" - 조합이 없는 경우\t:\t어떠한 조합도 되지 않은 경우, 더 높은 숫자를 가진 카드가 이깁니다.")
    print(" - 더블\t\t\t:\t같은 숫자 카드가 두 장인 경우, 더 높은 숫자의 더블 조합이 이깁니다.")
    print(" - 스트레이트\t\t:\t카드 세 장의 숫자가 연속되는 조합인 경우, 더 높은 연속 숫자 조합의 카드가 이깁니다.")
    print(" - 트리플\t\t:\t카드 세 장의 숫자가 모두 같은 경우, 더 높은 숫자의 트리플 조합이 이깁니다.")
    print(" * 우선 순위\t\t:\t조합이 없는 경우 < 더블 < 스트레이트 < 트리플\n\n\n")
    while True:
        print("홈으로 돌아가려면 Enter를 눌러주세요",end='')
        escape = input()
        if escape == '':
            break

def Interpace():
    print("┌───────────────────────────────────────────────────────────────────────┐")
    print("\t\t\t\t[인디언 홀덤]\t\t\t\t")
    print("\t\t\t\t\t\t\t\t\t")
    print("\t1. 게임 시작\t\t2. 규칙 설명\t\t3.게임 종료\t")
    print("└───────────────────────────────────────────────────────────────────────┘")
    while True:
        try:
            N = int(input("메뉴 선택 : "))
            if 0 < N and N < 4:
                break
            else:
                print("\n메뉴를 다시 선택해주세요.\n")
        except:
            print("\n정수 값이 아닙니다\n")

    return N

def PrintCard():
    print("공유된 카드 : ",share_Card)
    print("상대방 카드 : ",computer_Card)

def GamePlay():
    drow = 0
    owner = 0
    table_Chip=0
    while True:
        t = 0
        if 0 in chip:
            break
        Roll()
        if drow == 0:
            BettingSeedMoney(chip)
            table_Chip=2
        PrintCard()

        #선이 시작배팅금 정하고 다이면 넘어감
        if owner ==0:#선 플레이어
            t = PlayerBetting(chip)

        elif owner == 1:
            t = ComputerBetting(chip)

        if t == 0:#시작부터 다이
            if owner==0: chip[1] += table_Chip
            else: chip[0] += table_Chip

            owner = 1 if owner == 0 else 0

            CardReset()
            continue
        

        print('시작 배팅금: ',t)
        N1 = -1
        if owner ==0:
            k = True
            while k: 
                a = random.randrange(1,6)#여기서 확률로 컴퓨터 배팅
            #if a <= 2 이런식으로 하고 만약 1~4이면 콜 5~8은 레이스 9는 다이
            #콜받거나 다이하면 k는 false로 바꾸는형식 레이즈는 배팅금 올려서  물어보기 플레이어한테후 다시 랜덤으로 컴퓨터배팅 돌아오게
                if a <= 2:#콜
                    print("computer : call")
                    k = False
                elif a > 2 and a <=4:#레이스
                    print("computer : raise")
                    b = random.randrange(1,5)
                    print('현재 배팅금 : ',t+2)
                    N1 = int(input('배팅금액(콜- 같은값, 다이-0): '))
                    k = False
                elif a == 5:#다이
                    print("computer : die")
                    k = False
        
            if N1 == 0:
                chip[1] += t + 2 
                chip[0] -= t

                owner = 1 if owner == 0 else 0

                CardReset()
                continue
        
        
        
        elif owner == 1:#컴퓨터가 선 이라서 사람이 콜,레이즈,다이 고름
            kk = True
            while kk:
                BN = int(input('배팅금액(콜- 같은값, 레이즈- 더높은 수, 다이-0): '))
                if BN == t:
                    print('call')
                    kk = False
                elif BN == 0:
                    print('die')
                    kk = False
                elif BN > t:
                    print('raise')
                    t = t + BN
                    b1 = random.randrange(1,3)

                    kk = False
                    if b1 == 1:
                        print('computer : die')
                    elif b1 == 2:
                        print('computer : call')
            
            if b1 == 1:
                chip[1] -= t
                chip[0] += t + 2

                owner = 1 if owner == 0 else 0

                CardReset()
                continue
            #사람한테 뭐할껀지 받고 콜이나 다이면 바로 넘어가서 족보비교

            #아니면 위에처럼 반복문으로 콜나올때까지 while돌리기



        # 배팅 종류 후 족보 비교
        owner = 1 if owner == 0 else 0#선 변경
        res = CompareCard()
        if  res ==1:#player win
            chip[0] += t+2
            chip[1] -= t
            print('-player 승\n칩수 p1:',chip[0],' p2:',chip[1])

            drow = 0
        elif res == 0:#com win
            chip[0] -= t
            chip[1] += t+2
            print('-player 패\n칩수 p1:',chip[0],' p2:',chip[1])

            drow = 0
        else:
            print('-무승부')
            drow = 1

        CardReset()

def CompareCard(): # 족보 비교
#===========================================================================================
# 플레이어 우승시 리턴 값 1
# 컴퓨터 우승시 리턴 값 0
# 비길경우 리턴 값 2
#===========================================================================================
# -카드 공개 시 족보
#      1)공유카드와 아무런 조합이 없는 경우->높은 숫자의 카드를 가진 플레이어 승
#      2)공유카드와의 조합 자신의 카드와 공유카드 중 한 장이 같은 숫자 : 더블
#      3)공유카드 두 장과 자신의 카드 한 장이 연속되는 숫자를 이룰 때(ex)345) : 스트레이트
#      4)공유카드 두 장과 자신의 카드 한 장의 숫자가 모두 같은 숫자일 때 : 트리플
#      5)만약 두 플레이어가 같은 조합(더블과 더블 등)을 이룰 때 : 조합을 이루는 숫자의 수가 더 큰 플레이어가 승리
#===========================================================================================

    # 컴퓨터카드 + 공유카드
    tmp_com = share_Card + computer_Card
    tmp_com.sort()
    # 플레이어카드 + 공유카드
    tmp_player = share_Card + player_Card
    tmp_player.sort()

    if len(list(set(tmp_player))) == 1 or len(list(set(tmp_com))) == 1: # 트리플일 경우
        if len(list(set(tmp_player))) == 1 and len(list(set(tmp_com))) == 1:
            if max(tmp_player) > max(tmp_com):
                return 1
            elif max(tmp_player) == max(tmp_com):
                return 2
            else:
                return 0
        else:
            return 1 if len(list(set(tmp_player))) == 1 else 0

    elif (tmp_com[2] == tmp_com[1]+1 == tmp_com[0]+2) or (tmp_player[2] == tmp_player[1]+1 == tmp_player[0]+2): # 스트레이트인 경우
        if (tmp_com[2] == tmp_com[1]+1 == tmp_com[0]+2) and (tmp_player[2] == tmp_player[1]+1 == tmp_player[0]+2):
            if player_Card[0] > computer_Card[0]:
                return 1
            elif player_Card[0] == computer_Card[0]:
                return 2
            else:
                return 0
        else:
            return 1 if (tmp_player[2] == tmp_player[1]+1 == tmp_player[0]+2) else 0

    elif len(list(set(tmp_player))) == 2 or len(list(set(tmp_com))) == 2:# 더블일 경우
        if len(list(set(tmp_player))) == 2 and len(list(set(tmp_com))) == 2:
            if player_Card[0] > computer_Card[0]:
                return 1
            elif player_Card[0] == computer_Card[0]:
                return 2
            else:
                return 0
        else:
            return 1 if len(list(set(tmp_player))) == 2 else 0

    else:
        if player_Card[0] > computer_Card[0]:
            return 1
        elif player_Card[0] == computer_Card[0]:
            return 2
        else:
            return 0

if __name__ == "__main__":
    while True:
        menu = Interpace()
        if menu == 1:
            chip = [50, 50]
            cardList.clear()
            GamePlay()
        elif menu == 2:
            Rule()
        else:
            sys.exit("\n\n게임 종료\n\n")