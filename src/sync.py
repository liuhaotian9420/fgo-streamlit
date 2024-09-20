from mysql import MySQLSession, ArtsLooper,ArtsLooperBuffs,ArtsMetaSupport,ArtsCraftEssence
from model import Loopers, ServantBuffs, Supports,CraftEssence,sqlite_session as SqliteSession

VIEW_MAPPING = {
    # ArtsLooper: Loopers,
    # ArtsLooperBuffs: ServantBuffs, 
    # ArtsMetaSupport:ServantBuffs,
    ArtsCraftEssence:CraftEssence
    
    # Add more view models as needed
}

# 拐
# session = SqliteSession()
# session.add_all([Supports(name='阿尔托莉雅·卡斯特',id=504500),
#                  Supports(name='吉尔伽美什',id=501800),
#                  Supports(name='尼禄·克劳狄乌斯〔新娘〕',id=100600),
#                  Supports(name='阿瓦隆女士',id=2800300),
#                  Supports(name='徐福',id=1001400),
#                  Supports(name='阿斯克勒庇俄斯',id=504300),
#                  Supports(name='玉藻前',id=500300),
#                  Supports(name='冯·霍恩海姆·帕拉塞尔苏斯',id=501000),
#                  ])
# session.commit()
# session.close()

def migrate_data(view_model, sqlite_model, mysql_session, sqlite_session)-> None:
    """Migrates data from a MySQL view to an SQLite table."""
    # Fetch data from MySQL view
    mysql_data = mysql_session.query(view_model).all()
    
    # Map MySQL data to SQLite model
    for record in mysql_data:
        mapped_record = sqlite_model(
            **{column.name: getattr(record, column.name) for column in sqlite_model.__table__.columns if column.name !='record_id'}
        )
        sqlite_session.merge(mapped_record)


def migrate_all_views():
    """Migrates all views defined in the VIEW_TO_MODEL_MAPPING."""
    mysql_session = MySQLSession()
    sqlite_session = SqliteSession()

    try:
        for mysql_view, sqlite_model in VIEW_MAPPING.items():
            print(f"Migrating {mysql_view.__tablename__} to {sqlite_model.__tablename__}...")
            migrate_data(mysql_view, sqlite_model, mysql_session, sqlite_session)
            sqlite_session.commit()
            print(f"Migration of {mysql_view.__tablename__} completed.")
    except Exception as e:
        sqlite_session.rollback()
        print(f"Error occurred: {e}")
    finally:
        mysql_session.close()
        sqlite_session.close()

# Run the migration
if __name__ == '__main__':
    migrate_all_views()


