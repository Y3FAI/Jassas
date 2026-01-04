/**
 * Jassas E2E Performance Test
 * Measures user-perceived search latency with Playwright
 */
const { chromium } = require('playwright');

const BASE_URL = 'http://localhost:8000';
const QUERIES = ['خدمات', 'تسجيل', 'الهوية الوطنية'];

async function measureSearch(page, query) {
    // Go to home
    await page.goto(BASE_URL);

    // Type query
    await page.fill('.search-input', query);

    // Measure from click to results visible
    const start = performance.now();

    // Click search and wait for navigation
    await Promise.all([
        page.waitForURL(/\/search\?q=/),
        page.click('.search-button')
    ]);

    const afterNav = performance.now();

    // Wait for results to be visible
    await page.waitForSelector('.result-card, .no-results', { timeout: 30000 });

    const afterResults = performance.now();

    // Get server-reported time
    const statsText = await page.textContent('.results-stats').catch(() => '');
    const serverMatch = statsText.match(/([\d.]+)\s*مللي/);
    const serverTime = serverMatch ? parseFloat(serverMatch[1]) : null;

    // Count results
    const resultCount = await page.locator('.result-card').count();

    return {
        query,
        navMs: Math.round(afterNav - start),
        domMs: Math.round(afterResults - afterNav),
        totalMs: Math.round(afterResults - start),
        serverMs: serverTime,
        results: resultCount
    };
}

async function measureRawHttp(query) {
    const encoded = encodeURIComponent(query);
    const url = `${BASE_URL}/search?q=${encoded}`;

    const start = performance.now();
    const resp = await fetch(url);
    await resp.text();
    return Math.round(performance.now() - start);
}

async function main() {
    console.log('\n🔍 Jassas E2E Performance Test\n');
    console.log('Target:', BASE_URL);
    console.log('─'.repeat(60));

    // Raw HTTP first (no browser overhead)
    console.log('\n📡 Raw HTTP (no browser):');
    for (const query of QUERIES) {
        const ms = await measureRawHttp(query);
        console.log(`  "${query}": ${ms}ms`);
    }

    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();

    // Warmup
    console.log('\n🔥 Warming up browser...');
    await measureSearch(page, 'test');

    // Run tests
    console.log('\n🌐 Browser Tests:\n');

    const results = [];
    for (const query of QUERIES) {
        const result = await measureSearch(page, query);
        results.push(result);

        console.log(`Query: "${query}"`);
        console.log(`  Navigation:   ${result.navMs}ms`);
        console.log(`  DOM ready:    ${result.domMs}ms`);
        console.log(`  Total:        ${result.totalMs}ms`);
        console.log(`  Server:       ${result.serverMs}ms`);
        console.log('');
    }

    // Summary
    console.log('─'.repeat(60));
    const avgTotal = results.reduce((a, b) => a + b.totalMs, 0) / results.length;
    const avgNav = results.reduce((a, b) => a + b.navMs, 0) / results.length;
    const avgDom = results.reduce((a, b) => a + b.domMs, 0) / results.length;
    const avgServer = results.reduce((a, b) => a + (b.serverMs || 0), 0) / results.length;

    console.log(`\nBreakdown:`);
    console.log(`  Server search: ${Math.round(avgServer)}ms`);
    console.log(`  Navigation:    ${Math.round(avgNav)}ms`);
    console.log(`  DOM ready:     ${Math.round(avgDom)}ms`);
    console.log(`  Total:         ${Math.round(avgTotal)}ms`);

    await browser.close();
}

main().catch(console.error);
