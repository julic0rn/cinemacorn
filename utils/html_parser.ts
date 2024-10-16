import { DOMParser, HTMLDocument } from 'jsr:@b-fuze/deno-dom';

export class HtmlParser {
    static getDocument(pageContents: string): HTMLDocument {
        return new DOMParser().parseFromString(
            pageContents,
            'text/html',
        );
    }
}
