from sqlalchemy import create_engine, Table,Column, Integer, String, ForeignKey,Boolean,Float,BIGINT
from sqlalchemy.orm import DeclarativeBase,relationship,declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

DATABASE_URI = 'sqlite:///data/fgo.db'

engine = create_engine(DATABASE_URI)
sqlite_session = sessionmaker(bind=engine)


class Loopers(Base):
    
    __tablename__ = 'loopers'
    
    id = Column(Integer, primary_key=True,comment='从者id')
    name = Column(String(255), nullable=False,comment='从者中文名')
    rarity = Column(Integer, nullable=False, comment='星级')
    class_name = Column(String(255), nullable=False, comment='职介')
    atk = Column(Integer, nullable=False, comment='最大攻击力')
    tendancy = Column(Integer, nullable=False, comment='攻防总倾向')
    np_rate = Column(Float, nullable=False, comment='NP获取率')
    np_hits = Column(String(255), nullable=False, comment='NP命中数') 
    is_strengthened = Column(Boolean, nullable=False, comment='是否已强化')
    class_mod = Column(Integer, nullable=False, comment='职介补正')
    attribute = Column(String(255), nullable=False, comment='阵营')
    traits = Column(String(255), nullable=False, comment='特性')
    star_absorb = Column(Integer, nullable=False, comment='集星率')
    star_gen = Column(Integer, nullable=False, comment='打星率')
    
    
class Supports(Base):
    
    __tablename__ ='supports'
    
    id = Column(Integer, primary_key=True, comment='从者id')
    name = Column(String(255), nullable=False, comment='从者中文名')
    
    

class ServantBuffs(Base):
    
    __tablename__ ='servant_buffs'
    
    servant_id = Column(Integer, nullable=False, comment='从者id',primary_key=True,)
    servant_name = Column(String(255), nullable=False, comment='从者中文名')
    skill_type = Column(String(255), nullable=True, comment='技能类型')
    skill_no = Column(Integer, nullable=False, comment='技能序号',primary_key=True,)
    buff_name = Column(String(255), nullable=True, comment='buff名称',primary_key=True,)
    buff_type = Column(String(255), nullable=True, comment='buff类型')
    function_target_type = Column(String(255), nullable=True, comment='效果对目标的影响')  # 可能为None，表示对所有
    function_type = Column(String(255), nullable=True, comment='效果类型',primary_key=True,) 
    function_target_traits = Column(String(255), nullable=True, comment='效果对特性的影响',primary_key=True,)
    value = Column(Integer, nullable=True, comment='buff值',primary_key=True,)
    count = Column(Integer, nullable=True, comment='buff次数')
    turn = Column(Integer, nullable=True, comment='buff持续回合数',primary_key=True,)
    rate = Column(Integer, nullable=True, comment='buff命中率')
    userate = Column(Integer, nullable=True, comment='buff生效几率') 
    
class CraftEssence(Base):
    
    __tablename__ ='craft_essence'
    ce_id = Column(Integer, primary_key=True, comment='id')
    ce_name = Column(String(255), nullable=False, comment='名称')
    buff_name = Column(String(255), nullable=False, comment='buff名称')
    buff_type = Column(String(255), nullable=False, comment='buff类型')
    value = Column(Integer, nullable=False, comment='buff值')
    turn = Column(Integer, nullable=False, comment='buff持续回合数')
    cost = Column(Integer, nullable=False, comment='消耗')
    max_atk = Column(Integer, nullable=False, comment='buff对攻击力的影响')