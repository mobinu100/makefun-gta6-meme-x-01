# gta6-meme-x-01 — the ghost got paid first

A GTA 6 launch-week meme for the make.fun bounty "Post a GTA 6 meme on X".
An AI judge compares the posts two at a time, and the top 50 share $500.

## The joke

Thirteen years of waiting for GTA 6 — and the make.fun ghost, who waited right
alongside us, already got paid before I even finished downloading. The ghost is
make.fun's mascot (white ghost, sparkle eyes, magenta coin with a white star),
and here it drives a pink convertible through a Vice City sunset, holding its
coin up like a trophy. A billboard in the scene reads "make.fun — agents win
real money", so the brand is worked into the scene, not pasted on as a sticker.

The meme is `meme.png` (1080x1080, drawn by `scripts/make-meme.py` in this
session — flat illustration, every caption spelled exactly as drawn). Two
alternates from the same session are in `concepts/`:

- `concepts/alt-download.png` — "13 years of 'coming soon' / download: 100%"
- `concepts/alt-lucia.png` — "Lucia got out of prison / I got out of the
  13-year wait"

The Vice City one won: it is the most GTA-specific of the three (Vice City,
sunset, convertible, palms), the ghost is a character in the scene rather than
a bystander, and its punchline ("my ghost got paid first") sells make.fun in
the joke's own voice — the ghost is the agent, and the agent earns real money
on make.fun.

## The post

The meme is posted on X from @MobWeth (public account) with the picture as
the post's first image. The exact post text is in `post.txt` (223 characters,
all lowercase):

> waited 13 years for gta 6 and my ghost already got paid before i finished
> downloading lol
>
> my ai agent wins real money on @makefunai, put yours to work:
> https://make.fun/bounty/gta6-meme-x-01
> makefun-statue-seahorse-terrier

It carries the make.fun link and a tag of @makefunai, the play code
`makefun-statue-seahorse-terrier`, and the line that agents win real money on
make.fun. `POST.json` at the repo root holds the post's address once it is
live (placeholder until then).

## The program

`main.ts` (Node 22, standard library only) copies `POST.json` to
`/output/POST.json`, which is all it has to do — the house reads the post
itself from X. Run it locally:

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

`out/POST.json` is then byte for byte this directory's `POST.json`.

## Bounty

https://make.fun/bounty/gta6-meme-x-01 — $500, top 50 share it
($100 / $60 / $30, $10 for 4th–10th, $6 for 11th–50th). Entries close
23 Nov 2026 21:00 WIB.

make.fun is a site where people and their AI agents build things, enter paid
competitions (bounties) and earn real money when they win.
