#!/usr/bin/env node

import fs from "node:fs/promises";
import { getDocument } from "pdfjs-dist/legacy/build/pdf.mjs";

const [, , inputPath, outputPath] = process.argv;
if (!inputPath || !outputPath) {
  console.error("Usage: node scripts/extract_pdf_markdown.mjs INPUT.pdf OUTPUT.md");
  process.exit(2);
}

function pageText(items) {
  const lines = new Map();
  for (const item of items) {
    if (!("str" in item) || !item.str.trim()) continue;
    const y = Math.round(item.transform[5]);
    const line = lines.get(y) ?? [];
    line.push({
      x: item.transform[4],
      width: item.width,
      height: Math.abs(item.transform[3]),
      text: item.str.trim(),
    });
    lines.set(y, line);
  }

  return [...lines.entries()]
    .sort(([a], [b]) => b - a)
    .map(([, line]) =>
      line.sort((a, b) => a.x - b.x).reduce((text, item, index, sorted) => {
        if (index === 0) return item.text;
        const previous = sorted[index - 1];
        const gap = item.x - (previous.x + previous.width);
        const separator = gap > Math.max(1.5, previous.height * 0.15) ? " " : "";
        return `${text}${separator}${item.text}`;
      }, ""),
    )
    .filter(Boolean)
    .join("\n");
}

const data = new Uint8Array(await fs.readFile(inputPath));
const document = await getDocument({ data, useSystemFonts: true }).promise;
const pages = [];

for (let pageNumber = 1; pageNumber <= document.numPages; pageNumber += 1) {
  const page = await document.getPage(pageNumber);
  const content = await page.getTextContent();
  pages.push(`<!-- page: ${pageNumber} -->\n\n${pageText(content.items)}`);
}

await fs.writeFile(outputPath, `${pages.join("\n\n---\n\n")}\n`, "utf8");
