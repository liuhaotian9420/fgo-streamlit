from mysql import MySQLSession, ArtsLooper,ArtsLooperBuffs
from model import Loopers, ServantBuffs, sqlite_session as SqliteSession

VIEW_MAPPING = {
    ArtsLooper: Loopers,
    ArtsLooperBuffs: ServantBuffs, 
    # Add more view models as needed
}

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


