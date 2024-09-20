from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP
import random
import numpy as np
import math

def discardDigitsBeyond(number:float,digits:int=2):
    '''
    舍弃小数点后 digits 位以后的数字
    number: 输入的数字
    digits: 舍弃的位数，默认为 2
    '''
    result = float(str(number).split('.')[0] + '.' + ''.join(str(number).split('.')[1][:digits]))
    return result

def npGain(card_rate,command_up=0,np_gain_up=0,np_rate:float=0,
           np_regain:int=0,overkill:list=[],
           is_crit=False,is_ex=False,
           arts_head=False, mod=1):
    
    '''
    计算指令卡/宝具的 NP 回收
    card_rate: 指令卡 NP 倍率
    command_up: A 类 buff
    np_gain_up: 黄金律
    np_rate: 基础 NP 回收
    np_regain: 回收效果(直充缓冲等)
    overkill: 过量
    is_crit: 是否暴击
    is_ex: ex 指令卡
    arts_head: 首蓝补正
    '''
    hits = np.arange(len(overkill))
    total_np = 0 
    arts_mod = (1 if arts_head else 0)
    for h in hits:
        base_np = discardDigitsBeyond(mod*np_rate*(card_rate*(1+command_up)+arts_mod)*(1+np_gain_up)*(2 if is_crit and not is_ex else 1),2)
        if overkill[h] == 1:
            base_np = discardDigitsBeyond(base_np*1.5,2)
        total_np += base_np
    
    return discardDigitsBeyond(total_np,2)+np_regain


def critStarDistribute(mask:np.array,
                       star_rate:np.array,
                       total_stars:int=0,
                       absorb_rateup:list[float]=[]):
    """
    模拟暴击星分配
    
    Parameters:
    - mask:指令卡序数，长度为 5，代表当前选取的 5 张卡,例如 [1,2,3,4,5] 代表选取序号为 1-5 的卡
    - star_rate: 指令卡基础集星率，长度为 5, 和 mask 同序
    - absorb_rateup: 集星率 buff
    - total_stars: 总星星数量
    
    Returns: 
    - A dictionary containing the distribution of cards with their counts
    """
    
    cards = defaultdict(int)
    fixed_weights = np.array([50, 20, 20, 0, 0])
    np.random.shuffle(fixed_weights)
    
    # Calculate adjusted weights
    weights = (star_rate * (np.array(absorb_rateup) + 1)) + fixed_weights
    ajusted_weights = weights / weights.sum()
    
    for _ in range(total_stars):
        # Draw a card index based on the adjusted weights
        selected_card = np.random.choice(mask, p=ajusted_weights)
        
        # Check the count for the selected card, ensure max of 10
        while cards[selected_card] >= 10:
            selected_card = np.random.choice(mask, p=ajusted_weights)
        
        cards[selected_card] += 1
    
    return cards


def damageCalculate(card_rate: float = 0, command_up: float = 0, atk_up: float = 0,
                    np_damage_up: float = 0, np_special_damage: float = 0,
                    crit: float = 0, damage_mod: float = 0, command_up_np: float = 0,
                    buster_head: bool = True, is_ex: bool = False,  np_rate: float = 6 * 1.5,
                    atk: int = 11000, is_buster_chain: bool = True,  rand: float = 0.9,
                    attribute_advantage: float = 1, is_np: bool = False, is_crit: bool = True,
                    class_advantage: float = 1, class_mod: float = 1):
    """
    Calculate damage based on various modifiers.

    Parameters:
    - card_rate: Base damage multiplier for the command card.
    - command_up: Command card damage buff.
    - atk_up: Attack buff multiplier.
    - np_damage_up: NP damage buff multiplier.
    - np_special_damage: Special NP damage buff multiplier.
    - crit: Critical damage multiplier.
    - damage_mod: Special damage modifier.
    - command_up_np: NP-specific command card damage buff multiplier.
    - buster_head: Whether Buster chain bonus is applied.
    - is_ex: Whether it's an EX card.
    - np_rate: NP multiplier (default is for 1st NP level).
    - atk: Base attack value.
    - is_buster_chain: Whether it's a Buster chain.
    - rand: Random factor in damage calculation.
    - attribute_advantage: Attribute advantage multiplier.
    - is_np: Whether it's an NP attack.
    - is_crit: Whether it's a critical hit.
    - class_advantage: Class advantage multiplier.
    - class_mod: Class-specific multiplier.

    Returns:
    - precise_damage: Calculated damage considering the given modifiers.
    - equivalent_np_rate: Adjusted NP rate considering the card damage.
    - total_buff: Overall buff multiplier.
    """
    # Set EX card multiplier
    ex_rate = Decimal(3.5 if is_ex else 1)
    
    # Buster chain bonus
    buster_head_rate = Decimal(0.5 if buster_head else 0)
    
    # Calculate base card and NP damage multipliers
    command_buff = Decimal((1 + command_up) * card_rate + buster_head_rate).quantize(Decimal('0.001'), ROUND_HALF_UP)
    atk_buff = Decimal(1 + atk_up).quantize(Decimal('0.001'), ROUND_HALF_UP)
    crit_mod = Decimal(1 + (crit if is_crit else 0) + damage_mod).quantize(Decimal('0.001'), ROUND_HALF_UP)
    
    # Calculate chain bonus for non-EX cards in a Buster chain
    chain_bonus = Decimal(0.2 * atk if is_buster_chain and not is_ex else 0).quantize(Decimal('0.001'), ROUND_HALF_UP)
    
    # Calculate total card damage
    card_damage = (
        Decimal(atk) * Decimal(0.23) * command_buff * atk_buff * crit_mod *
        (2 if is_crit and not is_ex else 1) * ex_rate + chain_bonus
    )
    
    # Calculate NP damage
    raw_np_damage = (
        Decimal(atk * 0.23 * (1 + command_up_np) * (1 + atk_up) * (1 + damage_mod + np_damage_up) * (1 + np_special_damage))
    ).quantize(Decimal('0.001'), ROUND_HALF_UP) * Decimal(np_rate)
    
    # Calculate equivalent NP rate based on card damage
    equivalent_np_rate = (card_damage / raw_np_damage) * Decimal(np_rate)
    
    # Calculate total buff multiplier
    total_buff = (raw_np_damage / Decimal(np_rate) * Decimal(class_advantage) * Decimal(class_mod))
    
    # Calculate precise np damage
    precise_np_damage = raw_np_damage * Decimal(rand) * Decimal(attribute_advantage) * Decimal(class_mod) * Decimal(class_advantage)
    
    # Return calculated equivalent NP rate and total buff ratio
    return precise_np_damage if is_np else card_damage, math.ceil(float(equivalent_np_rate) * 100), round(float(total_buff) / (atk * 0.23), 2)



def critStarGen(hits:int, base_rate,card_rate, star_drop_up_rate=0,
                command_up =0, is_quick_head=False,crit=False,overkill=False,
                enemy_mod=0, ):
    """
    Calculate critical star generation based on various modifiers.
    
    Parameters:
    - card_rate: Base damage multiplier for the command card.
    - base_rate: 基础产星率
    - card_rate: 指令卡产星率
    - star_drop_up_rate: 星星掉落率 buff
    - command_up: A 类 buff
    - is_quick_head: 是否首绿
    - crit: 是否暴击
    - overkill: 过量
    - enemy_mod: 敌方补正
    
    Returns:
    - star_count: 产出的星星数量
    """
    crit_mod = 0.2 if crit else 0
    overkill_mod = 0.3 if overkill else 0
    head_mod = 0.2 if is_quick_head else 0
    total_star_rate = min(base_rate+card_rate*(1+command_up)+star_drop_up_rate+enemy_mod+head_mod+crit_mod+overkill_mod,3)
    base_star = total_star_rate // 1 * hits
    float_star = random.binomialvariate(hits, total_star_rate % 1)
    return base_star+float_star