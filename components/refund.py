import streamlit as st
import numpy as np  
# 回收相关的模块



def enemies(enemies,hits_dist:list[int],container=None):
    '''
    敌人相关
    
    Parameters:
    - container: container for display
    - enemies: 敌人列表
    - hits_dist: 伤害分布
    '''
    max_overkills = len(hits_dist)
    enemy_count = len(enemies)
    enemy_panels = st.columns([1]*enemy_count,vertical_alignment='center')
    result = []
    if not container:
        for idx,panel in enumerate(enemy_panels):
            mod = panel.number_input(f'敌人{idx+1}回收补正', value=1.0, min_value=0.1, max_value=1.5,)
            overkills = panel.slider(f'敌方{idx+1}过量hit数', min_value=1,max_value=max_overkills,step=1,value=1)
            result.append((enemies[idx], mod, overkills))
    
    return result
            
        
        
    
    
    