import random

N = 2
M = 100000
pattern = ['C','D','H','S']
availableCard = [[i,j]for i in pattern for j in range(1,14)]
cardList=[[] for _ in range (N)]    # 플레이어 카드 
Player_Money = [M]*N                # 나 자신과 컴퓨터 게임 머니
Table_Money = 0                     # 테이블에 배팅된 머니
betting_Money = 300                 # 기본 배팅 금액
rank = [0]*N                        # 플레이어 순서 index값을 저장

def roll():
    # 카드 뭉치?에서 랜덤으로 뽑아 
    # 플레이어 카드 리스트에 카드 정보를 넣는 함수

    for i in range(N):
        tmp = random.randrange(1, len(availableCard))
        cardList[i].append(availableCard[tmp])
        availableCard.pop(tmp)
    return

def Betting_System(): # 베팅 시스템
    # 플레이어가 베팅 순서에 맞게 자신이 
    # 베팅하고 싶은 금액에 맞게 베팅하는 함수

    pass
def Card_Compare(): # 카드 비교 함수(승패 결정)
    # 플레이어 카드 리스트를 각각 비교하여 
    # 제일 높은 점수의 패를 가지고 있는 플레이어가 우승하는 함수
    
    pass

if __name__=="__main__":
    for _ in range(4):
        roll()

    for i in range(N):
        cardList[i].sort()

    print("computerCard: ", cardList[1])
    print("playerCard: ", cardList[0])
    print("삭제할 카드의 인덱스를 입력(0~):",end=' ')
    N = int(input())
    cardList[0].pop(N)
    cardList[1].pop(random.randrange(0,len(cardList[1])))

    print("computerCard: ", cardList[1])
    print("playerCard: ", cardList[0])



