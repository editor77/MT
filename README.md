# LXX Morphology Downloader

This repository contains a small utility for downloading the LXX Morphology corpus from the UPenn gopher mirror.

## Usage

```bash
python scripts/download_lxxmorph.py --output-dir lxxmorph
```

By default, it pulls from:

```
https://ccat.sas.upenn.edu/gopher/text/religion/biblical/lxxmorph/
```

The downloader defaults to fetching only `*.mlxx` files so the local corpus stays limited to the MLXX data.
You can override the base URL with `--base-url` or adjust the filename filter with `--include` if the mirror
changes or you need additional file types.

## Chat question template

Use the template below when you want an analysis run based on the local `*.mlxx` files and the
`MT-LXX_Parallel_Manual (1).pdf` instructions:

```
Please analyze <BOOK CHAPTER:VERSE> using the local .mlxx files. Follow the MT-LXX_Parallel_Manual (1).pdf
step-by-step and return rows in this format:

Reference,Hebrew (MT),Greek (LXX),CATSS Notation & Analysis
```
