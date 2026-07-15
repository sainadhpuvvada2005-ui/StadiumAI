import { expect, test } from "@playwright/test";

test("landing page exposes the product and dashboard entry point", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "STADIUMAI" })).toBeVisible();
  await expect(page.getByRole("link", { name: /open dashboard/i })).toBeVisible();
});
