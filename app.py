import streamlit as st
import pandas as pd
import numpy as np
from collections import defaultdict
from pprint import pprint
from src.calculator import npGain,discardDigitsBeyond
from src.data_loader import fetch_data,process_servant_buffs_data,process_servant_data,process_craft_essence_data
from src.utils import reverse_mapping
from components.refund import enemies,servant_basic,supports,skills,craft_essence


def sum_buff(buff_dict,buff_type,ban_one_turn=False,skills_activated=None):
    
    buff_lst = buff_dict.get(buff_type, [])  
    
    if not buff_lst:
        return 0 
    
    divider = 100 if buff_type == 'charge' else 10
    
    if skills_activated:
        buff_lst = [bf for bf in buff_lst if skills_activated[bf['skill_no']-1 ] and not (bf['skill_type']=='active' and bf['skill_no']==0)]
    
    if ban_one_turn:
        return sum([bf['value'] for bf in buff_lst if bf['turn']>1])/divider
    
    return sum([bf['value'] for bf in buff_lst])/divider    

def calc_increase(current,original):
    if original == 0:
        return '-'
    else:
        return str(round((current)/(original),3) * 100 - 100)+'%'

def initialize_session_state():
    
    if 'default_gr' not in st.session_state:
        st.session_state.default_gr = 0

    if 'default_mb' not in st.session_state:
        st.session_state.default_mb = 0

    if 'default_regain' not in st.session_state:
        st.session_state.default_regain = 0

    if 'silver_fu' not in st.session_state:
        st.session_state.silver_fu = True
        
    if 'golden_fu' not in st.session_state:
        st.session_state.golden_fu = False
        
    if 'ce_atk' not in st.session_state:
        st.session_state.ce_atk = 0
        
    if 'level' not in st.session_state:
        st.session_state.level = 0

def reset_added_buffs():
    st.session_state['default_mb'] = 0
    st.session_state['default_gr'] = 0
    st.session_state['default_regain'] = 0

def reset_basics(rarity):
    
    default_level = {1:60,2:65,3:70,4:80,5:90}

    st.session_state['golden_fu'] = False
    st.session_state['silver_fu'] = True
    st.session_state['ce_atk'] = 0
    st.session_state['np_level'] = 1 if svt_data['rarity']>=4 else 5    
    st.session_state['level'] = default_level[rarity]


st.set_page_config(page_title="FGO 模拟", page_icon='assets/images/favicon_fgo.png')
st.title('蓝光炮回收计算🏄',)

servants,name_id_mapping = process_servant_data(fetch_data('loopers'))
meta_supports = fetch_data('supports')
name_id_mapping.update({sp['name']:sp['id'] for sp in meta_supports})
servant_buffs = process_servant_buffs_data(fetch_data('servant_buffs'))

ce_data = fetch_data('craft_essence')
ce_buffs = process_craft_essence_data(ce_data)
name_id_mapping.update({ce['ce_name']:ce['ce_id'] for ce in ce_data})

id_name_mapping = reverse_mapping(name_id_mapping)
test_enemies = [1,1,1]



svt_name = st.selectbox('选择从者',name_id_mapping.keys(),)
svt_data = servants[svt_name]
svt_buff = servant_buffs[name_id_mapping[svt_name]]


basics = servant_basic(svt_data['rarity'],reset_fn=reset_basics)
support_lst = supports([sp['name'] for sp in meta_supports])
ce = craft_essence([ce['ce_name'] for ce in ce_data])
skill_settings = skills()
ban_one_turn = skill_settings['ban_one_turn']
hits = svt_data['np_hits'].split(',')    


with st.expander('额外 BUFF') as expander:
    
    buffs,button = st.columns([3,2],vertical_alignment='center')
    if button.button('重置自定义 Buff',use_container_width=True):
        reset_added_buffs()
    regain = button.number_input('缓冲',0,100,step=5,key='default_regain')
    npGainUp = buffs.slider('黄金律', 0,400,step=1,key='default_gr')
    commandUp = buffs.slider('蓝魔放',0,400,step=1,key='default_mb')

enemy_panels = enemies(test_enemies, hits)

# 计算所有的 buff 

skills_activated = [skill_settings['activate_skill_1'],skill_settings['activate_skill_2'], skill_settings['activate_skill_3']]
append_skill_2 = skill_settings['passive_skill_2']

active_skill_buff = {
    'npGainUp':sum_buff(svt_buff,'NP Gain Up',ban_one_turn=ban_one_turn,skills_activated=skills_activated),
    'commandUp':(
                sum_buff(svt_buff,'Arts Up',ban_one_turn=ban_one_turn,skills_activated=skills_activated) 
                + sum_buff(svt_buff,'Arts Attack Resistance Down',ban_one_turn=ban_one_turn,skills_activated=skills_activated)
                ),
    'charge':sum_buff(svt_buff,'charge',skills_activated=skills_activated) + (20 if append_skill_2 else 0)
    
}
support_buffs = defaultdict(float)
for sup in support_lst:
    if sup in name_id_mapping:
        buff = servant_buffs[name_id_mapping[sup]]
        support_buffs['npGainUp'] += sum_buff(buff,'NP Gain Up',ban_one_turn=ban_one_turn)
        support_buffs['commandUp'] += sum_buff(buff,'Arts Up',ban_one_turn=ban_one_turn)
        support_buffs['charge'] += sum_buff(buff,'charge',skills_activated=skills_activated)

ce_buff = defaultdict(float)
if ce['ce_name']:
    ce_buff['npGainUp'] = sum_buff(ce_buffs[name_id_mapping[ce['ce_name']]],'NP Gain Up',ban_one_turn=ban_one_turn) if name_id_mapping[ce['ce_name']] else 0 
    ce_buff['commandUp'] = sum_buff(ce_buffs[name_id_mapping[ce['ce_name']]],'Arts Up',ban_one_turn=ban_one_turn) if name_id_mapping[ce['ce_name']] else 0
    ce_buff['charge'] = sum_buff(ce_buffs[name_id_mapping[ce['ce_name']]],'charge',) if name_id_mapping[ce['ce_name']]  else 0


added_buffs = {'npGainUp':npGainUp,'commandUp':commandUp,}

command_up,np_gain_up,current_np = st.columns([1,1,1],vertical_alignment='center')

commandUpTotal = command_up.metric('蓝魔放',value=active_skill_buff['commandUp']+added_buffs['commandUp']+support_buffs['commandUp']+ce_buff['commandUp']
                        , delta=calc_increase(active_skill_buff['commandUp']+added_buffs['commandUp']+support_buffs['commandUp']+ce_buff['commandUp'],active_skill_buff['commandUp'])
                        )
npGainUpTotal = np_gain_up.metric('黄金律',value=active_skill_buff['npGainUp']+added_buffs['npGainUp']+support_buffs['npGainUp']+ce_buff['npGainUp'],
                                delta=calc_increase(active_skill_buff['npGainUp']+added_buffs['npGainUp']+support_buffs['npGainUp']+ce_buff['npGainUp'],active_skill_buff['npGainUp'])
)
chargeTotal = current_np.metric('充能',value=active_skill_buff['charge']+support_buffs['charge']+ce_buff['charge'])   



# 伤害结算面板
total_np = 0
percentage = 0
for idx,mod,overkill in enemy_panels:
    if overkill > len(hits):
        st.error('过量 hit数不能大于 hits')
        break
    overkills = [1 if len(hits)-idx<=overkill else 0 for idx,i in enumerate(hits) ]
    total_np+=npGain(3.0,command_up=(active_skill_buff['commandUp']+added_buffs['commandUp']+support_buffs['commandUp']+ce_buff['commandUp'])/100,
            np_gain_up=(active_skill_buff['npGainUp']+added_buffs['npGainUp']+support_buffs['npGainUp']+ce_buff['npGainUp'])/100,
            np_rate = svt_data['np_rate']/100,
            np_regain=regain,
            overkill=overkills,
            mod=mod)  
    # 计算伤害占比
    percentage+=int(hits[0:np.where(np.array(overkills)==1)[0][0]+1][-1])
    
refund = discardDigitsBeyond(total_np,2)
damage_board,refund_board = st.columns([1,1],vertical_alignment='center')
dmg = damage_board.metric('有效伤害占比', value=str(percentage)+'%',)
rfd = refund_board.metric('回收', value=refund,)