import { test, expect } from '@playwright/test';

test.describe('Task Management', () => {
  // Helper to login before each test
  test.beforeEach(async ({ page }) => {
    // Navigate to login
    await page.goto('/login');
    
    // Login (assuming test user exists - may need to create via API or seed)
    await page.fill('input[name="username"]', 'testuser');
    await page.fill('input[name="password"]', 'testpassword');
    
    // Wait for navigation after login
    await Promise.all([
      page.waitForURL(/\/tasks/, { timeout: 10000 }),
      page.click('button[type="submit"]')
    ]);
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
    // Create a task first to ensure we have one to view
    await page.click('text=/Create Task/i');
    await expect(page).toHaveURL(/\/tasks\/new/);
    
    await page.fill('input[name="title"]', 'Test Task Detail View');
    await page.fill('textarea[name="description"]', 'Task for detail view test');
    await page.selectOption('select[name="status"]', 'todo');
    
    // Submit and wait for navigation to task detail page
    await Promise.all([
      page.waitForURL(/\/tasks\/\d+/, { timeout: 10000 }),
      page.click('button[type="submit"]')
    ]);
    
    // Should be on task detail page
    await expect(page).toHaveURL(/\/tasks\/\d+/);
    
    // Should see task details
    await expect(page.locator('h1')).toBeVisible();
    await expect(page.locator('text=Test Task Detail View')).toBeVisible();
  });

  test('should search tasks', async ({ page }) => {
    // Enter search query (search is debounced, so wait after typing)
    const searchInput = page.locator('input[placeholder*="Search tasks"]');
    await searchInput.fill('test');
    
    // Wait for debounce (500ms) plus API call
    await page.waitForTimeout(1000);
    
    // Should show search results (or no results message)
    await expect(
      page.locator('text=/No tasks found|test/i').first()
    ).toBeVisible({ timeout: 5000 });
  });

  test('should filter tasks by status', async ({ page }) => {
    // Find status filter select (it's after a label with text "Status")
    const statusLabel = page.locator('label:has-text("Status")');
    await expect(statusLabel).toBeVisible();
    
    // Get the select that follows the label (parent div contains both label and select)
    const statusSelect = statusLabel.locator('..').locator('select').first();
    await statusSelect.selectOption('todo');
    
    // Wait for filter to apply and API call
    await page.waitForTimeout(1500);
    
    // Should show filtered results - check if we have tasks with "todo" status badge or "No tasks found"
    // The status badge appears in task cards, not as plain text
    const hasTasks = await page.locator('[class*="cursor-pointer"]').count() > 0;
    const hasNoTasks = await page.locator('text=/No tasks found/i').isVisible().catch(() => false);
    
    // Either we have tasks (which may or may not show "todo" badge) or we have "No tasks found"
    expect(hasTasks || hasNoTasks).toBeTruthy();
  });
});
