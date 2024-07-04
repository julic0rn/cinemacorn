from typing import List
import dataclasses
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://kinotickets.express"
CINEMA_PATHS = [
    "/ingolstadt-cinema1",
    "/ingolstadt-cinema2",
    "/ingolstadt_donau-flimmern",
]


@dataclasses.dataclass
class ScheduleItem:
    """Represents a date and times when a movie is shown"""

    date: str
    times: List[str]


@dataclasses.dataclass
class Schedule:
    """Represents e.g. a week of dates and times when a movie is shown"""

    schedule_items: List[ScheduleItem]


@dataclasses.dataclass
class Movie:
    """Represents a movie and its schedule"""

    title: str
    schedule: Schedule


def main():
    """main lol"""
    for cinema in CINEMA_PATHS:
        parse_cinema(BASE_URL + cinema)


def parse_cinema(url: str):
    """For given url of a cinema get all movies and its schedules

    Args:
        url (str): The url of the cinema to parse
    """
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    print("Parsing: ", url)
    plan = extract_plan(soup)
    only_ov_plan = filter_only_ov(plan)
    movies = print_date_and_time(only_ov_plan)
    print("Parses movies count: ", len(movies))


def extract_plan(cinema_template):
    """Extracts the overall plan with all movies and its schedule as a template
    from the root template of the cinema

    Args:
        cinema_template (BeautifulSoup): template of the cinema site

    Returns:
        BeautifulSoup: template of only the plan
    """
    movie_posters = cinema_template.find_all("img", attrs={"alt": "movie poster"})
    plan = []
    for movie_poster in movie_posters:
        movie_element = movie_poster.parent.parent
        plan.append(movie_element)
    return plan


def get_title(movie_element) -> str:
    """Extracts the movies title

    Args:
        movie_element (_type_): _description_

    Returns:
        str: _description_
    """
    return movie_element.select_one("ul li div").text


def is_ov(title) -> bool:
    """Returns whether the title is OV or OmU

    Args:
        title (str): title

    Returns:
        boolean: is OV or OmU
    """
    if "OmU" in title or "OV" in title:
        return True
    return False


def filter_only_ov(schedule):
    """Filters given schedule to return only movies in OV

    Args:
        schedule (_type_): template of the schedule

    Returns:
        _type_: template of the filtered schedule with only OV movies
    """
    return [
        movie_element for movie_element in schedule if is_ov(get_title(movie_element))
    ]


def print_date_and_time(plan) -> List[Movie]:
    """Maps the given plan template into a list of movies

    Args:
        plan (_type_): template of the plan

    Returns:
        List[Movie]: Mapped movie list
    """
    movies: List[Movie] = []
    for movie_element in plan:
        title = get_title(movie_element)
        print(title)
        times = movie_element.select("ul li")
        schedule_items: List[ScheduleItem] = []
        for time in times:
            date = time.select_one("li div")
            print("date: ", split_and_join(date.text))
            times_of_play = time.select("li div a")
            times_for_date: List[str] = []
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
    """splits a string with a lot of white space in it and joins them with a single whitespace

    Args:
        input (str): Input string

    Returns:
        str: _description_
    """
    return " ".join(input.split())


main()
