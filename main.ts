import { Cinema } from './models/cinema.ts';
import CinemaParser from './utils/cinema_parser.ts';
import FileWriter from './utils/file_writer.ts';
import { HtmlParser } from './utils/html_parser.ts';
import MarkdownBuilder from './utils/markdown_builder.ts';
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

  Promise.all(cinemaPromises).then(
    (cinemas: Cinema[]) => {
      const markdown: string = MarkdownBuilder.cinemasMarkdown(cinemas);
      FileWriter.writeToFile(GLOBALS.markdownFilePath, markdown);
    },
  );
}

// Learn more at https://deno.land/manual/examples/module_metadata#concepts
if (import.meta.main) {
  main();
}
