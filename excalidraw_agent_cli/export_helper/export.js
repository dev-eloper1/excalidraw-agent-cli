#!/usr/bin/env node
/**
 * Excalidraw CLI Export Helper
 *
 * Uses Puppeteer (headless Chrome) + roughjs to render .excalidraw files
 * to SVG and PNG with the authentic hand-drawn Excalidraw aesthetic.
 *
 * Usage:
 *   node export.js '{"format":"svg","input":"file.excalidraw","output":"out.svg"}'
 */

'use strict';

const fs = require('fs');
const path = require('path');

// ── Parse arguments ───────────────────────────────────────────────────────────

const args = process.argv.slice(2);
if (args.length === 0) {
  console.error('Usage: node export.js \'{"format":"svg","input":"...","output":"...",...}\'');
  process.exit(1);
}

let opts;
try {
  opts = JSON.parse(args[0]);
} catch (e) {
  console.error(`Failed to parse options JSON: ${e.message}`);
  process.exit(1);
}

const { format, input, output, darkMode = false, scale = 1, padding = 10, embedScene = true } = opts;

if (!format || !input || !output) {
  console.error('Options must include: format, input, output');
  process.exit(1);
}

if (!['svg', 'png'].includes(format)) {
  console.error(`Unsupported format: ${format}. Use 'svg' or 'png'.`);
  process.exit(1);
}

// ── Read input ────────────────────────────────────────────────────────────────

let excalidrawData;
try {
  const raw = fs.readFileSync(input, 'utf8');
  excalidrawData = JSON.parse(raw);
} catch (e) {
  console.error(`Failed to read input file: ${e.message}`);
  process.exit(1);
}

// ── Read roughjs bundle to inline in page ─────────────────────────────────────

// Use the UMD build (rough.js) which exposes window.rough in browser contexts
const roughjsPath = path.join(__dirname, 'node_modules', 'roughjs', 'bundled', 'rough.js');
let roughjsBundle;
try {
  roughjsBundle = fs.readFileSync(roughjsPath, 'utf8');
} catch (e) {
  console.error('roughjs not installed. Run: cd export_helper && npm install');
  process.exit(1);
}

// ── Export via Puppeteer ──────────────────────────────────────────────────────

async function main() {
  let puppeteer;
  try {
    puppeteer = require('puppeteer');
  } catch (e) {
    console.error(
      'Puppeteer not installed.\n' +
      'Run: cd export_helper && npm install'
    );
    process.exit(1);
  }

  const browser = await puppeteer.launch({
    headless: true,
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--disable-web-security',
      '--single-process',
    ],
  });

  try {
    const page = await browser.newPage();
    const html = buildHtmlPage(excalidrawData, roughjsBundle, { darkMode, scale, padding, embedScene, format });

    await page.setContent(html, { waitUntil: 'networkidle0', timeout: 30000 });

    await page.waitForFunction(
      () => window.__exportReady === true || window.__exportError !== undefined,
      { timeout: 30000 }
    );

    const exportError = await page.evaluate(() => window.__exportError);
    if (exportError) {
      throw new Error(`Excalidraw export error: ${exportError}`);
    }

    const svgContent = await page.evaluate(() => window.__exportResult);
    if (!svgContent) {
      throw new Error('SVG export returned empty content');
    }

    if (format === 'svg') {
      fs.writeFileSync(output, svgContent, 'utf8');
    } else if (format === 'png') {
      const os = require('os');
      const tmpSvg = path.join(os.tmpdir(), `cae_svg_${Date.now()}.svg`);
      fs.writeFileSync(tmpSvg, svgContent, 'utf8');

      let sharp;
      try {
        sharp = require('sharp');
      } catch (e) {
        fs.unlinkSync(tmpSvg);
        throw new Error('sharp not installed. Run: cd export_helper && npm install');
      }

      try {
        const scl = opts.scale || 1;
        const wMatch = svgContent.match(/\bwidth="(\d+(?:\.\d+)?)"/);
        const hMatch = svgContent.match(/\bheight="(\d+(?:\.\d+)?)"/);
        const svgW = wMatch ? Math.round(parseFloat(wMatch[1]) * scl) : null;
        const svgH = hMatch ? Math.round(parseFloat(hMatch[1]) * scl) : null;

        let pipeline = sharp(tmpSvg);
        if (svgW && svgH) {
          pipeline = pipeline.resize(svgW, svgH, { fit: 'contain' });
        }
        const pngBuf = await pipeline.png().toBuffer();
        fs.writeFileSync(output, pngBuf);
      } finally {
        try { fs.unlinkSync(tmpSvg); } catch(e) {}
      }
    }

    const fileSize = fs.statSync(output).size;
    const result = {
      success: true,
      output: output,
      format: format,
      file_size: fileSize,
      method: 'excalidraw-roughjs',
    };
    console.log(JSON.stringify(result));

  } finally {
    await browser.close();
  }
}

// ── HTML page builder ─────────────────────────────────────────────────────────

function buildHtmlPage(data, roughjsBundle, { darkMode, scale, padding, embedScene, format }) {
  const dataJson = JSON.stringify(data);
  const theme = darkMode ? 'dark' : 'light';
  const bgColor = darkMode ? '#121212' : (data.appState && data.appState.viewBackgroundColor || '#ffffff');

  return `<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>body { margin: 0; padding: 0; }</style>
</head>
<body>
  <script>
    window.__exportReady = false;
    window.__exportError = undefined;
    window.__exportResult = undefined;
  </script>

  <!-- roughjs for hand-drawn rendering -->
  <script>${roughjsBundle}</script>

  <script>
  (function() {
    try {
      const data = ${dataJson};
      const elements = (data.elements || []).filter(el => !el.isDeleted);
      const appState = data.appState || {};

      // Build element lookup map for arrow routing and text binding
      const elementMap = {};
      for (const el of elements) elementMap[el.id] = el;
      window.__allElements = elements; // needed by findBoundText

      const svg = buildRoughSvg(elements, elementMap, appState, data, {
        darkMode: ${JSON.stringify(darkMode)},
        padding: ${JSON.stringify(padding)},
        embedScene: ${JSON.stringify(embedScene)},
      });
      window.__exportResult = svg;
      window.__exportReady = true;
    } catch(e) {
      window.__exportError = e.message + '\\n' + e.stack;
    }
  })();

  // ── Rough SVG builder ─────────────────────────────────────────────────────

  function buildRoughSvg(elements, elementMap, appState, sceneData, opts) {
    const { darkMode, padding, embedScene } = opts;
    const bg = darkMode ? '#121212' : (appState.viewBackgroundColor || '#ffffff');

    const bbox = getBoundingBox(elements);
    const vx = (bbox ? bbox.x : 0) - padding;
    const vy = (bbox ? bbox.y : 0) - padding;
    const vw = (bbox ? bbox.width : 400) + padding * 2;
    const vh = (bbox ? bbox.height : 300) + padding * 2;

    // Create a real SVG element so roughjs can draw into it
    const svgEl = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svgEl.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    svgEl.setAttribute('xmlns:xlink', 'http://www.w3.org/1999/xlink');
    svgEl.setAttribute('version', '1.1');
    svgEl.setAttribute('viewBox', vx + ' ' + vy + ' ' + vw + ' ' + vh);
    svgEl.setAttribute('width', String(vw));
    svgEl.setAttribute('height', String(vh));
    svgEl.setAttribute('data-theme', darkMode ? 'dark' : 'light');
    document.body.appendChild(svgEl);

    // Font styles
    const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
    const style = document.createElementNS('http://www.w3.org/2000/svg', 'style');
    style.textContent = '@font-face { font-family: Virgil; } text { font-family: Virgil, "Comic Sans MS", cursive, sans-serif; }';
    defs.appendChild(style);
    svgEl.appendChild(defs);

    // Background rect
    const bgRect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    bgRect.setAttribute('x', String(vx));
    bgRect.setAttribute('y', String(vy));
    bgRect.setAttribute('width', String(vw));
    bgRect.setAttribute('height', String(vh));
    bgRect.setAttribute('fill', bg);
    svgEl.appendChild(bgRect);

    // Create roughjs instance
    const rc = rough.svg(svgEl);

    // Render in order: non-arrows first, then arrows on top
    const nonArrows = elements.filter(el => el.type !== 'arrow' && el.type !== 'line');
    const arrows = elements.filter(el => el.type === 'arrow' || el.type === 'line');

    for (const el of [...nonArrows, ...arrows]) {
      const node = renderElement(rc, svgEl, el, elementMap, darkMode);
      if (node) svgEl.appendChild(node);
    }

    // Embed scene metadata
    if (embedScene) {
      const meta = document.createElementNS('http://www.w3.org/2000/svg', 'metadata');
      meta.innerHTML = '<excalidraw:scene xmlns:excalidraw="https://excalidraw.com/svg" data="' +
        btoa(unescape(encodeURIComponent(JSON.stringify(sceneData)))) + '"/>';
      svgEl.appendChild(meta);
    }

    const serialized = new XMLSerializer().serializeToString(svgEl);
    svgEl.remove();
    return serialized;
  }

  // ── Per-element renderer ──────────────────────────────────────────────────

  function renderElement(rc, svgEl, el, elementMap, darkMode) {
    const stroke = el.strokeColor || '#1e1e1e';
    const fill = (!el.backgroundColor || el.backgroundColor === 'transparent') ? 'none' : el.backgroundColor;
    const sw = el.strokeWidth || 2;
    const roughness = el.roughness !== undefined ? el.roughness : 1;
    const opacity = (el.opacity || 100) / 100;

    const roughOpts = {
      stroke,
      strokeWidth: sw,
      roughness,
      fill: fill === 'none' ? undefined : fill,
      fillStyle: fill === 'none' ? 'solid' : (el.fillStyle || 'hachure'),
      seed: el.seed || 42,
    };

    // Add stroke dash
    const dashArray = el.strokeStyle === 'dashed' ? [8, 4] : el.strokeStyle === 'dotted' ? [2, 4] : undefined;

    let node;

    switch (el.type) {
      case 'rectangle': {
        const r = el.roundness ? Math.min(el.width, el.height) * 0.1 : 0;
        if (r > 0) {
          // Rough path for rounded rect
          node = rc.path(roundedRectPath(el.x, el.y, el.width, el.height, r), roughOpts);
        } else {
          node = rc.rectangle(el.x, el.y, el.width, el.height, roughOpts);
        }
        break;
      }

      case 'ellipse': {
        node = rc.ellipse(
          el.x + el.width / 2,
          el.y + el.height / 2,
          el.width,
          el.height,
          roughOpts
        );
        break;
      }

      case 'diamond': {
        const cx = el.x + el.width / 2;
        const cy = el.y + el.height / 2;
        const pts = [
          [cx, el.y],
          [el.x + el.width, cy],
          [cx, el.y + el.height],
          [el.x, cy],
        ];
        node = rc.polygon(pts, roughOpts);
        break;
      }

      case 'arrow':
      case 'line': {
        // Compute routed start/end points
        const { start, end } = resolveArrowEndpoints(el, elementMap);
        const isArrow = el.type === 'arrow';

        // For a simple 2-point line, route as straight line
        // For arrows that loop back (same source & target), add an offset loop
        const startBound = el.startBinding && elementMap[el.startBinding.elementId];
        const endBound = el.endBinding && elementMap[el.endBinding.elementId];
        const isSelfLoop = startBound && endBound && startBound.id === endBound.id;

        let arrowNode;
        if (isSelfLoop) {
          // Draw a loop arc
          const ex = startBound.x + startBound.width / 2;
          const ey = startBound.y;
          arrowNode = rc.path(
            \`M \${ex - 30} \${ey} C \${ex - 80} \${ey - 80} \${ex + 80} \${ey - 80} \${ex + 30} \${ey}\`,
            { ...roughOpts, fill: undefined, fillStyle: 'solid' }
          );
        } else {
          arrowNode = rc.line(start.x, start.y, end.x, end.y, {
            ...roughOpts,
            fill: undefined,
            fillStyle: 'solid',
          });
        }

        if (dashArray) {
          const paths = arrowNode.querySelectorAll('path');
          paths.forEach(p => p.setAttribute('stroke-dasharray', dashArray.join(',')));
        }
        if (opacity < 1) arrowNode.setAttribute('opacity', String(opacity));

        // Arrowhead marker
        if (isArrow && el.endArrowhead) {
          const markerId = 'ah-' + el.id.replace(/[^a-z0-9]/gi, '');
          const markerDef = createArrowheadMarker(svgEl, markerId, stroke, sw);
          svgEl.querySelector('defs').appendChild(markerDef);
          const paths = arrowNode.querySelectorAll('path');
          if (paths.length > 0) {
            paths[paths.length - 1].setAttribute('marker-end', \`url(#\${markerId})\`);
          }
        }

        node = arrowNode;
        break;
      }

      case 'frame': {
        const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
        rect.setAttribute('x', String(el.x));
        rect.setAttribute('y', String(el.y));
        rect.setAttribute('width', String(el.width));
        rect.setAttribute('height', String(el.height));
        rect.setAttribute('fill', 'none');
        rect.setAttribute('stroke', el.strokeColor || '#bbb');
        rect.setAttribute('stroke-width', '1');
        rect.setAttribute('stroke-dasharray', '6,3');
        const label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        label.setAttribute('x', String(el.x));
        label.setAttribute('y', String(el.y - 4));
        label.setAttribute('font-size', '12');
        label.setAttribute('fill', '#888');
        label.textContent = el.name || 'Frame';
        g.appendChild(rect);
        g.appendChild(label);
        node = g;
        break;
      }

      case 'text': {
        // Standalone text (not bound to a container — those are rendered with their parent)
        if (el.containerId) return null;
        node = createTextNode(el, opacity);
        break;
      }

      default:
        return null;
    }

    if (node) {
      if (opacity < 1 && el.type !== 'arrow' && el.type !== 'line') {
        node.setAttribute('opacity', String(opacity));
      }

      // Append bound text label after the shape
      if (['rectangle', 'ellipse', 'diamond'].includes(el.type)) {
        const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        g.appendChild(node);
        const textChild = findBoundText(el.id, window.__allElements || []);
        if (textChild) {
          const textNode = createTextNode(textChild, opacity);
          if (textNode) g.appendChild(textNode);
        }
        return g;
      }
    }

    return node;
  }

  // ── Arrow endpoint resolution ─────────────────────────────────────────────

  function resolveArrowEndpoints(arrow, elementMap) {
    const pts = arrow.points || [[0,0],[0,100]];
    const rawStart = { x: arrow.x + pts[0][0], y: arrow.y + pts[0][1] };
    const rawEnd   = { x: arrow.x + pts[pts.length-1][0], y: arrow.y + pts[pts.length-1][1] };

    const srcEl = arrow.startBinding && elementMap[arrow.startBinding.elementId];
    const dstEl = arrow.endBinding && elementMap[arrow.endBinding.elementId];

    // Get actual edge-intersection points
    const start = srcEl ? shapeEdgePoint(srcEl, rawEnd) : rawStart;
    const end   = dstEl ? shapeEdgePoint(dstEl, rawStart) : rawEnd;

    return { start, end };
  }

  // Find the point where the line from shape center to "other" exits the shape boundary
  function shapeEdgePoint(shape, other) {
    const cx = shape.x + shape.width / 2;
    const cy = shape.y + shape.height / 2;
    const dx = other.x - cx;
    const dy = other.y - cy;
    const gap = 5; // small gap so arrow doesn't overlap border

    if (shape.type === 'ellipse') {
      // Ellipse parametric intersection
      const rx = shape.width / 2 + gap;
      const ry = shape.height / 2 + gap;
      const len = Math.sqrt(dx * dx / (rx * rx) + dy * dy / (ry * ry));
      if (len === 0) return { x: cx, y: cy - ry };
      return { x: cx + dx / len / rx * rx, y: cy + dy / len / ry * ry };
    }

    if (shape.type === 'diamond') {
      // Diamond edges: top, right, bottom, left
      const hw = shape.width / 2;
      const hh = shape.height / 2;
      if (dx === 0 && dy === 0) return { x: cx, y: cy - hh };
      // parametric ray intersection with diamond edges
      const candidates = [];
      // top-right edge: from (cx, cy-hh) to (cx+hw, cy)
      const t1 = lineRayIntersect(cx, cy, dx, dy, cx, cy-hh, cx+hw, cy);
      if (t1 !== null && t1 > 0) candidates.push(t1);
      // bottom-right
      const t2 = lineRayIntersect(cx, cy, dx, dy, cx+hw, cy, cx, cy+hh);
      if (t2 !== null && t2 > 0) candidates.push(t2);
      // bottom-left
      const t3 = lineRayIntersect(cx, cy, dx, dy, cx, cy+hh, cx-hw, cy);
      if (t3 !== null && t3 > 0) candidates.push(t3);
      // top-left
      const t4 = lineRayIntersect(cx, cy, dx, dy, cx-hw, cy, cx, cy-hh);
      if (t4 !== null && t4 > 0) candidates.push(t4);
      const t = Math.min(...candidates);
      return { x: cx + dx * t + (dx > 0 ? gap : -gap), y: cy + dy * t + (dy > 0 ? gap : -gap) };
    }

    // Rectangle (default)
    const hw = shape.width / 2;
    const hh = shape.height / 2;
    if (dx === 0 && dy === 0) return { x: cx, y: cy - hh - gap };

    // Clamp to rectangle boundary along direction
    const tx = dx !== 0 ? hw / Math.abs(dx) : Infinity;
    const ty = dy !== 0 ? hh / Math.abs(dy) : Infinity;
    const t = Math.min(tx, ty);
    return {
      x: cx + dx * t + (dx > 0 ? gap : dx < 0 ? -gap : 0),
      y: cy + dy * t + (dy > 0 ? gap : dy < 0 ? -gap : 0),
    };
  }

  // Ray from (ox,oy) in direction (dx,dy) intersects segment (ax,ay)-(bx,by)
  // Returns t parameter or null
  function lineRayIntersect(ox, oy, dx, dy, ax, ay, bx, by) {
    const ex = bx - ax, ey = by - ay;
    const denom = dx * ey - dy * ex;
    if (Math.abs(denom) < 1e-10) return null;
    const t = ((ax - ox) * ey - (ay - oy) * ex) / denom;
    const s = ((ax - ox) * dy - (ay - oy) * dx) / denom;
    if (s < 0 || s > 1) return null;
    return t;
  }

  // ── Text node creator ─────────────────────────────────────────────────────

  function createTextNode(el, parentOpacity) {
    const lines = (el.text || '').split('\\n');
    const fs = el.fontSize || 16;
    const lh = (el.lineHeight || 1.25) * fs;
    const anchor = el.textAlign === 'center' ? 'middle' : el.textAlign === 'right' ? 'end' : 'start';
    const tx = el.textAlign === 'center' ? el.x + el.width / 2 : el.textAlign === 'right' ? el.x + el.width : el.x;
    const stroke = el.strokeColor || '#1e1e1e';
    const family = el.fontFamily === 2 ? 'Helvetica, Arial, sans-serif'
                 : el.fontFamily === 3 ? 'Cascadia Code, monospace'
                 : 'Virgil, "Comic Sans MS", cursive, sans-serif';

    const textEl = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    textEl.setAttribute('font-size', String(fs));
    textEl.setAttribute('font-family', family);
    textEl.setAttribute('text-anchor', anchor);
    textEl.setAttribute('fill', stroke);
    textEl.setAttribute('x', String(tx));

    // Vertical centering: start from top of element + offset to mid
    const totalH = lines.length * lh;
    const startY = el.y + (el.height - totalH) / 2 + fs * 0.8;

    lines.forEach((line, i) => {
      const tspan = document.createElementNS('http://www.w3.org/2000/svg', 'tspan');
      tspan.setAttribute('x', String(tx));
      tspan.setAttribute('dy', i === 0 ? String(startY - el.y) : String(lh));
      tspan.setAttribute('y', i === 0 ? String(startY) : '');
      tspan.textContent = line;
      textEl.appendChild(tspan);
    });

    if (parentOpacity !== undefined && parentOpacity < 1) {
      textEl.setAttribute('opacity', String(parentOpacity));
    }
    return textEl;
  }

  function findBoundText(containerId, elements) {
    return elements.find(el => el.containerId === containerId && el.type === 'text' && !el.isDeleted);
  }

  // ── Arrowhead marker ──────────────────────────────────────────────────────

  function createArrowheadMarker(svgEl, id, color, sw) {
    const marker = document.createElementNS('http://www.w3.org/2000/svg', 'marker');
    marker.setAttribute('id', id);
    marker.setAttribute('markerWidth', '10');
    marker.setAttribute('markerHeight', '7');
    marker.setAttribute('refX', '9');
    marker.setAttribute('refY', '3.5');
    marker.setAttribute('orient', 'auto');
    const poly = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
    poly.setAttribute('points', '0 0, 10 3.5, 0 7');
    poly.setAttribute('fill', color);
    marker.appendChild(poly);
    return marker;
  }

  // ── Bounding box ──────────────────────────────────────────────────────────

  function getBoundingBox(elements) {
    let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    for (const el of elements) {
      if (el.type === 'text' && el.containerId) continue; // skip bound text
      const x = el.x || 0, y = el.y || 0;
      if (el.points) {
        for (const p of el.points) {
          minX = Math.min(minX, x + p[0]); minY = Math.min(minY, y + p[1]);
          maxX = Math.max(maxX, x + p[0]); maxY = Math.max(maxY, y + p[1]);
        }
      } else {
        minX = Math.min(minX, x); minY = Math.min(minY, y);
        maxX = Math.max(maxX, x + (el.width || 0)); maxY = Math.max(maxY, y + (el.height || 0));
      }
    }
    if (!isFinite(minX)) return null;
    return { x: minX, y: minY, width: maxX - minX, height: maxY - minY };
  }

  // ── Rounded rect SVG path ─────────────────────────────────────────────────

  function roundedRectPath(x, y, w, h, r) {
    return \`M \${x+r} \${y} L \${x+w-r} \${y} Q \${x+w} \${y} \${x+w} \${y+r}
      L \${x+w} \${y+h-r} Q \${x+w} \${y+h} \${x+w-r} \${y+h}
      L \${x+r} \${y+h} Q \${x} \${y+h} \${x} \${y+h-r}
      L \${x} \${y+r} Q \${x} \${y} \${x+r} \${y} Z\`;
  }

  </script>
</body>
</html>`;
}

// ── Run ───────────────────────────────────────────────────────────────────────

main().catch(err => {
  console.error(err.message || err);
  process.exit(1);
});
