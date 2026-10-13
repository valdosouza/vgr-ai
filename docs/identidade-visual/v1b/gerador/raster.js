// Draws SVGs to PNGs of an exact size with Chromium (used by plataformas.py).
// Needs playwright: NODE_PATH="$(npm root -g)" node raster.js jobs.json
const fs = require('fs');
const { chromium } = require('playwright');

(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const executablePath = process.env.CHROMIUM_PATH || undefined;
  const browser = await chromium.launch(executablePath ? { executablePath } : {});
  const page = await browser.newPage({ deviceScaleFactor: 1 });
  for (const job of jobs) {
    await page.setViewportSize({ width: job.w, height: job.h });
    await page.setContent(
      `<html><body style="margin:0;background:transparent">` +
      `<img style="display:block;width:${job.w}px;height:${job.h}px" src="data:image/svg+xml;base64,${job.svg}">` +
      `</body></html>`);
    await page.waitForFunction(() => document.images[0].complete);
    await page.screenshot({ path: job.out, omitBackground: job.transparent, clip: { x: 0, y: 0, width: job.w, height: job.h } });
  }
  await browser.close();
})();
