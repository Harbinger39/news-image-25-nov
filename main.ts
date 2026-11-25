// News image entry — 25 November 2026 (Node 22, standard library only).
// Copies the bundled entry.png to $MAKEFUN_OUTPUT_DIR (default /output),
// after checking it is a 1024x1024 PNG of at most 1 MiB.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const src = new URL('./entry.png', import.meta.url);
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const buf = readFileSync(src);
if (buf.length > 1024 * 1024) {
  throw new Error(
    `entry.png is ${buf.length} bytes, over the 1 MiB gate limit — rebuild a smaller image`,
  );
}
if (buf.subarray(0, 8).toString('hex') !== '89504e470d0a1a0a') {
  throw new Error('entry.png failed the PNG signature check');
}
const width = buf.readUInt32BE(16);
const height = buf.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  throw new Error(
    `entry.png is ${width}x${height}, but the gate requires exactly 1024x1024`,
  );
}
mkdirSync(outDir, { recursive: true });
copyFileSync(src, join(outDir, 'entry.png'));
// The gate sees exactly the bytes copied, so report what was delivered.
console.log(`copied entry.png (${buf.length} bytes, 1024x1024) to ${outDir}`);
