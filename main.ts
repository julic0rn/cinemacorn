import CinemaParser from './utils/cinema_parser.ts';
import { HtmlParser } from './utils/html_parser.ts';
import WebLoader from './utils/web_loader.ts';

export const GLOBALS = {
  markdownFilePath: 'schedule.md',
  baseUrl: 'https://kinotickets.express',
  subPaths: [
    '/ingolstadt-cinema1',
    '/ingolstadt-cinema2',
  ],
};

export function main(): void {
  const cinemaPromises = GLOBALS.subPaths.map(
    async (subPath: string) => {
      const url = GLOBALS.baseUrl + subPath;
      const rawDocument = await WebLoader.load(url);
      const document = HtmlParser.getDocument(rawDocument);
      return CinemaParser.parseCinema(document, url);
    },
  );
  cinemaPromises.forEach((promise) =>
    promise.then((cinema) => console.log(cinema))
  );
}

// Learn more at https://deno.land/manual/examples/module_metadata#concepts
if (import.meta.main) {
  main();
}
