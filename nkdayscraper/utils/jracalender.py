# %%
class JraCalendar():
    @staticmethod
    def is_year(year):
        import datetime as dt
        try:
            dt.datetime.strptime(f'{year}-01-01', "%Y-%m-%d")
            return True
        except ValueError:
            return False

    @staticmethod
    def get_annual_schedule_json(year):
        import requests as rq
        for month in range(1, 13):
            file_name = f'{year}{month:02}.json'
            url = f'https://jra.jp/keiba/common/calendar/json/{file_name}'
            file_path = f'data/json/calendar/{file_name}'
            print(url)
            response = rq.get(url)
            response.encoding = response.apparent_encoding
            with open(file_path, 'wb') as f:
                f.write(response.content)

    def get_json(self):
        from sys import argv
        import datetime as dt
        index = 2 if len(argv) > 1 and argv[1] == 'get_annual_schedule_json' else 1
        year = argv[index] if len(argv) > index and self.is_year(argv[index]) else dt.date.today().year
        self.get_annual_schedule_json(year)

if __name__ == '__main__':
    jraCalendar = JraCalendar()
    jraCalendar.get_json()
