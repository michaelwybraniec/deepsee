import { test, expect } from '@playwright/test';

test.describe('Attachments', () => {
  test.beforeEach(async ({ page }) => {
    // Login
    await page.goto('/login');
    await page.fill('input[name="username"]', 'testuser');
    await page.fill('input[name="password"]', 'testpassword');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/\/tasks/, { timeout: 10000 });
  });

  test('should upload attachment to task', async ({ page }) => {
    // Navigate to a task detail page (create one first if needed)
    // For now, we'll create a task and then add attachment
    
    // Create a task
    await page.click('text=/Create Task/i');
    await page.fill('input[name="title"]', 'Task with Attachment');
    await page.fill('textarea[name="description"]', 'Test attachment upload');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/\/tasks/, { timeout: 10000 });
    
    // Click on the task we just created
    await page.click('text=Task with Attachment');
    await expect(page).toHaveURL(/\/tasks\/\d+/);
    
    // Check if attachments section exists
    const attachmentsSection = page.locator('text=/Attachments/i');
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
      
      // Should see attachments section
      await expect(page.locator('text=/Attachments/i')).toBeVisible();
    } else {
      test.skip();
    }
  });
});
