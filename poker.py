import random

pattern = ['C','D','H','S']
availableCard = [[i,j]for i in pattern for j in range(1,14)]
cardList=[[],[]]
Opened_Card = [] # 오픈된 카드 (민준)
Priority = {'S': 4 , 'D' : 3, 'H': 2 , 'C': 1}

def roll():
    tmp = random.randrange(1, len(availableCard))
    cardList[0].append(availableCard[tmp])
    availableCard.pop(tmp)
    tmp = random.randrange(1, len(availableCard))
    cardList[1].append(availableCard[tmp])
    availableCard.pop(tmp)
    return

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
    for i in range(len(tmp)-1):
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
            

def Betting_System(): # 베팅 시스템
    # 플레이어가 베팅 순서에 맞게 자신이 
    # 베팅하고 싶은 금액에 맞게 베팅하는 함수
    pass

if __name__=="__main__":
    for _ in range(4):
        roll()

    cardList[0].sort()
    cardList[1].sort()
    print(availableCard)
    print("playerCard: ", cardList[0])
    print("computerCard: ", cardList[1])
    print("삭제할 카드의 인덱스를 입력(0~):",end=' ')
    N = int(input())
    cardList[0].pop(N)
    cardList[1].pop(random.randrange(0,len(cardList[1])))

    print("playerCard: ", cardList[0])
    print("computerCard: ", cardList[1])

    comnum = random.randrange(0,3)
    print("최초로 오픈할 카드의 인덱스를 입력(0~): ",end=' ')
    usernum = int(input())
    
    print("player first Open Card : ", cardList[0][usernum])
    print("computer first Open Card : ", cardList[1][comnum])

    Opened_Card.append([cardList[0][usernum]])
    Opened_Card.append([cardList[1][comnum]])
    cardList[0].pop(usernum)
    cardList[1].pop(comnum)

    #PSO = Player second Open  / CSO = Computer Second Open
    if Card_Priority == 0:#유저 선
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

    print(Opened_Card)
    
    if Card_Priority() == 0: # player 선
        print("(third)player first")
        # 배팅 미완
        # 배팅 후 선(0 : player)이 오픈카드를 한 장씩 받는다.
        PSOCard = random.choice(availableCard)
        availableCard.pop(availableCard.index(PSOCard))
        CSOCard = random.choice(availableCard)
        availableCard.pop(availableCard.index(CSOCard))
    else: # 1일 때 / computer 선
        print("(third)computer first")
        # 배팅 미완
        # 배팅 후 선(1: Computer)이 오픈카드를 한 장씩 받는다.
        CSOCard = random.choice(availableCard)
        availableCard.pop(availableCard.index(CSOCard))
        PSOCard = random.choice(availableCard)
        availableCard.pop(availableCard.index(PSOCard))
    
    print("player third Open Card : ", PSOCard)
    print("computer third Open Card : ", CSOCard)
    
    Opened_Card[0].append(PSOCard)
    Opened_Card[1].append(CSOCard)

    print(Opened_Card)

    if Card_Priority() == 0: # player 선
        print("(fourth)player first")
        # 배팅 미완
        # 배팅 후 선(0 : player)이 오픈카드를 한 장씩 받는다.
        PSOCard = random.choice(availableCard)
        availableCard.pop(availableCard.index(PSOCard))
        CSOCard = random.choice(availableCard)
        availableCard.pop(availableCard.index(CSOCard))

    else: # 1일 때 / computer 선
        print("(fourth)computer first")
        # 배팅 미완
        # 배팅 후 선(1: Computer)이 오픈카드를 한 장씩 받는다.
        CSOCard = random.choice(availableCard)
        availableCard.pop(availableCard.index(CSOCard))
        PSOCard = random.choice(availableCard)
        availableCard.pop(availableCard.index(PSOCard))

    print("player fourth Open Card : ", PSOCard)
    print("computer fourth Open Card : ", CSOCard)
    
    Opened_Card[0].append(PSOCard)
    Opened_Card[1].append(CSOCard)

# 히든카드
    if Card_Priority() == 0: # player 선
        print("(fifth)player first")
        # 배팅 미완
        # 배팅 후 선(0 : player)이 오픈카드를 한 장씩 받는다.
        PSOCard = random.choice(availableCard)
        availableCard.pop(availableCard.index(PSOCard))
        CSOCard = random.choice(availableCard)
        availableCard.pop(availableCard.index(CSOCard))

    else: # 1일 때 / computer 선
        print("(fifth)computer first")
        # 배팅 미완
        # 배팅 후 선(1: Computer)이 오픈카드를 한 장씩 받는다.
        CSOCard = random.choice(availableCard)
        availableCard.pop(availableCard.index(CSOCard))
        PSOCard = random.choice(availableCard)
        availableCard.pop(availableCard.index(PSOCard))

    print("player fourth Open Card : ", PSOCard)
    print("computer fourth Open Card : ", CSOCard)
    
    cardList[0].append(PSOCard)
    cardList[1].append(CSOCard)    

    print("playerCard(엎어져있는 카드) :", cardList[0])
    print("playerCard(공개된 카드) : ",Opened_Card[0])
    print("computerCard(엎어져있는 카드) :", cardList[1])
    print("playerCard(공개된 카드) : ",Opened_Card[1])
