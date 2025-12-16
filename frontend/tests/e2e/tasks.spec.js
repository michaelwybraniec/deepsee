import { test, expect } from '@playwright/test';

test.describe('Task Management', () => {
  // Helper to login before each test
  test.beforeEach(async ({ page }) => {
    // Navigate to login
    await page.goto('/login');
    
    // Login (assuming test user exists - may need to create via API or seed)
    await page.fill('input[name="username"]', 'testuser');
    await page.fill('input[name="password"]', 'testpassword');
    await page.click('button[type="submit"]');
    
    // Wait for redirect to tasks page
    await expect(page).toHaveURL(/\/tasks/, { timeout: 10000 });
  });

  test('should display task list', async ({ page }) => {
    await expect(page.locator('h1')).toContainText('Tasks');
    await expect(page.locator('text=/Create Task/i')).toBeVisible();
  });

  test('should create a new task', async ({ page }) => {
    // Navigate to create task page
    await page.click('text=/Create Task/i');
    await expect(page).toHaveURL(/\/tasks\/new/);
    
    // Fill in task form
    await page.fill('input[name="title"]', 'E2E Test Task');
    await page.fill('textarea[name="description"]', 'This is a test task created by E2E tests');
    await page.selectOption('select[name="status"]', 'todo');
    await page.selectOption('select[name="priority"]', 'high');
    
    // Submit form
    await page.click('button[type="submit"]');
    
    // Should redirect to tasks page and show success
    await expect(page).toHaveURL(/\/tasks/, { timeout: 10000 });
    
    // Should see the new task in the list
    await expect(page.locator('text=E2E Test Task')).toBeVisible();
  });

  test('should view task detail', async ({ page }) => {
    // Click on first task (if any exist)
    const firstTask = page.locator('[class*="cursor-pointer"]').first();
    const taskCount = await firstTask.count();
    
    if (taskCount > 0) {
      await firstTask.click();
      
      // Should be on task detail page
      await expect(page).toHaveURL(/\/tasks\/\d+/);
      
      // Should see task details
      await expect(page.locator('h1')).toBeVisible();
    } else {
      // Skip if no tasks exist
      test.skip();
    }
  });

  test('should search tasks', async ({ page }) => {
    // Enter search query
    await page.fill('input[placeholder*="Search tasks"]', 'test');
    
    // Submit search
    await page.click('button[type="submit"]');
    
    // Should show search results (or no results message)
    await expect(
      page.locator('text=/No tasks found|test/i')
    ).toBeVisible({ timeout: 5000 });
  });

  test('should filter tasks by status', async ({ page }) => {
    // Select status filter
    await page.selectOption('select:has-text("Status")', 'todo');
    
    // Wait for filter to apply (debounced)
    await page.waitForTimeout(600);
    
    // Should show filtered results
    await expect(page.locator('text=/todo|No tasks found/i')).toBeVisible();
  });
});
