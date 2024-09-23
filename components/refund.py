import streamlit as st
import numpy as np  
# 回收相关的模块


def overwrite(key):
    print(f'Overwriting {key}')
    if key == 'default_oks':
        st.session_state.overwrite_default_ok = True
    else:
        raise ValueError(f'Invalid key: {key}')


def enemies(enemies,hits_dist:list[int],container=None,default_oks:int=1):
    '''
    敌人相关
    
    Parameters:
    - container: container for display
    - enemies: 敌人列表
    - hits_dist: 伤害分布
    '''
    with st.expander('敌方配置') as expander:
        max_overkills = len(hits_dist)
        enemy_count = len(enemies)
        enemy_panels = st.columns([1]*enemy_count,vertical_alignment='center')
        result = []
        if not container:
            for idx,panel in enumerate(enemy_panels):
                mod = panel.number_input(f'敌人{idx+1}回收补正', value=1.0, min_value=0.1, max_value=1.5,)                
                overkills = panel.slider(f'敌方{idx+1}过量hit数', min_value=0,max_value=max_overkills,step=1,value=1)                                        
                result.append((enemies[idx], mod, overkills))
    
    return result
            
# 礼装模块        
def craft_essence(ces:list[str],container=None):
    selector,atk = st.columns([1,1],vertical_alignment='center')
    ce_name = selector.selectbox('礼装', options=ces, key='craft_essence',index=None,placeholder='选择礼装')
    atk = atk.number_input('礼装 ATK', value=0, min_value=0, max_value=2400, step=100)
    return {'ce_name': ce_name, 'atk': atk}

# 从者基础数据的模块
def servant_basic(rarity,reset_fn=None):
    default_level = {1:60,2:65,3:70,4:80,5:90}
    default_np_level = 1 if rarity>=4 else 5
    with st.expander('基础数据') as expander:
        level,fufu = st.columns([1,1],vertical_alignment='center')
        if fufu.button('重置基础数据',use_container_width=True):
            reset_fn(rarity)
        servant_level = level.number_input('等级', value=default_level[rarity], min_value=0, max_value=120,step=1,)
        np_level = level.number_input('宝具等级',value=default_np_level,min_value=1, max_value=5, step=1)
        sil,gol = fufu.columns([1,1],vertical_alignment='center')
        silver_fu = sil.checkbox('银芙芙',key='silver_fu')
        golden_fu = gol.checkbox('金芙芙',key='golden_fu')
    return {'level': servant_level,'np_level': np_level,'silver_fu': silver_fu, 'golden_fu': golden_fu}

# 技能相关

def skills():
    setting1,setting2 = st.columns([1,1],vertical_alignment='center')
    default_all_skill = setting1.toggle('全技能开启',value=True)
    ban_one_turn = setting2.toggle('禁止一回合buff',value=False)
    with st.expander('从者 技能') as expander:
        skills,passives = st.columns([1,1],vertical_alignment='center')
        activate_skill_1 = skills.toggle('主动技能1',value=default_all_skill)
        activate_skill_2 = skills.toggle('主动技能2',value=default_all_skill)
        activate_skill_3 = skills.toggle('主动技能3',value=default_all_skill)
        passive_skill_2 = passives.toggle('被动 2',value=True)
        passive_skill_5 = passives.toggle('被动 5',value=False)
        tree = passives.toggle('天赋树',value=False)     
        
    return {'activate_skill_1': activate_skill_1,
            'activate_skill_2': activate_skill_2,
            'activate_skill_3': activate_skill_3,
            'passive_skill_2': passive_skill_2, 
            'passive_skill_5': passive_skill_5,
            'tree': tree,
            'ban_one_turn': ban_one_turn}  

# 拐的选择
def supports(supports):
    
    options,support1,support2,support3 = st.columns([2,2,2,2],vertical_alignment='center')
    change = options.toggle('换人',value=False)
    dual = options.toggle('允许重名',value=True)

    support_1 = support1.selectbox('拐1',options=list(supports),label_visibility='hidden',placeholder='1号拐',index=None)
    support_2 = support2.selectbox('拐2',options=list(supports),label_visibility='hidden',placeholder='2号拐',index=None)
    support_3 = support3.selectbox('拐3',options=list(supports),label_visibility='hidden',placeholder='3号拐',index=None,disabled=not change)
    if not dual and (support_1 == support_2 or support_1 == support_3 or support2 == support_3):
        st.error('请保证拐不重名')
        
    return [support_1,support_2,support_3]        
    
    
    