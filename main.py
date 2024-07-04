from typing import List
from datetime import datetime
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

    datetimes: List[datetime]


@dataclasses.dataclass
class Movie:
    """Represents a movie and its schedule"""

    title: str
    schedule: List[ScheduleItem]


@dataclasses.dataclass
class Cinema:
    """Represents a cinema with its movie schedule"""

    url: str
    movies: List[Movie]


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
    plan = extract_plan(soup)
    only_ov_plan = filter_only_ov(plan)
    cinema = Cinema(url, map_to_movies(only_ov_plan))
    print(cinema.url)
    for movie in cinema.movies:
        print(movie.title)
        for item in movie.schedule:
            for date in item.datetimes:
                print(date)
            print()
    print()


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


def map_to_movies(plan) -> List[Movie]:
    """Maps the given plan template into a list of movies

    Args:
        plan (_type_): template of the plan

    Returns:
        List[Movie]: Mapped movie list
    """
    movies: List[Movie] = []
    for movie_element in plan:
        title = get_title(movie_element)
        times = movie_element.select("ul li")
        schedule_items: List[ScheduleItem] = []
        for time in times:
            date = time.select("li div div")[1]
            date_string = split_and_join(date.text) + str(datetime.today().year)
            times_of_play = time.select("li div a")
            date_times: List[datetime] = []
            for play in times_of_play:
                time_of_play = play.text.strip()
                date_times.append(parse_date_from_str(date_string + " " + time_of_play))
            schedule_item = ScheduleItem(date_times)
            schedule_items.append(schedule_item)
        movie = Movie(title, schedule_items)
        movies.append(movie)
    return movies


def parse_date_from_str(datetime_str: str) -> datetime:
    """Parses the horrible date from the movies into a datetime object

    Args:
        datetime_str (str): a date string like "08.07." or "07.07."

    Returns:
        datetime: a datetime object
    """
    return datetime.strptime(datetime_str, "%d.%m.%Y %H:%M")


def split_and_join(input) -> str:
    """splits a string with a lot of white space in it and joins them with a single whitespace

    Args:
        input (str): Input string

    Returns:
        str: _description_
    """
    return " ".join(input.split())


main()
