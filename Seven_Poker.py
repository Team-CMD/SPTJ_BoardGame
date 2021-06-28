import random
import sys

person = 2
M = 100000
M1 = 0
pattern = ['C','H','D','S']
availableCard = [[i,j]for i in pattern for j in range(1,14)]
cardList=[[] for _ in range (person)]    # 플레이어 카드 
Player_Money = [M]*person                # 나 자신과 컴퓨터 게임 머니
myBetting = [M1]*person # 각 플레이어가 얼마나 배팅을 하였는지(개인 배팅액 저장소)
Betting_Status = ["common"]*person # common, all, die
race = 1 # 배팅의 시작인지 아닌지 구분하기 위해.    
Table_Money = 0
seed_Money = 300                       # 시작 배팅 금액
Table_Money = 0                          # 테이블에 배팅된 머니
Opened_Card = [] # 오픈된 카드 (민준)
Priority = {'S': 4 , 'D' : 3, 'H': 2 , 'C': 1} # 패턴별 우선순위
die_win = 0 # die

def roll():
    # 카드 뭉치?에서 랜덤으로 뽑아
    # 플레이어 카드 리스트에 카드 정보를 넣는 함수

    for i in range(person):
        tmp = random.randrange(1, len(availableCard))
        cardList[i].append(availableCard[tmp])
        availableCard.pop(tmp)
    return
    
def Player_Card_Print():
    for i in range(person):
        if i == 0:
            print("playerCard: ", cardList[i])
        else:
            print("computerCard"+str(i),":", cardList[i])
    print("\n")
#==============================================================================================
# 포카드(무늬는 다르지만 같은 숫자 4개)
# 트리플(무늬에 관계 없이 같은 숫자 3장 모은 경우)
# 투페어(같은 숫자 두 개(원페어 두쌍))
# 원페어(무늬에 관계없이 같은 숫자 2장을 모은 경우)
# 노페어(누구도 족보 완성x -> 가지고 있는 등급의 카드 중 가장 높은 등급의 카드를 가진 사람이 우선)
#==============================================================================================

# 민준 (수정 필요하면 바로 말씀주세욤)
def Card_Priority(): # 카드 우선순위 체크
    Player_Opened_Card = Opened_Card[0]
    Computer_Opened_Card = Opened_Card[1]

    # Player가 선이면 return 0 / Computer가 선이면 return 1
    if len(Opened_Card[0]) == 1: # 경우의 수 : 노페어
        P_num_result = Number_Priority_Check(Player_Opened_Card)
        C_num_result = Number_Priority_Check(Computer_Opened_Card)
        P_pattern_result = Pattern_Priority_Check(Player_Opened_Card)
        C_pattern_result = Pattern_Priority_Check(Computer_Opened_Card)

        if P_num_result == C_num_result:
            return 0 if P_pattern_result > C_pattern_result else 1
        else:
            return 0 if P_num_result > C_num_result else 1           
                            
    if len(Opened_Card[0]) == 2: # 경우의 수 : 원페어, 노페어
        P_OnePair_result = OnePair(Player_Opened_Card)
        C_OnePair_result = OnePair(Computer_Opened_Card)

        if P_OnePair_result[0] and C_OnePair_result[0]: # 둘 다 원페어인 경우
            return 0 if P_OnePair_result[2] > C_OnePair_result[2] else 1
        elif P_OnePair_result[0] or C_OnePair_result[0]: # 둘 중 한명만 원페어인 경우
            return 0 if P_OnePair_result[0] else 1
        else: # 둘다 노페어인 경우
            if Number_Priority_Check(Player_Opened_Card) > Number_Priority_Check(Computer_Opened_Card):
                return 0
            elif Number_Priority_Check(Player_Opened_Card) < Number_Priority_Check(Computer_Opened_Card):
                return 1
            else:
                if Pattern_Priority_Check(Player_Opened_Card) > Pattern_Priority_Check(Computer_Opened_Card):
                    return 0
                else:
                    return 1

    if len(Opened_Card[0]) == 3: # 경우의 수 : 트리플, 원페어, 노페어
        P_Triple_result = Triple(Player_Opened_Card)
        C_Triple_result = Triple(Computer_Opened_Card)

        if P_Triple_result[0] and C_Triple_result[0]: # 둘다 트리플일 경우
            return 0 if P_Triple_result[1] > C_Triple_result[1] else 1
        elif P_Triple_result[0] or C_Triple_result[0]:
            return 0 if P_Triple_result[0] else 1

        P_OnePair_result = OnePair(Player_Opened_Card)
        C_OnePair_result = OnePair(Computer_Opened_Card)

        if P_OnePair_result[0] and C_OnePair_result[0]: # 둘 다 원페어인 경우
            return 0 if P_OnePair_result[2] > C_OnePair_result[2] else 1
        elif P_OnePair_result[0] or C_OnePair_result[0]: # 둘 중 한명만 원페어인 경우
            return 0 if P_OnePair_result[0] else 1
        else: # 둘다 노페어인 경우
            if Number_Priority_Check(Player_Opened_Card) > Number_Priority_Check(Computer_Opened_Card):
                return 0
            elif Number_Priority_Check(Player_Opened_Card) < Number_Priority_Check(Computer_Opened_Card):
                return 1
            else:
                if Pattern_Priority_Check(Player_Opened_Card) > Pattern_Priority_Check(Computer_Opened_Card):
                    return 0
                else:
                    return 1

    if len(Opened_Card[0]) == 4: # 경우의 수 : 포카드, 트리플, 투페어, 원페어, 노페어
        P_FourCard_result = FourCard(Player_Opened_Card)
        C_FourCard_result = FourCard(Computer_Opened_Card)

        if P_FourCard_result[0] and C_FourCard_result[0]:
            return 0 if P_FourCard_result[1] > C_FourCard_result[1] else 1
        elif P_FourCard_result[0] or C_FourCard_result[0]:
            return 0 if P_FourCard_result[0] else 1

        P_Triple_result = Triple(Player_Opened_Card)
        C_Triple_result = Triple(Computer_Opened_Card)

        if P_Triple_result[0] and C_Triple_result[0]:
            return 0 if P_Triple_result[1] > C_Triple_result[1] else 1
        elif P_Triple_result[0] or C_Triple_result[0]:
            return 0 if P_Triple_result[0] else 1

        P_TwoPair_result = TwoPair(Player_Opened_Card)
        C_TwoPair_result = TwoPair(Computer_Opened_Card)

        if P_TwoPair_result[0] and C_TwoPair_result[0]:
            return 0 if P_TwoPair_result[1] > C_TwoPair_result[1] else 1
        elif P_TwoPair_result[0] or C_TwoPair_result[0]:
            return 0 if P_TwoPair_result[0] else 1

        P_OnePair_result = OnePair(Player_Opened_Card)
        C_OnePair_result = OnePair(Computer_Opened_Card)

        if P_OnePair_result[0] and C_OnePair_result[0]: # 둘 다 원페어인 경우
            return 0 if P_OnePair_result[2] > C_OnePair_result[2] else 1
        elif P_OnePair_result[0] or C_OnePair_result[0]: # 둘 중 한명만 원페어인 경우
            return 0 if P_OnePair_result[0] else 1
        else: # 둘다 노페어인 경우
            if Number_Priority_Check(Player_Opened_Card) > Number_Priority_Check(Computer_Opened_Card):
                return 0
            elif Number_Priority_Check(Player_Opened_Card) < Number_Priority_Check(Computer_Opened_Card):
                return 1
            else:
                if Pattern_Priority_Check(Player_Opened_Card) > Pattern_Priority_Check(Computer_Opened_Card):
                    return 0
                else:
                    return 1


def FourCard(Card): # 포카드(포커)
    tmp = sorted(Card, key = lambda x: x[1])
    for i in range(len(tmp)-3):
        if (tmp[i][1] == tmp[i+1][1]) and (tmp[i+1][1] == tmp[i+2][1]) and (tmp[i+2][1] == tmp[i+3][1]):
            return [True, tmp[i][1]]
    return [False]

def Triple(Card):
    tmp = sorted(Card, key = lambda x: x[1])
    for i in range(len(tmp)-2): # tmp를 정렬 해두었기때문에 연속된 숫자들은 모여있을 것이다.  
        if (tmp[i][1] == tmp[i+1][1]) and (tmp[i+1][1] == tmp[i+2][1]):
            return [True, tmp[i][1]]
    return [False]

def TwoPair(Card):
    tmp = sorted(Card, key = lambda x:x[1])
    cnt = 0
    value_max = []
    for i in range(len(tmp)-1):
        if tmp[i][1] == tmp[i+1][1]:
            cnt += 1
            for key, value in Priority.items():
                if key == tmp[i][0] or key == tmp[i+1][0]:
                    value_max.append(value)
            if cnt == 2:
                return [True, max(value_max)]
                
    return [False]

def OnePair(Card):
    for i in range(len(Card)):
        for j in range(i+1,len(Card)):
            if Card[i][1] == Card[j][1]: # 숫자가 같다면
                for key, value in Priority.items(): # 패턴 우선 순위에 따라(두 사람이 원 페어인 경우 대비)
                    if key == Card[i][0] or key == Card[j][0]:
                        return [True, Card[i][1], value]
    return [False]

def Number_Priority_Check(Card): # 숫자 기준 우선순위 체크
    tmp = sorted(Card, key = lambda x : -x[1])
    if tmp[-1][1] == 1:
        return tmp[-1][1]
    else:
        return tmp[0][1]

            
def Pattern_Priority_Check(Card): # 패턴 기준 우선순위 체크
# P_Card : Player_Opened_Card / C_Card : Computer_Opened_Card
    for key, value in Priority.items():
        for i in range(len(Card)):
            if Card[i][0] == key:
                return value

def Betting_SeedMoney(Player_Money,myBetting): # 시드머니 배팅
    # 게임 시작과 동시에
    # 모든 플레이어들은 기본 배팅 금액을 지불한다.
    global Table_Money

    Table_Money = seed_Money * person # 테이블머니 = 시작배팅머니 * 플레이어 수
    for i in range(person):
        Player_Money[i] -= seed_Money # 플레이어 소유액 -= 시작배팅머니
        myBetting[i] += seed_Money # 플레이어 배팅액 += 시작배팅머니
        print(i+1,"플레이어의 시드머니 배팅 후 소유액 :",Player_Money[i])


def Progress(temp,last,next,bettingEnd): # 배팅함수에 필요
    # 다음인덱스로 넘어가는 역할
    # 레이스 여부에 따라 배팅을 끝낼지 다음 레이스를 이어갈지 정하는 역할  
    global Table_Money
    global race
    global die_win
    end = 0
    CommonList = [] #common상태 플레이어들의 배팅액을 저장

    if Betting_Status.count("die") == person - 1: # 한 명 제외 모두 die일때.
      bettingEnd = False
      next = 0
      die_win = 3
      for k in range(0, person):
        if Betting_Status[k] != "die":
          print(k+1,"번 플레이어님이 우승하셨습니다!!") 
      return bettingEnd, next

    if race == 1 and temp == last: # 1)첫배팅의 마지막 순서 인덱스라면
        for k in range(0,person): # 2)
            if Betting_Status[k] == "common": # 3)
                CommonList.append(myBetting[k])
        for l in range(0, len(CommonList)): # 2)
            if l == len(CommonList)-1: # 3)
                break
            else:
                if CommonList[l] == CommonList[l+1]: # 3)배팅액이 모두 같다면
                    end = 1
                elif CommonList[l] != CommonList[l+1]: # 3)배팅액이 다르다면
                    end = 2
                    break
        if end == 1:
            bettingEnd = False # 배팅을 종료한다.
            next = 0
            race = 1
            return bettingEnd, next
        elif end == 2:
            bettingEnd = True
            next = 1
            race = 2 # 배팅을 이어한다
            return bettingEnd, next  

    elif race == 1 and temp != last: # 1)첫배팅의 마지막 순서가 아니라면
        next = 1
        return bettingEnd, next

    elif race == 2: # 1)두번째 배팅이라면
        CommonList = []
        for k in range(0,person): # 2)
            if Betting_Status[k] == "common": # 3)
                CommonList.append(myBetting[k])
        for l in range(0, len(CommonList)): # 2)
            if l == len(CommonList)-1: # 3)
                break
            else:
                if CommonList[l] == CommonList[l+1]: # 3)배팅액이 모두 같다면
                    end = 1
                elif CommonList[l] != CommonList[l+1]: # 3)배팅액이 다르다면
                    end = 2
                    break
        if end == 1:
            bettingEnd = False # 배팅을 종료한다.
            next = 0
            race = 1
            return bettingEnd, next
        elif end == 2:
            bettingEnd = True
            next = 1
            race = 2 # 배팅을 이어한다
            return bettingEnd, next  


def Betting(choice, temp,eve,Betting_Status,betting_Money): # 배팅하는 함수. 삥1 체크2 콜3 하프4 따당5 다이6 올인7
    global Table_Money # return eve
    while 1:
      if choice == 1: # 삥
        Table_Money += seed_Money # 시드머니만큼 테이블머니에 돈을 낸다.
        Player_Money[temp] -= seed_Money # 시드머니만큼 소유액에서 돈을 뺀다.
        myBetting[temp] += seed_Money # 플레이어 배팅액에 추가
        eve = temp
        Betting_Status[temp] = "common"
        print("삥을 선택하셨군요! 지불한 금액 :",seed_Money,", 남은 잔액 :",int(Player_Money[temp]))
        break

      elif choice == 2: # 체크
        eve = temp
        Betting_Status[temp] = "common"
        print("체크를 선택하셨군요! 지불한 금액 : 0 , 남은 잔액 :",int(Player_Money[temp]))
        break       

      elif choice == 3: # 콜 베팅 - 플레이어머니
        temp2 = myBetting[eve] - myBetting[temp]
        Table_Money += temp2 # 이전사람이 낸 배팅액 - 내가낸 배팅
        Player_Money[temp] -= temp2
        myBetting[temp] = myBetting[eve]
        eve = temp
        Betting_Status[temp] = "common"
        print("콜을 선택하셨군요! 지불한 금액 :",int(temp2),", 남은 잔액 :",int(Player_Money[temp])) 
        break

      elif choice == 4: # 하프
        temp2 = Table_Money / 2
        Table_Money += temp2
        Player_Money[temp] -= temp2
        myBetting[temp] += temp2
        eve = temp
        Betting_Status[temp] = "common"
        print("하프를 선택하셨군요! 지불한 금액 :",int(temp2),", 남은 잔액 :",int(Player_Money[temp]))        
        break     

      elif choice == 5: # 따당
        temp2 = (myBetting[eve]-myBetting[temp])*2
        Table_Money += temp2
        Player_Money[temp] -= temp2
        myBetting[temp] += temp2
        eve = temp
        Betting_Status[temp] = "common"
        print("따당을 선택하셨군요! 지불한 금액 :",int(temp2),", 남은 잔액 :",int(Player_Money[temp])) 
        break
      
      elif choice == 6: # 올인
        temp2 = Player_Money[temp]
        myBetting[temp] += temp2
        Player_Money[temp] = 0
        Betting_Status = "all"
        print("올인! 지불한 금액 :",int(temp2))         
        break  

      elif choice == 7: # 다이
        myBetting[temp] = 0
        Betting_Status[temp] = "die"
        print("다이...남은 잔액 :",int(Player_Money[temp])) 
        break
        

      else: # 1-7이 아닌 잘못된 선택지
        print("잘못된 선택지를 누르셨습니다. 다시 배팅해주세요")
        continue

    return eve    


def Current_Print(temp, betting_Money, Player_Money):
    print("현재 테이블 머니 : ", Table_Money)
    print(temp+1,"번 플레이어님! 콜에 필요한 돈 :",int(betting_Money),", 현재 잔액 :", int(Player_Money[temp]))


def Betting_System(order): # 베팅 시스템
    # 플레이어가 베팅 순서에 맞게 자신이 
    # 베팅하고 싶은 금액에 맞게 베팅하는 함수
    global Table_Money
    global race

    bettingEnd = True
    first = order #우선순위 1등의 인덱스를 저장
    last = (first + (person-1)) % person
    next = 0
    eve = 0 # 인덱스를 저장하기 위한 변수.

    while bettingEnd == True: #bettingEnd가 true면 반복.
      for i in range(0,person): # 플레이어 수만큼 반복.
        temp = (first + i) % person  
        betting_Money = myBetting[eve]-myBetting[temp]   # 직전사람 배팅액 - 나의 배팅액(콜 조건)
        if Betting_Status[temp] == "all":
          continue
        elif Betting_Status[temp] == "die":
          myBetting[temp] = 0
          continue
        else: # Betting_Status[temp] == "common"
          if race == 1: # 배팅의 첫 바퀴일때.
            if Player_Money[temp] <= betting_Money or Player_Money[temp] <= seed_Money: # 올인 가능(= 콜할 돈(=이전사람배팅머니)이 없을때 또는 삥낼 돈도 없을때)
              if first == temp: # 선일때
                if Player_Money[temp] > seed_Money: # 삥, 체크, 올인, 다이
                  print("\n[1:삥 2:체크 6.올인 7.다이]")
                  Current_Print(temp, betting_Money, Player_Money)
                  while True:
                    if temp == 0: #플레이어일때
                      choice = int(input("배팅 선택지(숫자)를 입력하세요 : "))
                    else: # 컴퓨터일때
                      choice = random.randint(1,6)
                    if choice == 1 or choice == 2 or choice == 6 or choice == 7:
                      break
                    else:
                      if temp == 0: #플레이어일때
                        print(choice, "는 선택할 수 없는 배팅 선택지입니다. 다시 선택해주세요\n") 
                      else: #컴퓨터일때
                        continue
                  eve = Betting(choice,temp,eve,Betting_Status,betting_Money)                   
                  bettingEnd,next = Progress(temp,last,next,bettingEnd)
                  if next == 1: #다음인덱스 배팅 진행
                    continue 
                  else: # 베팅 종료
                    break
                elif Player_Money[temp] < seed_Money: # 체크, 올인, 다이
                  print("\n[2.체크 6.올인 7.다이]")
                  Current_Print(temp, betting_Money, Player_Money)
                  while True:
                    if temp == 0: #플레이어일때
                      choice = int(input("배팅 선택지(숫자)를 입력하세요 : "))
                    else: # 컴퓨터일때
                      choice = random.randint(1,6)
                    if choice == 2 or choice == 6 or choice == 7:
                      break
                    else:
                      if temp == 0: #플레이어일때
                        print(choice, "는 선택할 수 없는 배팅 선택지입니다. 다시 선택해주세요\n") 
                      else: #컴퓨터일때
                        continue               
                  eve = Betting(choice,temp,eve,Betting_Status,betting_Money)                    
                  bettingEnd,next = Progress(temp,last,next,bettingEnd)
                  if next == 1: #다음인덱스 배팅 진행
                    continue 
                  else: # 베팅 종료
                    break
              else: #선이 아닐때       
                  print("\n[6.올인 7.다이]")
                  Current_Print(temp, betting_Money, Player_Money)
                  while True:
                    if temp == 0: #플레이어일때
                      choice = int(input("배팅 선택지(숫자)를 입력하세요 : "))
                    else: # 컴퓨터일때
                      choice = random.randint(1,6)
                    if choice == 6 or choice == 7:
                      break
                    else:
                      if temp == 0: #플레이어일때
                        print(choice, "는 선택할 수 없는 배팅 선택지입니다. 다시 선택해주세요\n") 
                      else: #컴퓨터일때
                        continue              
                  eve = Betting(choice,temp,eve,Betting_Status,betting_Money)                    
                  bettingEnd,next = Progress(temp,last,next,bettingEnd)
                  if next == 1: #다음인덱스 배팅 진행
                    continue 
                  else: # 베팅 종료
                    break 

            elif Player_Money[temp] > betting_Money: # 올인 불가(=콜 가능 = 배팅머니 이상의 소유액 보유)
              if first == temp: #선일때
                if Player_Money[temp] > Table_Money / 2: # 삥 체크 하프 다이
                  print("\n[1.삥 2.체크 4.하프 7.다이]")
                  Current_Print(temp, betting_Money, Player_Money)
                  while True:
                    if temp == 0: #플레이어일때
                      choice = int(input("배팅 선택지(숫자)를 입력하세요 : "))
                    else: # 컴퓨터일때
                      choice = random.randint(1,6)
                    if choice == 1 or choice == 2 or choice == 4 or choice == 7:
                      break
                    else:
                      if temp == 0: #플레이어일때
                        print(choice, "는 선택할 수 없는 배팅 선택지입니다. 다시 선택해주세요\n") 
                      else: #컴퓨터일때
                        continue               
                  eve = Betting(choice,temp,eve,Betting_Status,betting_Money)                 
                  bettingEnd,next = Progress(temp,last,next,bettingEnd)
                  if next == 1: #다음인덱스 배팅 진행
                    continue 
                  else: # 베팅 종료
                    break
                elif Player_Money[temp] < Table_Money / 2 and Player_Money[temp] > seed_Money: #삥 체크 다이
                  print("\n[1.삥 2.체크 7.다이]")
                  Current_Print(temp, betting_Money, Player_Money)
                  while True:
                    if temp == 0: #플레이어일때
                      choice = int(input("배팅 선택지(숫자)를 입력하세요 : "))
                    else: # 컴퓨터일때
                      choice = random.randint(1,6)
                    if choice == 1 or choice == 2 or choice == 7:
                      break
                    else:
                      if temp == 0: #플레이어일때
                        print(choice, "는 선택할 수 없는 배팅 선택지입니다. 다시 선택해주세요\n") 
                      else: #컴퓨터일때
                        continue                
                  eve = Betting(choice,temp,eve,Betting_Status,betting_Money)                   
                  bettingEnd,next = Progress(temp,last,next,bettingEnd)
                  if next == 1: #다음인덱스 배팅 진행
                    continue 
                  else: # 베팅 종료
                    break     
              else: #선이 아닐때
                if Player_Money[temp] > Table_Money/2 and Player_Money[temp] > betting_Money*2: #콜 하프 따당 다이 
                  print("\n[3.콜 4.하프 5.따당 7.다이]")
                  Current_Print(temp, betting_Money, Player_Money)
                  while True:
                    if temp == 0: #플레이어일때
                      choice = int(input("배팅 선택지(숫자)를 입력하세요 : "))
                    else: # 컴퓨터일때
                      choice = random.randint(1,6)
                    if choice == 3 or choice == 4 or choice == 5 or choice == 7:
                      break
                    else:
                      if temp == 0: #플레이어일때
                        print(choice, "는 선택할 수 없는 배팅 선택지입니다. 다시 선택해주세요\n") 
                      else: #컴퓨터일때
                        continue                
                  eve = Betting(choice,temp,eve,Betting_Status,betting_Money)                   
                  bettingEnd,next = Progress(temp,last,next,bettingEnd)
                  if next == 1: #다음인덱스 배팅 진행
                    continue 
                  else: # 베팅 종료
                    break
                elif Player_Money[temp] > Table_Money/2 and Player_Money[temp] < betting_Money*2: #콜 하프 다이
                  print("\n[3.콜 4.하프 7.다이]")
                  Current_Print(temp, betting_Money, Player_Money)
                  while True:
                    if temp == 0: #플레이어일때
                      choice = int(input("배팅 선택지(숫자)를 입력하세요 : "))
                    else: # 컴퓨터일때
                      choice = random.randint(1,6)
                    if choice == 3 or choice == 4 or choice == 7:
                      break
                    else:
                      if temp == 0: #플레이어일때
                        print(choice, "는 선택할 수 없는 배팅 선택지입니다. 다시 선택해주세요\n") 
                      else: #컴퓨터일때
                        continue              
                  eve = Betting(choice,temp,eve,Betting_Status,betting_Money)              
                  bettingEnd,next = Progress(temp,last,next,bettingEnd)
                  if next == 1: #다음인덱스 배팅 진행
                    continue 
                  else: # 베팅 종료
                    break
                elif Player_Money[temp] < Table_Money/2 and Player_Money[temp] > betting_Money*2: #콜 따당 다이
                  print("\n[3.콜 5.따당 7.다이]")
                  Current_Print(temp, betting_Money, Player_Money)
                  while True:
                    if temp == 0: #플레이어일때
                      choice = int(input("배팅 선택지(숫자)를 입력하세요 : "))
                    else: # 컴퓨터일때
                      choice = random.randint(1,6)
                    if choice == 3 or choice == 5 or choice == 7:
                      break
                    else:
                      if temp == 0: #플레이어일때
                        print(choice, "는 선택할 수 없는 배팅 선택지입니다. 다시 선택해주세요\n") 
                      else: #컴퓨터일때
                        continue                  
                  eve = Betting(choice,temp,eve,Betting_Status,betting_Money)                  
                  bettingEnd,next = Progress(temp,last,next,bettingEnd)
                  if next == 1: #다음인덱스 배팅 진행
                    continue 
                  else: # 베팅 종료
                    break
                elif Player_Money[temp] < Table_Money/2 and Player_Money[temp] < betting_Money*2: #콜 다이
                  print("\n[3.콜 7.다이]")
                  Current_Print(temp, betting_Money, Player_Money)
                  while True:
                    if temp == 0: #플레이어일때
                      choice = int(input("배팅 선택지(숫자)를 입력하세요 : "))
                    else: # 컴퓨터일때
                      choice = random.randint(1,6)
                    if choice == 3 or choice == 7:
                      break
                    else:
                      if temp == 0: #플레이어일때
                        print(choice, "는 선택할 수 없는 배팅 선택지입니다. 다시 선택해주세요\n") 
                      else: #컴퓨터일때
                        continue               
                  eve = Betting(choice,temp,eve,Betting_Status,betting_Money)              
                  bettingEnd,next = Progress(temp,last,next,bettingEnd)
                  if next == 1: #다음인덱스 배팅 진행
                    continue 
                  else: # 베팅 종료
                    break          

          else: #race != 1 # 레이스로 인한 두번째 이상의 바퀴일때.
            if Player_Money[temp] <= betting_Money: # 올인 가능
              pass
            else: # 올인 불가
              if Player_Money[temp] > Table_Money/2 and Player_Money[temp] > betting_Money*2: # 콜, 하프 다이, 따당
                print("\n[3.콜 4.하프 5.따당 7.다이]")
                Current_Print(temp, betting_Money, Player_Money)
                while True:
                  if temp == 0: #플레이어일때
                    choice = int(input("배팅 선택지(숫자)를 입력하세요 : "))
                  else: # 컴퓨터일때
                    choice = random.randint(1,6)
                  if choice == 3 or choice == 4 or choice == 5 or choice == 7:
                    break
                  else:
                    if temp == 0: #플레이어일때
                      print(choice, "는 선택할 수 없는 배팅 선택지입니다. 다시 선택해주세요\n") 
                    else: #컴퓨터일때
                      continue             
                eve = Betting(choice,temp,eve,Betting_Status,betting_Money)                  
                bettingEnd,next = Progress(temp,last,next,bettingEnd)
                if next == 1: #다음인덱스 배팅 진행
                  continue 
                else: # 베팅 종료
                  break
              elif Player_Money[temp] > Table_Money/2 and Player_Money[temp] < betting_Money*2: # 콜, 하프, 다이
                print("\n[3.콜 4.하프 7.다이]")
                Current_Print(temp, betting_Money, Player_Money)
                while True:
                  if temp == 0: #플레이어일때
                    choice = int(input("배팅 선택지(숫자)를 입력하세요 : "))
                  else: # 컴퓨터일때
                    choice = random.randint(1,6)
                  if choice == 3 or choice == 4 or choice == 7:
                    break
                  else:
                    if temp == 0: #플레이어일때
                      print(choice, "는 선택할 수 없는 배팅 선택지입니다. 다시 선택해주세요\n") 
                    else: #컴퓨터일때
                      continue                  
                eve = Betting(choice,temp,eve,Betting_Status,betting_Money)                  
                bettingEnd,next = Progress(temp,last,next,bettingEnd)
                if next == 1: #다음인덱스 배팅 진행
                  continue 
                else: # 베팅 종료
                  break
              elif Player_Money[temp] < Table_Money/2 and Player_Money[temp] > betting_Money*2: # 콜, 따당, 다이
                print("\n[3.콜 5.따당 7.다이]")
                Current_Print(temp, betting_Money, Player_Money)
                while True:
                  if temp == 0: #플레이어일때
                    choice = int(input("배팅 선택지(숫자)를 입력하세요 : "))
                  else: # 컴퓨터일때
                    choice = random.randint(1,6)
                  if choice == 3 or choice == 5 or choice == 7:
                    break
                  else:
                    if temp == 0: #플레이어일때
                      print(choice, "는 선택할 수 없는 배팅 선택지입니다. 다시 선택해주세요\n") 
                    else: #컴퓨터일때
                      continue                
                eve = Betting(choice,temp,eve,Betting_Status,betting_Money)               
                bettingEnd,next = Progress(temp,last,next,bettingEnd)
                if next == 1: #다음인덱스 배팅 진행
                  continue 
                else: # 베팅 종료
                  break 
              elif Player_Money[temp] < Table_Money/2 and Player_Money[temp] < betting_Money*2: # 콜, 다이
                print("\n[3.콜 7.다이]")
                Current_Print(temp, betting_Money, Player_Money)
                while True:
                  if temp == 0: #플레이어일때
                    choice = int(input("배팅 선택지(숫자)를 입력하세요 : "))
                  else: # 컴퓨터일때
                    choice = random.randint(1,6)
                  if choice == 3 or choice == 7:
                    break
                  else:
                    if temp == 0: #플레이어일때
                      print(choice, "는 선택할 수 없는 배팅 선택지입니다. 다시 선택해주세요\n") 
                    else: #컴퓨터일때
                      continue                    
                eve = Betting(choice,temp,eve,Betting_Status,betting_Money)    
                bettingEnd,next = Progress(temp,last,next,bettingEnd)
                if next == 1: #다음인덱스 배팅 진행
                  continue 
                else: # 베팅 종료
                  break

def Card_Compare(arr): # 카드 비교 함수(승패 결정)
    # 플레이어 카드 리스트를 각각 비교하여 
    # 제일 높은 점수의 패를 가지고 있는 플레이어가 우승하는 함수
    # 1. 무늬가 5개 이상 있는 경우
    # 2. 연속된 숫자가 5개 이상있는경우
    # 3. 포카드, 풀 하우스 ,트리플, 투페어, 원페어, 노페어
        #12 + 탑렙 + 무늬인덱스   로얄 스트레이트 플러쉬    (10 J Q K A) 무늬 같음
        #11 + 탑렙 + 무늬인덱스   백 스트레이트 플러쉬      (A 2 3 4 5) 무늬 같음        
        #10 + 탑렙 + 무늬인덱스   스트레이트 플러쉬         (i ~ i+4)  무늬 같음
        #9  + 탑렙 + 무늬인덱스   포카드                    4장의 숫자 카드 같음
        #8  + 탑렙 + 무늬인덱스   풀하우스                  3장의 숫자 + 2장의 숫자 같음
        #7  + 탑렙 + 무늬인덱스   플러쉬                    (5장 무늬 같음)
        #6  + 탑렙 + 무늬인덱스   마운틴                    (10 J Q K A) 무늬 다름
        #5  + 탑렙 + 무늬인덱스   백스트레이트              (A 2 3 4 5) 무늬 다름
        #4  + 탑렙 + 무늬인덱스   스트레이트                (5장 연속) 무늬 다름
        #3  + 탑렙 + 무늬인덱스   트리플                    3장의 숫자 같음
        #2  + 탑렙 + 다음 탑렙    투페어                    2장의 숫자 + 2장의 숫자 같음
        #1  + 탑렙 + 다음 탑렙    원페어                    1장의 숫자 같음
        #0  + 탑렙 + 무늬인덱스   노페어                    노페어

    player_Score = [0]*person
    for i in range(person):
        shape = []
        Number = []
        for j in range(len(arr[i])):
            shape.append(arr[i][j][0])
            Number.append(arr[i][j][1])
        index, count = flush(shape)                               # 가장 작은 인덱스값
        if(index >= 0):                                           # 무늬 5개가 같으면 
            index2 = flush_straight(Number,index,count)           # 가장 큰 인덱스 값 (10,J,Q,K,A) 예외
            if(index2 >= 0):
                if Number[index2] == 1:                     # 로얄 스트레이트 플러쉬
                    score = 12*1000 + Number[index2]*10 + pattern.index(shape[index2])
                elif Number[index2] == 5:                    # 백 스트레이트 플러쉬
                    score = 11*1000 + Number[index2]*10 + pattern.index(shape[index2])
                else:                                       # 스트레이트 플러쉬
                    score = 10*1000 + Number[index2]*10 + pattern.index(shape[index2])
            else:                                           # 플러쉬
                score = 7*1000 + Number[index+4]*10 + pattern.index(shape[index2])
        else:
            index = straight(Number)                        # 제일 큰 인덱스 반환
            if(index >= 0):                                 # 연속된 숫자 5개가 있으면
                if Number[index] == 1:                      # 마운틴
                    score = 6*1000 + Number[index]*10 + pattern.index(shape[index])
                elif Number[index] == 5:                    # 백 스트레이트
                    score = 5*1000 + Number[index]*10 + pattern.index(shape[index])
                else:                                       # 스트레이트
                    score = 4*1000 + Number[index]*10 + pattern.index(shape[index])
            else:
                status = 0
                card = set(Number)
                card = list(card)
                card.reverse()
                for j in card:
                    if Number.count(j) == 4 and status < 9:             # 포카드
                        status = 9
                        Top = j
                        break
                    elif Number.count(j) == 3 and status < 3:           # 트리플
                        status = 3
                        Top = j
                        for k in card:
                            if Number.count(k) == 2:                    # 풀하우스
                                status = 8
                        break
                    elif Number.count(j) == 2 and status < 2:           # 투페어 이하
                        status = 1                                      # 원 페어 
                        Top = j
                        for k in card:
                            if Number.count(k) == 2 and k != j:         # 투 페어
                                status = 2
                                if(Top < k):
                                    Top = k
                    elif(status < 1):
                        status = 0
                        Top = max(Number)

                for j in range(len(Number)):
                    if Number[j] == Top:
                        Top_index = j

                score = status*1000 + Top*10 + pattern.index(shape[Top_index])

        player_Score[i] = score

    winner = player_Score.index(max(player_Score))
    return winner

def flush_straight(Number,start,count):
    index = -1
    cnt = 1
    for i in range(start, start+count-1):
        if Number[i]+1 == Number[i+1]:
            cnt += 1
            if(cnt >= 5):
                index = i+1
                if(Number[i+1] == 5): break
            if(cnt >= 4 and (Number[i+1] == 13 and Number[start] == 1)):
                index = start
        else:
            cnt = 1
    
    return index

def straight(Number):
    # 연속된 5개의 숫자가 존재하는지 확인하여 있으면 
    # 연속된 숫자 중 제일 큰 값의 인덱스를 반환
    # 이중for문으로 전체리스트를 순회 
    index = -1
    Num_copy = Number[:]
    Num_copy.sort()
    Num_copy = list(set(Num_copy))
    cnt = 1
    for i in Num_copy:
        if (i+1) in Number:
            cnt += 1
            if(cnt >= 5):
                index = Number.index(i+1)
                if(i+1 == 5): break
            if(cnt >= 4 and (i+1 == 13 and Num_copy[0] == 1)):
                index = Number.index(1)
                break
        else:
            cnt = 1

    return index

def flush(shape):
    # 같은 문양이 5개 이상있으면 
    # 문양 중 가장 작은 숫자의 인덱스를 반환
    index = -1
    for i in pattern:
        m = shape.count(i)
        if m < 5:
            continue
        else:
            index = shape.index(i)
            break
    return index, m

if __name__=="__main__":

    Betting_SeedMoney(Player_Money,myBetting)

    for _ in range(4):
        roll()

    cardList[0].sort()
    cardList[1].sort()

    Player_Card_Print()

    while True:
      print("삭제할 카드의 인덱스를 입력(0~):",end=' ')
      N = int(input())
      if N >= 0 and N < 4:
          break
      else:
          print("숫자범위에 벗어났습니다. 다시 입력해주세요.\n")

    cardList[0].pop(N)
    cardList[1].pop(random.randrange(0,len(cardList[1])))

    Player_Card_Print()

    comnum = random.randrange(0,3)
    while True:
      print("최초로 오픈할 카드의 인덱스를 입력(0~): ",end=' ')
      usernum = int(input())
      
      if usernum >= 0 and usernum < 3:
        break
      else:
        print("숫자범위에 벗어났습니다. 다시 입력해주세요.\n")
    
    print("player first Open Card : ", cardList[0][usernum])
    print("computer first Open Card : ", cardList[1][comnum], '\n')

    # 여기부터 상엽이 부분이었는데 내껄로 하다보니까 함수 내용에 포함되서 수정함
    Opened_Card.append([cardList[0][usernum]])
    Opened_Card.append([cardList[1][comnum]])
    cardList[0].pop(usernum)
    cardList[1].pop(comnum)

   
#     #PSO = Player second Open  / CSO = Computer Second Open
    if  Card_Priority() == 0:#유저 선
        print("(second)player first")
        PSOCard = random.choice(availableCard)
        availableCard.pop(availableCard.index(PSOCard))
        CSOCard = random.choice(availableCard)
        availableCard.pop(availableCard.index(CSOCard))
    else:#컴터 선
        print("(second)computer first")
        CSOCard = random.choice(availableCard)
        availableCard.pop(availableCard.index(CSOCard))
        PSOCard = random.choice(availableCard)
        availableCard.pop(availableCard.index(PSOCard))

    print("player second Open Card : ", PSOCard)
    print("computer second Open Card : ", CSOCard)
    # ===========================================================
    # 일단은 반복문 안돌리고 하나하나 복붙하였음.
    # ===========================================================
    Opened_Card[0].append(PSOCard)
    Opened_Card[1].append(CSOCard)
    print(Opened_Card, '\n')

    for j in range(3,7):
          if(j < 6):
                priority = Card_Priority()
          else:
                priority = Card_Compare(Opened_Card)
          if priority == 0:#유저 선
              print(str(j) + "번째 player first")
              Betting_System(0)
              if die_win == 3:
                  sys.exit()
              PSOCard = random.choice(availableCard)
              availableCard.pop(availableCard.index(PSOCard))
              CSOCard = random.choice(availableCard)
              availableCard.pop(availableCard.index(CSOCard))
          else:#컴터 선
              print(str(j) + "번째 판 computer first")
              Betting_System(1)
              if die_win == 3:
                  sys.exit()              
              CSOCard = random.choice(availableCard)
              availableCard.pop(availableCard.index(CSOCard))
              PSOCard = random.choice(availableCard)
              availableCard.pop(availableCard.index(PSOCard))

          print("player second Open Card : ", PSOCard)
          print("computer second Open Card : ", CSOCard)
          Opened_Card[0].append(PSOCard)
          Opened_Card[1].append(CSOCard)
          print(Opened_Card,'\n')

    print("playerCard(엎어져있는 카드) :", cardList[0])
    print("playerCard(공개된 카드) : ",Opened_Card[0])
    print("computerCard(엎어져있는 카드) :", cardList[1])
    print("computerCard(공개된 카드) : ",Opened_Card[1])

    for i in range(person):
        cardList[i] = cardList[i] + Opened_Card[i]
        cardList[i].sort()

    winner = Card_Compare(cardList)
    print(str(winner+1)+"번 플레이어님이 우승하셨습니다.")