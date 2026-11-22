// news-image-20261121: copy the rendered front page to /output/entry.png.
// The image is drawn by build-image.py (PIL, deterministic); this entrypoint
// only verifies it and copies it, so both grader runs write identical bytes.
// Size cap: PNG, at most 1 MiB and 1024x1024 px (the render is 1024x1024).
import { createHash } from "node:crypto";
import { copyFileSync, readFileSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const dst = join(outDir, "entry.png");

const bytes = readFileSync(src);
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!bytes.subarray(0, 8).equals(PNG_MAGIC)) {
  throw new Error("entry.png is not a PNG file");
}
if (bytes.length > 1048576) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB cap`);
}
mkdirSync(outDir, { recursive: true });
copyFileSync(src, dst);
const copied = statSync(dst).size;
const sha = createHash("sha256").update(bytes).digest("hex");
console.log(`entry.png: ${copied} bytes, sha256 ${sha}`);
