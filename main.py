from typing import List
from datetime import datetime, UTC
import dataclasses
import requests
from bs4 import BeautifulSoup
from mdutils import MdUtils

MARKDON_FILE_PATH = "schedule.md"

BASE_URL = "https://kinotickets.express"
CINEMA_PATHS = [
    "/ingolstadt-cinema1",
    "/ingolstadt-cinema2",
    "/ingolstadt_donau-flimmern",
]


@dataclasses.dataclass
class ScheduleItem:
    """Represents a date and times when a movie is shown"""

    datetime: datetime
    url_path: str


@dataclasses.dataclass
class Movie:
    """Represents a movie and its schedule"""

    title: str
    schedule: List[ScheduleItem]


@dataclasses.dataclass
class Cinema:
    """Represents a cinema with its movie schedule"""

    url: str
    name: str
    movies: List[Movie]


def main():
    """main lol"""
    cinemas: List[Cinema] = []
    for cinema in CINEMA_PATHS:
        cinemas.append(parse_cinema(BASE_URL + cinema))
    create_markdown(cinemas=cinemas)


def create_markdown(cinemas: List[Cinema]):
    """Creates a markdown file to show the cinemas and its schedules

    Args:
        cinemas (List[Cinema]): _description_
    """

    md_file = MdUtils(
        file_name=MARKDON_FILE_PATH, title="Cinemacorn - " + str(datetime.now(UTC))
    )

    for cinema in cinemas:
        print(cinema.url)
        md_file.new_header(1, md_file.new_inline_link(link=cinema.url, text=cinema.name))

        for movie in cinema.movies:
            print(movie.title)
            md_file.new_header(2, movie.title)
            for item in movie.schedule:
                print(item.datetime)
                formatted_date = item.datetime.strftime("%A") + " " + str(item.datetime)
                md_file.new_line(
                    md_file.new_inline_link(
                        link=BASE_URL + item.url_path, text=formatted_date
                    )
                )
                print()
                md_file.new_line()
        print()
    md_file.create_md_file()


def parse_cinema(url: str) -> Cinema:
    """For given url of a cinema get all movies and its schedules

    Args:
        url (str): The url of the cinema to parse
    """
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    plan = extract_plan(soup)
    only_ov_plan = filter_only_ov(plan)
    cinema_name = extract_cinema_name(soup)
    return Cinema(url, cinema_name, map_to_movies(only_ov_plan))

def extract_cinema_name(cinema_template) -> str:
    """Extracts the name of the cinema

    Args:
        cinema_template (_type_): template

    Returns:
        str: name of the cinema
    """
    return cinema_template.find_all("div", attrs={"class": "truncate"})[0].text


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
        str: title
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
            for play in times_of_play:
                time_of_play = play.text.strip()
                href = play['href']
                schedule_item = ScheduleItem(
                    datetime=parse_date_from_str(date_string + " " + time_of_play),
                    url_path=href
                )
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
