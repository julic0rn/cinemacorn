export default class FileWriter {
	public static async writeToFile(
		fileName: string,
		textInput: string,
	): Promise<void> {
		const file = await Deno.create(fileName);

		const writer = file.writable.getWriter();
		await writer.write(new TextEncoder().encode(textInput));
		await writer.close();
	}
}
