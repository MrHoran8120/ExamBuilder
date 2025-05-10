# ----- exam_builder/automator.py -----
from exam_builder.browser_manager import setup_browser
from exam_builder.json_loader import load_questions
from exam_builder.question_form import QuestionFormFiller


class ExamBuilderAutomator:
    """Orchestrates loading questions, browser setup, and processing each question."""
    def __init__(self, browser_url: str = "http://127.0.0.1:9222", json_file: str = "questions.json"):
        self.browser_url = browser_url
        self.json_file = json_file
        self.page = None

    def run(self):
        """Main entry: connect browser, load questions, process all."""
        self.page = setup_browser(self.browser_url)
        questions = load_questions(self.json_file)
        form = QuestionFormFiller(self.page)
        for q in questions:
            try:
                self.process_question(q, form)
            except Exception as e:
                print(f"Error processing question '{q.get('question')}': {e}")

    def process_question(self, question: dict, form: QuestionFormFiller):
        """Fill out and save one question."""
        form.click_create_question()
        # select multiple-choice type, then:
        form.fill_question_text(question['question'])
        form.add_options(question['options'])
        answers = question.get('answer') or question.get('answers')
        form.mark_correct_option(
            correct_answers=(answers if isinstance(answers, list) else [answers]),
            expected_count=len(question['options'])
        )
        form.save_question()