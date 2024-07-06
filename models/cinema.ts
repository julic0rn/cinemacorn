import { Movie } from "./movie.ts";

export interface Cinema {
    url: string;
    name: string;
    movies: Movie[];
}