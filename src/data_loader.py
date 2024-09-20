from .utils import sqlite_operation
from collections import defaultdict
import json
from sqlalchemy import text

@sqlite_operation()
def fetch_data(session,table_name,query=None)->json:
    if query is None:
        query = text(f"SELECT * FROM {table_name}")
    result = session.execute(query)
    rows = result.fetchall()
    return json.loads(json.dumps([dict(row._mapping) for row in rows]))


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
        buff_name = d.get('buff_name') if d['buff_name'] is not None else 'charge'
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
        buff_info[servant_id][buff_name].append({'turn': turn, 'value': value,
                                                 'is_single_target': is_single_target,
                                                 'skill_type': d['skill_type'],
                                                 'triggers':triggers,
                                                 'skill_no': d['skill_no'],
                                                 'function_target_type': d['function_target_type'],})
    return buff_info

def process_craft_essence_data(data)->dict:
    buff_info = defaultdict(lambda:defaultdict(list))
    for d in data:
        buff_name = d.get('buff_name','charge')
        value =  d.get('value',0)
        ce_id = d['ce_id']
        buff_info[ce_id][buff_name].append({'turn': 3, 'value': value,'skill_type': 'passive','skill_no': 0,'is_single_target': False,})
    return buff_info
