export default class WebLoader {
	public static async load(url: string): Promise<string> {
		return await fetch(url).then((res) => res.text());
	}
}
