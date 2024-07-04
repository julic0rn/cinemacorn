import requests
from bs4 import BeautifulSoup

BASE_URL = "https://kinotickets.express"
CINEMA_PATHS = [
    "/ingolstadt-cinema1",
    "/ingolstadt-cinema2",
    "/ingolstadt_donau-flimmern",
]

class ScheduleItem:
    def __init__(self, date, times):
        self.date = date
        self.times = times

class Schedule:
    def __init__(self, schedule_item):
        self.schedule_item = schedule_item

class Movie:
    def __init__(self, title, schedule):
        self.title = title
        self.schedule = schedule

def main():
    for cinema in CINEMA_PATHS:
        parse_cinema(BASE_URL + cinema)

def parse_cinema(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    print("Parsing: ", url)
    plan = extract_plan(soup)
    only_ov_plan = filter_only_ov(plan)
    movies = print_date_and_time(only_ov_plan)
    # print(len(movies))


def extract_plan(cinema_template):
    movie_posters = cinema_template.find_all('img', attrs={'alt': 'movie poster'})
    plan = list()
    for movie_poster in movie_posters:
        movie_element = movie_poster.parent.parent
        plan.append(movie_element)
    return plan

def get_title(movie_element):
    return movie_element.select_one('ul li div').text

def is_ov(title):
    if "OmU" in title or "OV" in title:
        return True
    else:
        return False

def filter_only_ov(schedule):
    return [movie_element for movie_element in schedule if is_ov(get_title(movie_element))]

def print_date_and_time(plan):
    movies = list()
    for movie_element in plan:
        title = get_title(movie_element)
        print(title)
        times = movie_element.select('ul li')
        schedule_items = list()
        for time in times:
            date = time.select_one('li div')
            print("date: ", split_and_join(date.text))
            times_of_play = time.select('li div a')
            times_for_date = list()
            for play in times_of_play:
                time_of_play = play.text.strip()
                times_for_date.append(time_of_play)
                print("time: ", time_of_play)
            schedule_item = ScheduleItem(date, times_for_date)
            schedule_items.append(schedule_item)
        schedule = Schedule(schedule_items)
        movie = Movie(title, schedule)
        movies.append(movie)
    return movies
    

def split_and_join(input):
    return " ".join(input.split())

main()