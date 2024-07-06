import { DOMParser, HTMLDocument } from '../deps.ts';

export class HtmlParser {
    static getDocument(pageContents: string): HTMLDocument {
        return new DOMParser().parseFromString(
            pageContents,
            'text/html',
        );
    }
}
