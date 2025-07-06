import { GLOBALS } from '../main.ts';
import { Cinema } from '../models/cinema.ts';
import CinemaParser from '../utils/cinema_parser.ts';
import { HtmlParser } from '../utils/html_parser.ts';
import WebLoader from '../utils/web_loader.ts';
import { expect } from 'jsr:@std/expect';
import { Element } from 'jsr:@b-fuze/deno-dom';

interface CinemaMovieTestData {
	cinema: Cinema;
	movieList: Element | null;
}

Deno.test({
	name: 'Check if DOM is unchanged',
	async fn() {
		const cinemaPromises = GLOBALS.subPaths.map(
			async (subPath: string) => {
				const url = GLOBALS.baseUrl + subPath;
				const rawDocument = await WebLoader.load(url);
				const document = HtmlParser.getDocument(rawDocument);
				return {
					cinema: CinemaParser.parseCinema(document, url),
					movieList: document.querySelector(
						'body > main > div > div > div > ul',
					),
				} satisfies CinemaMovieTestData;
			},
		);

		await Promise.all(cinemaPromises).then(
			(testData: CinemaMovieTestData[]) => {
				// Verify we receive always GLOBALS.subPaths.length cinemas
				expect(testData.length).toBe(GLOBALS.subPaths.length);

				testData.forEach((data) => {
					// Verify the movieList <ul> was found
					expect(data.movieList).not.toBe(null);

					// Verify at least one movie is in the list
					const movies = data.movieList!.children;
					expect(movies.length).toBeGreaterThan(0);

					for (let index = 0; index < movies.length; index++) {
						// Check if every movies schedule, title and poster url can be accessed
						const movie = movies.item(index);

						const schedule = movie.querySelector('ul')?.getElementsByTagName(
							'li',
						);
						expect(schedule).not.toBe(null);

						const title = movie.querySelector('div > div');
						expect(title).not.toBe(null);

						const posterUrl =
							movie.getElementsByTagName('img')[0]?.getAttribute('src') ?? '';
						expect(posterUrl).not.toBe(null);
					}
				});
			},
		);
	},
	sanitizeResources: false,
	sanitizeOps: false,
});
