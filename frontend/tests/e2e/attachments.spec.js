import { test, expect } from '@playwright/test';

test.describe('Attachments', () => {
  test.beforeEach(async ({ page }) => {
    // Login
    await page.goto('/login');
    await page.fill('input[name="username"]', 'testuser');
    await page.fill('input[name="password"]', 'testpassword');
    
    // Wait for navigation after login
    await Promise.all([
      page.waitForURL(/\/tasks/, { timeout: 10000 }),
      page.click('button[type="submit"]')
    ]);
  });

  test('should upload attachment to task', async ({ page }) => {
    // Navigate to create task page
    await page.click('text=/Create Task/i');
    await expect(page).toHaveURL(/\/tasks\/new/);
    
    // Fill in task form
    await page.fill('input[name="title"]', 'Task with Attachment');
    await page.fill('textarea[name="description"]', 'Test attachment upload');
    
    // Submit and wait for navigation to task detail page
    await Promise.all([
      page.waitForURL(/\/tasks\/\d+/, { timeout: 10000 }),
      page.click('button[type="submit"]')
    ]);
    
    // Check if attachments section exists (use heading to avoid ambiguity)
    const attachmentsSection = page.locator('h2:has-text("Attachments")');
    await expect(attachmentsSection).toBeVisible();
    
    // Note: File upload testing requires a file - this is a basic smoke test
    // Full file upload test would need a test file fixture
  });

  test('should display attachments section on task detail', async ({ page }) => {
    // Navigate to any task
    const firstTask = page.locator('[class*="cursor-pointer"]').first();
    const taskCount = await firstTask.count();
    
    if (taskCount > 0) {
      await firstTask.click();
      await expect(page).toHaveURL(/\/tasks\/\d+/);
      
      // Should see attachments section (use heading to avoid ambiguity)
      await expect(page.locator('h2:has-text("Attachments")')).toBeVisible();
    } else {
      test.skip();
    }
  });
});
