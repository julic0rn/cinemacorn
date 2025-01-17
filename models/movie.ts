import { ScheduleItem } from './schedule_item.ts';

export interface Movie {
	title: string;
	schedule: ScheduleItem[];
	posterUrl: string;
}
