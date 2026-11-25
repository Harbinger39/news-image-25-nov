// Copies entry.png (the 25 November 2026 news-image entry) into the
// make.fun output directory. Node 22, standard library only.
//
// Usage:  MAKEFUN_OUTPUT_DIR=/output node main.ts
// If MAKEFUN_OUTPUT_DIR is not set, /output is used.
//
// Before copying, the image is checked: it must be a PNG, exactly
// 1024x1024 pixels, and at most 1 MiB. Anything else is rejected
// with a non-zero exit code and nothing is copied.

import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const MAX_BYTES = 1024 * 1024;
const EXPECTED_WIDTH = 1024;
const EXPECTED_HEIGHT = 1024;

// PNG signature, then the IHDR chunk: 4 bytes length, 4 bytes "IHDR",
// then width (4 bytes, big-endian) and height (4 bytes, big-endian).
const PNG_SIGNATURE = Buffer.from([
  0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
]);

function fail(message) {
  console.error(`main.ts: ${message}`);
  process.exit(1);
}

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");

let stats;
try {
  stats = statSync(source);
} catch {
  fail(`entry.png not found next to main.ts (${source})`);
}
if (stats.size > MAX_BYTES) {
  fail(`entry.png is ${stats.size} bytes, over the 1 MiB limit`);
}

const bytes = readFileSync(source);
if (bytes.length < 33 || !bytes.subarray(0, 8).equals(PNG_SIGNATURE)) {
  fail("entry.png is not a PNG file");
}
if (bytes.toString("ascii", 12, 16) !== "IHDR") {
  fail("entry.png has no IHDR chunk where one was expected");
}
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width !== EXPECTED_WIDTH || height !== EXPECTED_HEIGHT) {
  fail(
    `entry.png is ${width}x${height}, expected ` +
      `${EXPECTED_WIDTH}x${EXPECTED_HEIGHT}`,
  );
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
mkdirSync(outDir, { recursive: true });
const dest = join(outDir, "entry.png");
copyFileSync(source, dest);
console.log(`main.ts: copied entry.png (${stats.size} bytes) to ${dest}`);
