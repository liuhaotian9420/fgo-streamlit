import streamlit as st
import pandas as pd
from src.data_loader import fetch_data,process_servant_buffs_data,process_servant_data
from src.utils import reverse_mapping
from components.refund import enemies

st.set_page_config(page_title="FGO 模拟", page_icon='assets/images/favicon_fgo.png')
st.title('蓝光炮回收计算🏄',)

servants,name_id_mapping = process_servant_data(fetch_data('loopers'))
id_name_mapping = reverse_mapping(name_id_mapping)
servant_buffs = process_servant_buffs_data(fetch_data('servant_buffs'))
test_enemies = [1,1,1]
hits_dist = [1,2,3,4]

enemy_panels = enemies(test_enemies, hits_dist)

# for panel,ok in enemy_panels:
#     panel_data = panel 
#     ok_data = ok
        



# svt_name = st.selectbox('选择从者',name_id_mapping.keys(),)

# default_level = {1:60,2:65,3:70,4:80,5:90}
# svt_data = data[name_id_mapping[svt_name]]
# svt_buff = buff_info[name_id_mapping[svt_name]]
# hits = svt_data['card_dist_acc'].split(',')

# def1,support1,support2,support3 = st.columns([2,2,2,2],vertical_alignment='center')
# default_all_skill = def1.toggle('全技能开启',value=True)
# ban_one_turn = def1.toggle('禁止一回合buff',value=False)
# change = def1.toggle('换人',value=False)

# support_1 = support1.selectbox('拐1',options=['无']+list(supports_name_id_mapping.keys()),label_visibility='hidden',placeholder='1号拐',index=None)
# support_2 = support2.selectbox('拐2',options=['无']+list(supports_name_id_mapping.keys()),label_visibility='hidden',placeholder='2号拐',index=None)
# support_3 = support3.selectbox('拐3',options=['无']+list(supports_name_id_mapping.keys()),label_visibility='hidden',placeholder='3号拐',index=None,disabled=not change)

# sp1_buff = support_buff_info[supports_name_id_mapping[support_1]] if support_1!='无' and support_1 is not None else {}
# sp2_buff = support_buff_info[supports_name_id_mapping[support_2]] if support_2!='无' and support_2 is not None else {}
# sp3_buff = support_buff_info[supports_name_id_mapping[support_3]] if support_3!='无' and support_3 is not None else {}

# sp_mb = sum_buff(sp1_buff,'Arts Up',ban_one_turn=ban_one_turn) + sum_buff(sp2_buff,'Arts Up',ban_one_turn=ban_one_turn) + sum_buff(sp3_buff,'Arts Up',ban_one_turn=ban_one_turn)
# sp_gr = sum_buff(sp1_buff,'NP Gain Up',ban_one_turn=ban_one_turn) + sum_buff(sp2_buff,'NP Gain Up',ban_one_turn=ban_one_turn) + sum_buff(sp3_buff,'NP Gain Up',ban_one_turn=ban_one_turn)
# sp_charge = sum_buff(sp1_buff,'charge') + sum_buff(sp2_buff,'charge') + sum_buff(sp3_buff,'charge')


# if 'np_level' not in st.session_state:
#     st.session_state.np_level = 1 if svt_data['servant_rarity']>=4 else 5

# with st.expander('基础数据') as expander:
#     level,fufu = st.columns([2,1])
#     if fufu.button('重置基础数据',use_container_width=True):
#         reset_basics(svt_data['servant_rarity'])
#     level.slider('等级', value=default_level[svt_data['servant_rarity']], min_value=90, max_value=120,step=1)
#     level.slider('礼装最大白值',max_value=2400,step=100,key='ce_atk')
#     np_level = fufu.number_input('宝具等级',key='np_level',min_value=1, max_value=5, step=1)
#     sil,gol = fufu.columns([1,1],vertical_alignment='center')
#     silver_fu = sil.checkbox('银芙芙',key='silver_fu')
#     golden_fu = gol.checkbox('金芙芙',key='golden_fu')



# with st.expander('从者 技能') as expander:
#     skills,passives = st.columns([1,1],vertical_alignment='center')
#     activate_skill_1 = skills.toggle('主动技能1',value=default_all_skill)
#     activate_skill_2 = skills.toggle('主动技能2',value=default_all_skill)
#     activate_skill_3 = skills.toggle('主动技能3',value=default_all_skill)
#     passive_skill_2 = passives.toggle('被动 2',value=True)
#     passive_skill_5 = passives.toggle('被动 5',value=False)
#     tree = passives.toggle('天赋树',value=False)

# with st.expander('额外 BUFF') as expander:
#     # if st.button('reset'):
#     #     reset()

#     buffs,button = st.columns([3,2],vertical_alignment='center')
#     # ce = button.selectbox('礼装',[],index=1)
#     if button.button('重置自定义 Buff',use_container_width=True):
#         reset_buffs()
#     regain = button.number_input('缓冲',0,100,step=5,key='default_regain')
#     golden_rule = buffs.slider('黄金律', 0,400,step=1,key='default_gr')
#     arts_mana_burst = buffs.slider('蓝魔放',0,400,step=1,key='default_mb')


# skills_activated = [activate_skill_1,activate_skill_2,activate_skill_3,]

# current_mana_burst,current_golden_rule,current_np = st.columns([1,1,1],vertical_alignment='center')

# # 主动技能默认
# default_golden_rule = sum_buff(svt_buff,'NP Gain Up',ban_one_turn=ban_one_turn,skills_activated=skills_activated)
# default_arts =(
#             sum_buff(svt_buff,'Arts Up',ban_one_turn=ban_one_turn,skills_activated=skills_activated) 
#             + sum_buff(svt_buff,'Arts Attack Resistance Down',ban_one_turn=ban_one_turn,skills_activated=skills_activated)
# )
# default_charges = sum_buff(svt_buff,'charge',skills_activated=skills_activated)


# def calc_increase(current,original):
#     if original == 0:
#         return '-'
#     else:
#         return str(round((current-original)/(original),3) * 100 - 100)+'%'


# cmb = current_mana_burst.metric('蓝魔放',value=default_arts+arts_mana_burst+sp_mb,
#                                  delta=calc_increase(default_arts+arts_mana_burst+sp_mb,arts_mana_burst))
# cgr = current_golden_rule.metric('黄金律',value=default_golden_rule+golden_rule+sp_gr,
#                                  delta=calc_increase(default_golden_rule+golden_rule+sp_gr,golden_rule))
# cnp = current_np.metric('NP',value=default_charges+sp_charge+(20 if passive_skill_2 else 0),
#                         delta=0)

# with st.expander('敌方数据') as expander:

#     e1,e2,e3 = st.columns([1,1,1],vertical_alignment='center')

#     enemy_mod_1 = e1.number_input('敌方补正1', value=1.0, min_value=0.1, max_value=1.5)
#     ok_1 = e1.slider('敌方1过量hit数', min_value=1,max_value=len(hits),step=1,value=1)
#     enemy_mod_2 = e2.number_input('敌方补正2', value=1.0, min_value=0.1, max_value=1.5)
#     ok_2 = e2.slider('敌方2过量hit数', min_value=1,max_value=len(hits),step=1,value=1)
#     enemy_mod_3 = e3.number_input('敌方补正3', value=1.0, min_value=0.1, max_value=1.5)
#     ok_3 = e3.slider('敌方3过量hit数', min_value=1,max_value=len(hits),step=1,value=1)




# # 伤害结算面板
# total_np = 0
# percentage = 0
# for mod,overkill in zip([enemy_mod_1,enemy_mod_2,enemy_mod_3], [ok_1,ok_2,ok_3]):
#     if overkill > len(hits):
#         st.error('过量 hit数不能大于 hits')
#         break
#     overkills = [1 if len(hits)-idx<=overkill else 0 for idx,i in enumerate(hits) ]
#     total_np+=npGain(3.0,a=default_arts+arts_mana_burst+sp_mb,
#             np_gain_buff=default_golden_rule+golden_rule+sp_gr,
#             np_rate = svt_data['servant_np_rate']/100,
#             gainEffect=regain,
#             overkill=overkills,
#             mod=mod)  
#     # 计算伤害占比
#     percentage+=int(hits[0:np.where(np.array(overkills)==1)[0][0]+1][-1])
    
# total_damage = 123456
# refund = discardDigitsBeyond(total_np,2)

# damage_board,refund_board = st.columns([1,1],vertical_alignment='center')
# dmg = damage_board.metric('有效伤害占比', value=str(percentage)+'%',)
# rfd = refund_board.metric('回收', value=refund,)