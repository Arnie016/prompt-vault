import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..", "..");
const catalogPath = path.join(repoRoot, "data", "subagent-query-catalog.json");

const catalog = JSON.parse(fs.readFileSync(catalogPath, "utf8"));
const matches = catalog.entries.filter(
  (entry) => entry.domain === "security" && entry.mode === "harden"
);

for (const entry of matches.slice(0, 5)) {
  console.log(`${entry.id}: ${entry.title}`);
}
