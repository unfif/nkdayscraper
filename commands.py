# %%
if __name__ == '__main__':
    from nkdayscraper.models import engine, Base, Racecourses, Racedates, drop_race_related_tables, drop_race_tables
    from sys import argv

    def recreate_racecourses():
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

    def recreate_racedates():
        Base.metadata.drop_all(engine, tables=[Racedates.__table__])
        Base.metadata.create_all(engine, tables=[Racedates.__table__])

    def check_records():
        from nkdayscraper.models import Race, HorseResult
        from sqlalchemy.orm import Session

        query = getQueryForDatesOfExistsRecords()\
        .filter(HorseResult.passageratelist == None)\
        .order_by(Race.date.desc())

        print(query.compile(compile_kwargs={"literal_binds": True}))

        with Session(engine) as session:
            result = session.execute(query)

        print('----------------------------------------[ incomplete_records ]----------------------------------------')
        for row in result.fetchall():
            print(row[0].strftime('%Y-%m-%d'))

        print('------------------------------------------------------------------------------------------------------')

    def exists_records():
        from nkdayscraper.models import Race, HorseResult
        from sqlalchemy.orm import Session

        query = getQueryForDatesOfExistsRecords()\
        .order_by(Race.date.desc())

        print(query.compile(compile_kwargs={"literal_binds": True}))

        with Session(engine) as session:
            result = session.execute(query)

        print('------------------------------------------[ exists_records ]------------------------------------------')
        for row in result.fetchall():
            print(row[0].strftime('%Y-%m-%d'))

        print('------------------------------------------------------------------------------------------------------')

    def getQueryForDatesOfExistsRecords():
        from sqlalchemy.future import select
        from nkdayscraper.models import Race, HorseResult
        query = select(Race.date.distinct()).join(HorseResult)\
        .filter(HorseResult.margin.notin_((('除外', '中止', '取消'))))
        return query

    def count_records():
        from nkdayscraper.models import HorseResult
        print(HorseResult.countResults())

    def display_help():
        print('-------------------------------------------[ command_list ]-------------------------------------------')
        print('create_tables:            this command creates all tables in model.')
        print('drop_race_related_tables: this command drops all tables related race.')
        print('drop_race_tables:         this command drops tables of race.')
        print('recreate_racecourses:     this command drops and creates Racecourses table.')
        print('recreate_racedates        this command drops and creates Racedates table.')
        print('check_records:            this command checks incomplate records and displays race date.')
        print('exists_records:           this command checks exists records and displays race date.')
        print('count_records:            this command count for Race and HorseResult')
        print('get_annual_schedule_json: this command downloads race schedules of JRA by JSON. (argv[2]: year)')
        print('------------------------------------------------------------------------------------------------------')

    if argv[1] == 'help':
        display_help()
    elif argv[1] == 'create_tables':
        Base.metadata.create_all(engine)
    elif argv[1] == 'drop_race_related_tables':
        drop_race_related_tables(engine)
    elif argv[1] == 'drop_race_tables':
        drop_race_tables(engine)
    elif argv[1] == 'recreate_racecourses':
        recreate_racecourses()
    elif argv[1] == 'recreate_racedates':
        recreate_racedates()
    elif argv[1] == 'check_records':
        check_records()
    elif argv[1] == 'exists_records':
        exists_records()
    elif argv[1] == 'count_records':
        count_records()
    elif argv[1] == 'get_annual_schedule_json':
        from nkdayscraper.utils.jracalender import JraCalendar
        jraCalendar = JraCalendar()
        jraCalendar.get_json()
    else:
        print(f"'{argv[1]}' is not found in prepared commands.")
        display_help()

    print('done...')

# %%
