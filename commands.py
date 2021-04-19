if __name__ == '__main__':
    from nkdayscraper.models import engine, Base, Racecourses#, create_tables, drop_tables, drop_race_tables
    from sys import argv

    if argv[1] == 'create_tables':
        print(argv[1])
    elif argv[1] == 'drop_tables':
        print(argv[1])
    elif argv[1] == 'drop_race_tables':
        print(argv[1])
    elif argv[1] == 'recreate_racecourses':
        print(argv[1])

        Base.metadata.drop_all(engine, tables=[Racecourses.__table__])
        Base.metadata.create_all(engine, tables=[Racecourses.__table__])

        rc_list = [
            Racecourses(id='01', name='札幌'),
            Racecourses(id='02', name='函館'),
            Racecourses(id='03', name='福島'),
            Racecourses(id='04', name='新潟'),
            Racecourses(id='05', name='東京'),
            Racecourses(id='06', name='中山'),
            Racecourses(id='07', name='中京'),
            Racecourses(id='08', name='京都'),
            Racecourses(id='09', name='阪神'),
            Racecourses(id='10', name='小倉')
        ]

        from sqlalchemy.orm import sessionmaker
        Session = sessionmaker(bind=engine, future=True)

        with Session() as session:
            try:
                session.add_all(rc_list)
                session.commit()
            except:
                session.rollback()
                raise

    else:
        print(f"'{argv[1]}' is not found in prepared commands.")
