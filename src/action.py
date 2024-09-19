import numpy as np


def deckShuffle(deck:np.array,deckMap:np.array,mask,seed:int=0):
    
    available_indices = np.where(~mask)[0]
    # np.random.seed(seed)
    card_idx = np.random.choice(available_indices,replace=False,size=5,)
    mask[card_idx] = True
    return deck[card_idx],deckMap[card_idx],mask,card_idx

def reshuffle(deck,deck_map,mask,card_idx,reshuffle_count,requirement_fn,):
    """
    洗牌
    
    Parameters:
    - deck: 初始卡组
    - deck_map: 初始卡组对应从者
    - mask: 发牌记录
    - card_idx: 当前发牌的序数
    - reshuffle_count: 可洗牌
    - requirement_fn: 满足条件的卡片判定函数，返回True/False
    
    Returns:
    - reshuffle_count: 剩余洗牌次数
    - card: 发出的卡片
    - card_map: 发出的卡组来自从者
    - mask: 发牌记录
    - card_idx: 下一次发牌的序数
    """
    
    card = None
    card_map = None
    card = deck[card_idx]
    card_map = deck_map[card_idx]
    
    while reshuffle_count > 0:
        reshuffle_count -= 1
        mask = np.array([False]*15)
        card, card_map, mask,card_idx = deckShuffle(deck,deck_map,mask,requirement_fn)
        if requirement_fn(card,card_map):
            return reshuffle_count,card,card_map,card_idx,mask
    return reshuffle_count,card,card_map,card_idx,mask