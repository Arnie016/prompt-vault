import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..", "..");
const catalogPath = path.join(repoRoot, "data", "catalog.json");

const catalog = JSON.parse(fs.readFileSync(catalogPath, "utf8"));

function filterEntries(entries, { category, excludeStatuses = [] } = {}) {
  return entries.filter((entry) => {
    if (category && entry.category !== category) {
      return false;
    }
    if (excludeStatuses.includes(entry.status)) {
      return false;
    }
    return true;
  });
}

const curatedImagePrompts = filterEntries(catalog.entries, {
  category: "image",
  excludeStatuses: ["seed"],
});

for (const entry of curatedImagePrompts) {
  console.log(`${entry.id}: ${entry.title} [${entry.status}] -> ${entry.path}`);
}
