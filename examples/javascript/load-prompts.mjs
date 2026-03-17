import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..", "..");
const catalogPath = path.join(repoRoot, "data", "catalog.json");

const catalog = JSON.parse(fs.readFileSync(catalogPath, "utf8"));
const curatedImagePrompts = catalog.entries.filter(
  (entry) => entry.category === "image" && entry.status !== "seed"
);

for (const entry of curatedImagePrompts) {
  console.log(`${entry.id}: ${entry.title}`);
}
