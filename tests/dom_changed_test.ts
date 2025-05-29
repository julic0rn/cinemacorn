import { GLOBALS } from '../main.ts';
import { Cinema } from '../models/cinema.ts';
import CinemaParser from '../utils/cinema_parser.ts';
import { HtmlParser } from '../utils/html_parser.ts';
import WebLoader from '../utils/web_loader.ts';
import { expect } from 'jsr:@std/expect';

Deno.test({
	name: 'Check if DOM is unchanged',
	async fn() {
		const cinemaPromises = GLOBALS.subPaths.map(
			async (subPath: string) => {
				const url = GLOBALS.baseUrl + subPath;
				const rawDocument = await WebLoader.load(url);
				const document = HtmlParser.getDocument(rawDocument);
				return CinemaParser.parseCinema(document, url);
			},
		);

		await Promise.all(cinemaPromises).then(
			(cinemas: Cinema[]) => {
				expect(cinemas.length).toBe(2);
				cinemas.forEach((cinema) => {
					expect(cinema.movies.length).toBeGreaterThanOrEqual(1);
				});
			},
		);
	},
	sanitizeResources: false,
	sanitizeOps: false,
});
