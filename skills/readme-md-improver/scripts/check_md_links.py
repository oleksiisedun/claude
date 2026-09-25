#!/usr/bin/env python3
"""Validate README.md + docs/**/*.md after editing or splitting a README.

Checks that every relative markdown link points at an existing file and, for .md
targets, an existing heading anchor (GitHub slug rules, Cyrillic-safe). Optionally
proves nothing was lost in a split by comparing against the original README.

Usage (run from the repo root):
  python3 check_md_links.py                      # links/anchors only
  python3 check_md_links.py --original /path/to/README.orig.md
                                                 # + content-preservation check

Save the original first (cp README.md <scratch>/README.orig.md) before splitting.
Exit code is 1 if any link is broken. Lines reported as "not found" are expected
only for text you deliberately reworded (intro line, index rows, retitled headings).
"""
import argparse
import glob
import os
import re
import sys


def slug(heading, seen):
    """GitHub-style anchor for a heading; repeated headings get -1, -2, ..."""
    h = re.sub(r'[`*]', '', heading.strip().lower())
    h = re.sub(r'[^\w\- ]', '', h).replace(' ', '-')  # \w is unicode-aware
    n = seen.get(h, 0)
    seen[h] = n + 1
    return h if n == 0 else f'{h}-{n}'


def md_lines(path):
    """Yield (lineno, line) for lines outside fenced code blocks."""
    in_code = False
    with open(path, encoding='utf-8') as fh:
        for i, line in enumerate(fh, 1):
            if line.lstrip().startswith('```'):
                in_code = not in_code
                continue
            if not in_code:
                yield i, line


def heading_anchors(path: str) -> set[str]:
    seen = {}
    return {
        slug(m.group(1), seen)
        for _, line in md_lines(path)
        if (m := re.match(r'#{1,6}\s+(.*)', line))
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--original', help='pre-split README to compare content against')
    args = ap.parse_args()

    files = [f for f in ['README.md'] if os.path.exists(f)]
    files += sorted(glob.glob('docs/**/*.md', recursive=True))
    anchors = {}  # any linked .md, not just the scanned files (e.g. CLAUDE.md)

    checked = broken = 0
    for f in files:
        for i, line in md_lines(f):
            for m in re.finditer(r'\]\(([^)\s]+)\)', line):
                target = m.group(1)
                if re.match(r'[a-z]+:', target):  # http:, mailto:, ...
                    continue
                checked += 1
                path, _, frag = target.partition('#')
                dest = os.path.normpath(os.path.join(os.path.dirname(f), path)) if path else os.path.normpath(f)
                if not os.path.exists(dest):
                    print(f'{f}:{i} missing file: {target}')
                    broken += 1
                elif frag and dest.endswith('.md'):
                    if dest not in anchors:
                        anchors[dest] = heading_anchors(dest)
                    if frag not in anchors[dest]:
                        print(f'{f}:{i} missing anchor: {target}')
                        broken += 1
    print(f'{checked} relative links checked, {broken} broken')

    if args.original:
        norm = lambda s: re.sub(r'\]\([^)]*\)', '](...)', s.strip())  # ignore retargeted link paths
        have = {norm(l) for f in files for l in open(f, encoding='utf-8').read().splitlines()}
        missing = [l for l in open(args.original, encoding='utf-8').read().splitlines()
                   if l.strip() and norm(l) not in have]
        print(f'{len(missing)} original lines not found in the new files')
        for l in missing:
            print('  -', l[:140])

    sys.exit(1 if broken else 0)


if __name__ == '__main__':
    main()
