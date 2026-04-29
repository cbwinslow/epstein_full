import { defineConfig, devices } from '@playwright/test';

/**
 * Playwright end‑to‑end test configuration.
 *
 * The `baseURL` can be overridden with the environment variable `E2E_BASE_URL`
 * to point at a remote staging or QA instance. By default it points at a local
 * development server (`http://localhost:8000`).
 */
export default defineConfig({
  testDir: './e2e',
  timeout: 30_000,
  expect: {
    // Default timeout for expect() assertions.
    timeout: 5000,
  },
  // Run tests in parallel across available CPU cores.
  fullyParallel: true,
  // Use the built‑in test runner.
  reporter: [
    ['list'],
    ['html', { open: 'never' }], // HTML report generated in `playwright-report`
  ],
  use: {
    // Base URL for all `page.goto` calls.
    baseURL: process.env.E2E_BASE_URL || 'http://localhost:8000',
    // Run browsers headless – suitable for CI and remote instances.
    headless: true,
    // Capture a trace on first retry – helpful for debugging failures.
    trace: 'on-first-retry',
    // Capture screenshots only on failure.
    screenshot: 'only-on-failure',
    // Browser/device presets – you can add more if needed.
    ...devices['Desktop Chrome'],
  },
});
