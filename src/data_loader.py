from utils import sqlite_operation
from collections import defaultdict
import json

@sqlite_operation()
def fetch_data(session,table_name,query=None)->json:
    if query is None:
        query = f"SELECT * FROM {table_name}"
    session.execute(query)
    return json.dumps([dict(row) for row in session.fetchall()])


def process_servant_data(data)->dict:
    '''
    处理从者数据
    '''
    svt_data = {}
    name_id_mapping = {}
    for d in data:
        name_id_mapping[d['name']] = d['id']
        svt_data[d['name']] = d
    return svt_data, name_id_mapping

def process_servant_buffs_data(data)->dict:
    buff_info = defaultdict(lambda:defaultdict(list))
    for d in data:
        buff_name = d.get('buff_name','charge')
        if d['skill_type'] != 'active' :
            turn = 3
        elif d['skill_type'] == 'active' and (d['function_target_type'] == 'enemyAll' or d['function_target_type'] == 'enemy'):
            turn = 1
        elif d['turn']<0:
            turn = 3
        else:
            turn = d['turn']
        value =  d.get('value',0)
        servant_id = d['servant_id']
        is_single_target = d['function_target_type'] == 'enemy'
        triggers = 3 if ((d['skill_type'] != 'active' and d['skill_type'] != 'passive') and d['turn']==3) else 1
        buff_info[servant_id][buff_name].append({'turn': turn, 'value': value,'is_single_target': is_single_target,'skill_type': d['skill_type'],'triggers':triggers,'skill_no': d['skill_no']})
    return buff_info

