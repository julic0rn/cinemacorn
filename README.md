# CINEMACORN

## What is this?

I want to know when there are movies in OV in my hometown lol.

Find the nicely formatted list
[here](https://github.com/julic0rn/cinemacorn/releases)

## Requirements

- [Deno](https://docs.deno.com/runtime/manual/getting_started/installation/)

### Test project

The project currently contains a simple test to check if any movie is returned
for both cinemas listed. If nothing is returned this might indicate that the DOM
has changed again and the selection of HTML tags containing movies needs to be
adjusted.

You can run the tests by running

```sh
deno test --allow-net=kinotickets.express
```

### Run project

```sh
deno run --allow-read --allow-write --allow-net=kinotickets.express main.ts
```

### Build executable binary

```sh
deno compile --allow-read --allow-write --allow-net=kinotickets.express main.ts --output cinemacorn
```
