import { test, expect } from '@playwright/test';

/**
 * Basic sanity check that the home page loads and contains the project title.
 * Adjust the selector / expected text to match your actual UI.
 */
test('homepage loads and shows title', async ({ page }) => {
  await page.goto('/');
  // Expect the page title to contain "Epstein" – change as appropriate.
  await expect(page).toHaveTitle(/Epstein/);
});
