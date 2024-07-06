export const GLOBALS = {
  markdownFilePath: 'schedule.md',
  baseUrl: 'https://kinotickets.express',
  subPaths: [
    '/ingolstadt-cinema1',
    '/ingolstadt-cinema2',
    '/ingolstadt_donau-flimmern',
  ],
};

export function main(): void {
  console.log(GLOBALS);
  
}

// Learn more at https://deno.land/manual/examples/module_metadata#concepts
if (import.meta.main) {
  main();
}
