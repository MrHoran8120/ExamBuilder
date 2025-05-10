# ----- exam_builder/question_form.py -----
from __future__ import annotations
from playwright.sync_api import Page
import time

class QuestionFormFiller:
    """Handles all interactions for creating and saving a question modal."""
    def __init__(self, page: Page) -> None:
        self.page = page

    def click_create_question(self) -> None:
        locator = self.page.locator('button:has-text("Create question")')
        count = locator.count()
        if count == 0:
            raise Exception("No 'Create question' button found.")
        locator.nth(count - 1).scroll_into_view_if_needed()
        locator.nth(count - 1).click()
        print("Opened question modal.")

    def fill_question_text(self, text: str) -> None:
        sel = '[data-testid="question-formulation-input"] div.fr-element.fr-view[contenteditable]'
        self.page.wait_for_selector(sel)
        self.page.locator(sel).fill(text)
        print("Filled question text.")

    def add_options(self, options: list[str]) -> None:
        base = "div.fr-wrapper >> div.fr-element.fr-view[contenteditable]"
        for opt in options:
            self.page.wait_for_selector(base)
            self.page.locator(base).last.fill(opt)
            self.page.get_by_text("Add answer").first.click()
            time.sleep(0.3)
            print(f"Added option: {opt}")

    def mark_correct_option(self, correct_answers: list[str], expected_count: int) -> None:
        correct_norm = [a.strip().lower() for a in correct_answers]
        self.page.wait_for_selector('div.OptionRow.animation', timeout=30000)
        rows = self.page.locator('div.OptionRow.animation')
        found = 0
        for i in range(rows.count()):
            label = rows.nth(i).locator('.MultipleChoiceAnswerOptions__option-label').inner_text().strip()
            if label.lower() in correct_norm:
                toggle = rows.nth(i).locator('[data-testid="correct-answer-toggle"] input[type="checkbox"]')
                if not toggle.is_checked():
                    toggle.click(force=True)
                found += 1
                print(f"Marked correct: {label}")
        if found != len(correct_norm):
            raise Exception(f"Expected {len(correct_norm)} correct but marked {found}.")

    def save_question(self) -> None:
        self.page.get_by_text("Save and close this question").last.click()
        print("Question saved.")
