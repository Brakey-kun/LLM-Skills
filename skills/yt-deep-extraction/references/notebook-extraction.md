# Companion Notebook Extraction (Browser-Only Method)

When a video references a Jupyter notebook on GitHub, extract its contents via browser even when terminal is broken.

## Step 1: Find the Raw JSON URL

GitHub notebooks are JSON files. The raw URL pattern is:

```
https://raw.githubusercontent.com/{USER}/{REPO}/{BRANCH}/{PATH}/{NOTEBOOK}.ipynb
```

Look in the video description for GitHub links. Example from the Quant Guild video:

```
https://github.com/romanmichaelpaolucci/Quant-Guild-Library/blob/main/.../is_trading_luck_or_skill.ipynb
```

Convert to raw:
```
https://raw.githubusercontent.com/romanmichaelpaolucci/Quant-Guild-Library/main/.../is_trading_luck_or_skill.ipynb
```

**Pattern**: Replace `github.com` with `raw.githubusercontent.com`, remove `/blob/`.

## Step 2: Load in Browser & Parse

```javascript
browser_navigate(raw_url);

// Parse the full notebook JSON
var nb = JSON.parse(document.body.textContent);

// Get cell count
nb.cells.length;

// Get all cell types and first 50 chars of source
nb.cells.map(function(c, i) {
  return {index: i, type: c.cell_type, source_preview: c.source.join('').slice(0,50)};
});
```

## Step 3: Extract Output Cells (text)

```javascript
// Get text output from a specific cell
var cells = JSON.parse(document.body.textContent).cells;
cells[15].outputs.map(function(o) {
  if (o.name === 'stdout' && o.text) {
    return o.text.join ? o.text.join('') : String(o.text);
  }
}).join('\n');
```

## Step 4: Handle Base64 PNG Outputs (plots)

Notebook cells with plots store them as base64 PNGs in `outputs[].data["image/png"]`. These are too large for browser_console character limits (~4-12K chars).

**Workaround**: Extract `text/plain` and `text/html` representations instead:

```javascript
var cell = JSON.parse(document.body.textContent).cells[24];
cell.outputs[0].data["text/plain"];  // text representation
cell.outputs[0].data["text/html"];   // HTML representation (may also be truncated)
```

Note the truncation and describe the plot based on:
- Matplotlib figure title
- Axis labels visible in text representation
- Code in the same cell (often reveals plot parameters)

## Step 5: Full JSON Structure

Notebook JSON structure for extraction:

```javascript
{
  "cells": [
    {
      "cell_type": "markdown" | "code",
      "source": ["line1\n", "line2\n", ...],
      "outputs": [  // only in code cells
        {
          "output_type": "stream",
          "name": "stdout",
          "text": ["output line 1\n", "output line 2\n", ...]
        },
        {
          "output_type": "display_data",
          "data": {
            "image/png": "base64...",      // TOO LARGE for console
            "text/plain": "text...",         // USE THIS
            "text/html": "<html>...</html>"  // USE THIS
          }
        }
      ],
      "execution_count": null | number
    }
  ],
  "metadata": {...},
  "nbformat": 4,
  "nbformat_minor": 5
}
```

## Limitations

1. **Base64 plots**: Cannot be extracted via browser_console due to size limits. Only `text/plain` and `text/html` representations available.
2. **Large notebooks**: >100 cells may exceed console output limits. Extract in ranges: `cells.slice(0, 20)`, `cells.slice(20, 40)`, etc.
3. **GitHub rate limits**: Raw GitHub URLs are rate-limited. Space requests 5+ seconds apart if extracting multiple notebooks.
