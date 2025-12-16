import { test, expect } from '@playwright/test';

test.describe('Authentication', () => {
  test('should login successfully with valid credentials', async ({ page }) => {
    await page.goto('/login');
    
    // Fill in login form
    await page.fill('input[name="username"]', 'testuser');
    await page.fill('input[name="password"]', 'testpassword');
    
    // Submit form
    await page.click('button[type="submit"]');
    
    // Should redirect to tasks page
    await expect(page).toHaveURL(/\/tasks/);
    
    // Should see tasks page
    await expect(page.locator('h1')).toContainText('Tasks');
  });

  test('should show error with invalid credentials', async ({ page }) => {
    await page.goto('/login');
    
    // Fill in login form with invalid credentials
    await page.fill('input[name="username"]', 'invaliduser');
    await page.fill('input[name="password"]', 'wrongpassword');
    
    // Submit form
    await page.click('button[type="submit"]');
    
    // Should show error message
    await expect(page.locator('text=/login failed|invalid/i')).toBeVisible();
  });

  test('should register new user and auto-login', async ({ page }) => {
    // Generate unique username
    const timestamp = Date.now();
    const username = `testuser_${timestamp}`;
    const email = `test_${timestamp}@example.com`;
    const password = 'testpassword123';
    
    await page.goto('/register');
    
    // Fill in registration form
    await page.fill('input[name="username"]', username);
    await page.fill('input[name="email"]', email);
    await page.fill('input[name="password"]', password);
    await page.fill('input[name="confirmPassword"]', password);
    
    // Submit form
    await page.click('button[type="submit"]');
    
    // Should redirect to tasks page after auto-login
    await expect(page).toHaveURL(/\/tasks/, { timeout: 10000 });
    
    // Should see tasks page
    await expect(page.locator('h1')).toContainText('Tasks');
  });
});
