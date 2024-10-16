import { Element, HTMLDocument } from 'jsr:@b-fuze/deno-dom';
import { Cinema } from '../models/cinema.ts';
import { Movie } from '../models/movie.ts';
import { ScheduleItem } from '../models/schedule_item.ts';

export default class CinemaParser {
	private static getCinemaName(document: HTMLDocument): string {
		const name = document.querySelector(
			'body > header > div.md\\:mx-auto.md\\:container.lg\\:max-w-screen-xl > div.text-cinema-text.fixed.top-0.left-0.right-0.bg-cinema.z-50 > div > div > div.flex-none.hidden.sm\\:flex.mr-auto.min-w-0 > div',
		);
		return this.returnTextOrError(name, 'cinemaName');
	}

	private static getMovieList(document: HTMLDocument): Element[] {
		const moviePoster = document.querySelector(
			'body > main > div > div > div > ul > li:nth-child(1) > div.sm\\:p-4.sm\\:order-first.sm\\:row-span-4 > img',
		);
		const movieListElement = moviePoster?.parentElement?.parentElement
			?.parentElement;

		const movieListCollection = movieListElement?.children;
		const movieList: Element[] = [];
		if (!movieListCollection) {
			return [];
		}
		for (let index = 0; index < movieListCollection.length; index++) {
			const element = movieListCollection?.item(index);
			movieList.push(this.returnOrError(element, 'movieListElement'));
		}

		return this.returnOrError(movieList, 'movieList');
	}
	private static getSchedule(movieListElement: Element): Element[] {
		const scheduleElement = movieListElement.querySelector('ul');
		const schedule = scheduleElement?.getElementsByTagName('li');
		return this.returnOrError(schedule, 'schedule');
	}

	private static extractMovieTitle(element: Element): string {
		const titleElement = element.getElementsByTagName('div')[0];
		return this.returnTextOrError(titleElement, 'titleElement');
	}

	public static parseCinema(document: HTMLDocument, url: string): Cinema {
		const cinemaName = this.getCinemaName(document);
		const movies = this.parseMovies(document);

		return {
			url: url,
			name: cinemaName,
			movies: movies,
		} as Cinema;
	}

	private static isOv(title: string): boolean {
		return title.includes('OmU') || title.includes('OV');
	}

	private static parseMovies(document: HTMLDocument): Movie[] {
		const movieList = this.getMovieList(document);
		return movieList.map((movieListElement: Element) => {
			const movieTitle = this.extractMovieTitle(movieListElement);
			const schedule = this.parseSchedule(
				this.getSchedule(movieListElement),
			);

			return {
				title: movieTitle,
				schedule: schedule,
			} as Movie;
		}).filter(
			(movie: Movie) => this.isOv(movie.title),
		);
	}

	private static parseSchedule(scheduleElements: Element[]): ScheduleItem[] {
		const result: ScheduleItem[] = [];
		scheduleElements.forEach(
			(element: Element) => {
				const dateString = this.extractDate(element) +
					new Date().getFullYear();
				const [day, month, year] = dateString.split('.').map((e) => Number(e));

				const timeElements = this.getTimes(element);

				timeElements.forEach(
					(timeElement: Element) => {
						const [hour, minutes] = this.returnTextOrError(
							timeElement,
							'timeElement',
						).split(':').map((e) => Number(e));
						const subPath = timeElement.getAttribute('href') ?? '';

						const date = new Date(
							year!,
							month! - 1,
							day,
							hour,
							minutes,
						);
						const scheduleItem: ScheduleItem = {
							datetime: date,
							urlPath: subPath,
						};
						result.push(scheduleItem);
					},
				);
			},
		);
		return result;
	}

	private static getTimes(scheduleElement: Element): Element[] {
		const timeElements = scheduleElement?.getElementsByTagName('a');
		return this.returnOrError(timeElements, 'timeElements');
	}

	private static extractDate(scheduleElement: Element): string {
		const dateHeaderElement = scheduleElement.getElementsByTagName('div')[0];
		const dateElement = dateHeaderElement?.getElementsByTagName('div')[1];
		return this.returnTextOrError(dateElement, 'dateElement');
	}

	/**
	 * Returns the given element if defined.
	 * Otherwise throws an error.
	 * @param element The DOM element to be checked
	 * @param source Some context about the element
	 * @returns The element if defined
	 */
	private static returnOrError<T>(
		element: T,
		source: string,
	): NonNullable<T> {
		if (element) {
			return element;
		} else {
			throw Error(`Could not return element ${source}`);
		}
	}

	/**
	 * Returns the text content of given element if defined.
	 * Otherwise throws an error.
	 * @param element The DOM element to be checked
	 * @param source Some context about the element
	 * @returns The text content of given element if defined
	 */
	private static returnTextOrError(
		element: Element | undefined | null,
		source: string,
	): string {
		if (element) {
			return element.textContent.trim();
		} else {
			throw Error(`Could not return element ${source}`);
		}
	}
}
