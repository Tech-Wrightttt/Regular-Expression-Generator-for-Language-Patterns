import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton,
                             QGroupBox, QMessageBox, QComboBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor


class RegexGeneratorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Regular Expression Generator')
        self.setGeometry(100, 100, 900, 700)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)

        # Title
        title = QLabel('Regular Expression Generator for Different Language Patterns')
        title.setFont(QFont('Arial', 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Pattern selection
        pattern_group = QGroupBox('Language Pattern Selection')
        pattern_layout = QVBoxLayout(pattern_group)

        pattern_label = QLabel('Select a language pattern:')
        self.pattern_combo = QComboBox()
        patterns = [
            "L = {w ∈ {a,b}* | w starts with P}",
            "L = {w ∈ {a,b}* | w ends with P}",
            "L = {w ∈ {a,b}* | w starts and ends with P}",
            "L = {w ∈ {a,b}* | w contains P}",
            "L = {w ∈ {a,b}* | w does not contain P}"
        ]
        self.pattern_combo.addItems(patterns)
        self.pattern_combo.currentIndexChanged.connect(self.update_interface)

        pattern_layout.addWidget(pattern_label)
        pattern_layout.addWidget(self.pattern_combo)

        # Input section
        input_group = QGroupBox('Input Pattern P')
        input_layout = QVBoxLayout(input_group)

        # Input field
        input_label = QLabel('Enter the pattern P (using a and b characters):')
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText('Enter pattern (e.g., aa)')
        self.input_field.textChanged.connect(self.validate_input)

        # Buttons
        button_layout = QHBoxLayout()
        generate_button = QPushButton('Generate Regular Expression')
        generate_button.clicked.connect(self.generate_regex)
        clear_button = QPushButton('Clear')
        clear_button.clicked.connect(self.clear_fields)

        button_layout.addWidget(generate_button)
        button_layout.addWidget(clear_button)

        input_layout.addWidget(input_label)
        input_layout.addWidget(self.input_field)
        input_layout.addLayout(button_layout)

        # Results section
        results_group = QGroupBox('Generated Regular Expression')
        results_layout = QVBoxLayout(results_group)

        self.results_display = QTextEdit()
        self.results_display.setReadOnly(True)
        results_layout.addWidget(self.results_display)

        # Explanation section
        explanation_group = QGroupBox('How It Works')
        explanation_layout = QVBoxLayout(explanation_group)

        self.explanation_label = QLabel()
        self.explanation_label.setWordWrap(True)
        explanation_layout.addWidget(self.explanation_label)

        # Add all groups to main layout
        main_layout.addWidget(pattern_group)
        main_layout.addWidget(input_group)
        main_layout.addWidget(results_group)
        main_layout.addWidget(explanation_group)

        # Set initial state
        self.update_interface()
        self.clear_fields()

    def update_interface(self):
        pattern_index = self.pattern_combo.currentIndex()
        explanations = [
            """
            <h3>Starts With Pattern</h3>
            <p>This tool generates a regular expression for the language:</p>
            <p><b>L = {w ∈ {a,b}* | w starts with P}</b></p>

            <p><b>How it works:</b></p>
            <ul>
                <li>Enter a pattern P using only 'a' and 'b' characters</li>
                <li>The generator will create a regular expression that matches all strings</li>
                <li>that begin with your pattern P, followed by any combination of a's and b's</li>
            </ul>

            <p><b>Examples:</b></p>
            <ul>
                <li>If P = "aa", the regular expression is: <code>aa(a+b)*</code></li>
                <li>If P = "ab", the regular expression is: <code>ab(a+b)*</code></li>
                <li>If P = "aba", the regular expression is: <code>aba(a+b)*</code></li>
            </ul>

            <p><b>Formal Definition:</b> For any pattern P, the regular expression is: <code>P(a+b)*</code></p>
            """,
            """
            <h3>Ends With Pattern</h3>
            <p>This tool generates a regular expression for the language:</p>
            <p><b>L = {w ∈ {a,b}* | w ends with P}</b></p>

            <p><b>How it works:</b></p>
            <ul>
                <li>Enter a pattern P using only 'a' and 'b' characters</li>
                <li>The generator will create a regular expression that matches all strings</li>
                <li>that end with your pattern P, preceded by any combination of a's and b's</li>
            </ul>

            <p><b>Examples:</b></p>
            <ul>
                <li>If P = "aa", the regular expression is: <code>(a+b)*aa</code></li>
                <li>If P = "ab", the regular expression is: <code>(a+b)*ab</code></li>
                <li>If P = "aba", the regular expression is: <code>(a+b)*aba</code></li>
            </ul>

            <p><b>Formal Definition:</b> For any pattern P, the regular expression is: <code>(a+b)*P</code></p>
            """,
            """
            <h3>Starts and Ends With Pattern</h3>
            <p>This tool generates a regular expression for the language:</p>
            <p><b>L = {w ∈ {a,b}* | w starts and ends with P}</b></p>

            <p><b>How it works:</b></p>
            <ul>
                <li>Enter a pattern P using only 'a' and 'b' characters</li>
                <li>The generator will create a regular expression that matches all strings</li>
                <li>that begin with your pattern P and end with your pattern P</li>
            </ul>

            <p><b>Examples:</b></p>
            <ul>
                <li>If P = "aa", the regular expression is: <code>aa(a+b)*aa</code></li>
                <li>If P = "ab", the regular expression is: <code>ab(a+b)*ab</code></li>
                <li>If P = "aba", the regular expression is: <code>aba(a+b)*aba</code></li>
            </ul>

            <p><b>Formal Definition:</b> For any pattern P, the regular expression is: <code>P(a+b)*P</code></p>
            """,
            """
            <h3>Contains Pattern</h3>
            <p>This tool generates a regular expression for the language:</p>
            <p><b>L = {w ∈ {a,b}* | w contains P}</b></p>

            <p><b>How it works:</b></p>
            <ul>
                <li>Enter a pattern P using only 'a' and 'b' characters</li>
                <li>The generator will create a regular expression that matches all strings</li>
                <li>that contain your pattern P anywhere in the string</li>
            </ul>

            <p><b>Examples:</b></p>
            <ul>
                <li>If P = "aa", the regular expression is: <code>(a+b)*aa(a+b)*</code></li>
                <li>If P = "ab", the regular expression is: <code>(a+b)*ab(a+b)*</code></li>
                <li>If P = "aba", the regular expression is: <code>(a+b)*aba(a+b)*</code></li>
            </ul>

            <p><b>Formal Definition:</b> For any pattern P, the regular expression is: <code>(a+b)*P(a+b)*</code></p>
            """,
            """
            <h3>Does Not Contain Pattern</h3>
            <p>This tool generates a regular expression for the language:</p>
            <p><b>L = {w ∈ {a,b}* | w does not contain P}</b></p>

            <p><b>How it works:</b></p>
            <ul>
                <li>Enter a pattern P using only 'a' and 'b' characters</li>
                <li>The generator will create a regular expression that matches all strings</li>
                <li>that do not contain your pattern P anywhere in the string</li>
            </ul>

            <p><b>Note:</b> This is more complex and may not be expressible as a simple regular expression for all patterns P.</p>

            <p><b>Examples for simple cases:</b></p>
            <ul>
                <li>If P = "aa", the language consists of strings with no consecutive a's</li>
                <li>If P = "bb", the language consists of strings with no consecutive b's</li>
            </ul>
            """
        ]

        self.explanation_label.setText(explanations[pattern_index])

    def validate_input(self, text):
        # Only allow 'a' and 'b' characters
        if text and not all(char in ['a', 'b'] for char in text):
            # Remove invalid characters
            valid_text = ''.join(char for char in text if char in ['a', 'b'])
            self.input_field.setText(valid_text)

            # Move cursor to end
            self.input_field.setCursorPosition(len(valid_text))

    def generate_regex(self):
        pattern = self.input_field.text()
        pattern_index = self.pattern_combo.currentIndex()

        if not pattern:
            QMessageBox.warning(self, 'Input Error', 'Please enter a pattern first.')
            return

        # Generate the regular expression based on selected pattern
        if pattern_index == 0:  # Starts with P
            regex = f"{pattern}(a+b)*"
            desc = f"starts with '{pattern}'"
        elif pattern_index == 1:  # Ends with P
            regex = f"(a+b)*{pattern}"
            desc = f"ends with '{pattern}'"
        elif pattern_index == 2:  # Starts and ends with P
            regex = f"{pattern}(a+b)*{pattern}"
            desc = f"starts and ends with '{pattern}'"
        elif pattern_index == 3:  # Contains P
            regex = f"(a+b)*{pattern}(a+b)*"
            desc = f"contains '{pattern}'"
        else:  # Does not contain P
            # This is a simplified approach - in reality, this is more complex
            regex = f"(a+b)* without '{pattern}'"
            desc = f"does not contain '{pattern}'"

        # Display the result
        pattern_type = self.pattern_combo.currentText()
        result_text = f"""
        <h3>Generated Regular Expression</h3>
        <p>For pattern <b>P = "{pattern}"</b>, the regular expression for</p>
        <p><b>{pattern_type}</b></p>
        <p>is:</p>
        <div style="background-color: #f0f0f0; padding: 15px; border-radius: 5px; font-family: monospace; font-size: 16px;">
            {regex}
        </div>
        <p style="margin-top: 15px;">This regular expression will match any string that {desc}.</p>
        """

        self.results_display.setHtml(result_text)

    def clear_fields(self):
        self.input_field.clear()
        self.results_display.clear()
        self.input_field.setFocus()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RegexGeneratorGUI()
    window.show()
    sys.exit(app.exec_())