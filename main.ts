/**
 * main.ts — entrypoint for the make.fun news-image-20261124 bounty.
 *
 * Copies the finished front page (entry.png, sitting next to this file)
 * into the make.fun output directory so the bounty harness can pick it
 * up. Node 22, standard library only — nothing to install.
 *
 *   MAKEFUN_OUTPUT_DIR=/some/dir node main.ts
 *
 * When MAKEFUN_OUTPUT_DIR is unset the copy lands in /output. The
 * destination folder is created when it does not exist yet.
 */

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = dirname(fileURLToPath(import.meta.url));
const sourceImage = join(scriptDir, "entry.png");

const outDir = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? "/output");
const targetImage = join(outDir, "entry.png");

const pixels = readFileSync(sourceImage);
mkdirSync(outDir, { recursive: true });
writeFileSync(targetImage, pixels);
console.log(`entry.png (${pixels.length} bytes) -> ${targetImage}`);
