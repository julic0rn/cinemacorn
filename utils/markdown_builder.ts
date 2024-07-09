import { format } from '../deps.ts';
import { GLOBALS } from '../main.ts';
import { Cinema } from '../models/cinema.ts';
import { Movie } from '../models/movie.ts';
import { ScheduleItem } from '../models/schedule_item.ts';

export default class MarkdownBuilder {
    private static readonly DATE_TIME_FORMAT = 'yyyy-MM-dd HH:mm';

    public static heading(level: 1 | 2 | 3 | 4 | 5 | 6, text: string): string {
        const levelPrefix: string = '#'.repeat(level);
        return `${levelPrefix} ${text}`;
    }

    public static link(href: string, text: string): string {
        return `[${text}](${href})`;
    }

    public static paragraph(text: string): string {
        return `
        ${text}
        `;
    }

    public static cinemasMarkdown(cinemas: Cinema[]): string {
        const currentDateString = format(
            new Date(),
            this.DATE_TIME_FORMAT,
        );
        const header = this.heading(
            1,
            `${GLOBALS.projectName}: ${currentDateString}`,
        );

        const cinemasMarkdown: string = cinemas.map((cinema) =>
            this.convertCinemaToMarkdown(cinema)
        ).join('\n');

        return header.concat('\n', '\n', cinemasMarkdown);
    }

    private static convertCinemaToMarkdown(cinema: Cinema): string {
        const header = this.heading(2, this.link(cinema.url, cinema.name));

        const movieSchedule: string[] = cinema.movies.map(
            (movie: Movie) => {
                const movieHeader = this.heading(3, movie.title);
                const schedule = movie.schedule.map(
                    (scheduleItem: ScheduleItem) =>
                        '\n'.concat(this.link(
                            GLOBALS.baseUrl + scheduleItem.urlPath,
                            format(
                                scheduleItem.datetime,
                                this.DATE_TIME_FORMAT,
                            ),
                        )),
                );

                return movieHeader.concat('\n', ...schedule, '\n', '\n');
            },
        );

        return header.concat('\n', '\n', ...movieSchedule, '\n');
    }
}
