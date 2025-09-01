import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton,
                             QGroupBox, QMessageBox, QComboBox, QSpinBox, QStackedWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor


class RegexGeneratorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Advanced Regular Expression Generator')
        self.setGeometry(100, 100, 1000, 800)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)

        # Title
        title = QLabel('Advanced Regular Expression Generator for Language Patterns')
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
            "L = {w ∈ {a,b}* | w does not contain P}",
            "L = {w ∈ {a,b}* | w contains P and starts with P}",
            "L = {w ∈ {a,b}* | w contains P and ends with P}",
            "L = {w ∈ {a,b}* | w contains P and starts with P and ends with P}",
            "L = {w ∈ {a,b}* | |w| > N }",
            "L = {w ∈ {a,b}* | |w| < N }",
            "L = {w ∈ {a,b}* | |w| >= N }",
            "L = {w ∈ {a,b}* | |w| <= N }",
            "L = {w ∈ {a,b}* | |w| = N }",
            "L = {w ∈ {a,b}* | # of P in w is divisible by N }",
            "L = {w ∈ {a,b}* | the Nth symbol of w is P}",
            "L = {w ∈ {a,b}* | the Nth symbol from the last is P}"
        ]
        self.pattern_combo.addItems(patterns)
        self.pattern_combo.currentIndexChanged.connect(self.update_interface)

        pattern_layout.addWidget(pattern_label)
        pattern_layout.addWidget(self.pattern_combo)

        # Input section - using stacked widget for different input types
        input_group = QGroupBox('Input Parameters')
        input_layout = QVBoxLayout(input_group)

        self.stacked_inputs = QStackedWidget()

        # Pattern only input
        pattern_only_widget = QWidget()
        pattern_only_layout = QVBoxLayout(pattern_only_widget)
        pattern_label = QLabel('Enter pattern P (using a and b characters):')
        self.pattern_input = QLineEdit()
        self.pattern_input.setPlaceholderText('Enter pattern (e.g., aa)')
        self.pattern_input.textChanged.connect(self.validate_pattern_input)
        pattern_only_layout.addWidget(pattern_label)
        pattern_only_layout.addWidget(self.pattern_input)
        self.stacked_inputs.addWidget(pattern_only_widget)

        # Number only input
        number_only_widget = QWidget()
        number_only_layout = QVBoxLayout(number_only_widget)
        number_label = QLabel('Enter number N:')
        self.number_input = QSpinBox()
        self.number_input.setMinimum(0)
        self.number_input.setMaximum(1000)
        self.number_input.setValue(2)
        number_only_layout.addWidget(number_label)
        number_only_layout.addWidget(self.number_input)
        self.stacked_inputs.addWidget(number_only_widget)

        # Pattern and number input
        pattern_number_widget = QWidget()
        pattern_number_layout = QVBoxLayout(pattern_number_widget)
        pattern_label2 = QLabel('Enter pattern P (using a and b characters):')
        self.pattern_input2 = QLineEdit()
        self.pattern_input2.setPlaceholderText('Enter pattern (e.g., aa)')
        self.pattern_input2.textChanged.connect(self.validate_pattern_input2)
        number_label2 = QLabel('Enter number N:')
        self.number_input2 = QSpinBox()
        self.number_input2.setMinimum(1)
        self.number_input2.setMaximum(1000)
        self.number_input2.setValue(2)
        pattern_number_layout.addWidget(pattern_label2)
        pattern_number_layout.addWidget(self.pattern_input2)
        pattern_number_layout.addWidget(number_label2)
        pattern_number_layout.addWidget(self.number_input2)
        self.stacked_inputs.addWidget(pattern_number_widget)

        # Multiple patterns input
        multi_pattern_widget = QWidget()
        multi_pattern_layout = QVBoxLayout(multi_pattern_widget)
        pattern1_label = QLabel('Enter pattern P1 (using a and b characters):')
        self.pattern_input_p1 = QLineEdit()
        self.pattern_input_p1.setPlaceholderText('Enter first pattern')
        self.pattern_input_p1.textChanged.connect(self.validate_pattern_input_p1)
        pattern2_label = QLabel('Enter pattern P2 (using a and b characters):')
        self.pattern_input_p2 = QLineEdit()
        self.pattern_input_p2.setPlaceholderText('Enter second pattern')
        self.pattern_input_p2.textChanged.connect(self.validate_pattern_input_p2)
        pattern3_label = QLabel('Enter pattern P3 (using a and b characters):')
        self.pattern_input_p3 = QLineEdit()
        self.pattern_input_p3.setPlaceholderText('Enter third pattern (optional)')
        self.pattern_input_p3.textChanged.connect(self.validate_pattern_input_p3)
        multi_pattern_layout.addWidget(pattern1_label)
        multi_pattern_layout.addWidget(self.pattern_input_p1)
        multi_pattern_layout.addWidget(pattern2_label)
        multi_pattern_layout.addWidget(self.pattern_input_p2)
        multi_pattern_layout.addWidget(pattern3_label)
        multi_pattern_layout.addWidget(self.pattern_input_p3)
        self.stacked_inputs.addWidget(multi_pattern_widget)

        input_layout.addWidget(self.stacked_inputs)

        # Buttons
        button_layout = QHBoxLayout()
        generate_button = QPushButton('Generate Regular Expression')
        generate_button.clicked.connect(self.generate_regex)
        clear_button = QPushButton('Clear')
        clear_button.clicked.connect(self.clear_fields)

        button_layout.addWidget(generate_button)
        button_layout.addWidget(clear_button)

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

        # Set the appropriate input widget based on pattern type
        if pattern_index in [0, 1, 2, 3, 4]:  # Patterns requiring only P
            self.stacked_inputs.setCurrentIndex(0)
        elif pattern_index in [8, 9, 10, 11, 12]:  # Patterns requiring only N
            self.stacked_inputs.setCurrentIndex(1)
        elif pattern_index in [13, 14, 15]:  # Patterns requiring both P and N
            self.stacked_inputs.setCurrentIndex(2)
        else:  # Patterns requiring multiple patterns (5, 6, 7)
            self.stacked_inputs.setCurrentIndex(3)

        explanations = [
            # 0: Starts with P
            """
            <h3>Starts With Pattern</h3>
            <p>This tool generates a regular expression for the language:</p>
            <p><b>L = {w ∈ {a,b}* | w starts with P}</b></p>
            <p><b>Regular Expression:</b> P(a+b)*</p>
            """,
            # 1: Ends with P
            """
            <h3>Ends With Pattern</h3>
            <p>This tool generates a regular expression for the language:</p>
            <p><b>L = {w ∈ {a,b}* | w ends with P}</b></p>
            <p><b>Regular Expression:</b> (a+b)*P</p>
            """,
            # 2: Starts and ends with P
            """
            <h3>Starts and Ends With Pattern</h3>
            <p>This tool generates a regular expression for the language:</p>
            <p><b>L = {w ∈ {a,b}* | w starts and ends with P}</b></p>
            <p><b>Regular Expression:</b> P(a+b)*P or P(middle)* for overlapping patterns</p>
            """,
            # 3: Contains P
            """
            <h3>Contains Pattern</h3>
            <p>This tool generates a regular expression for the language:</p>
            <p><b>L = {w ∈ {a,b}* | w contains P}</b></p>
            <p><b>Regular Expression:</b> (a+b)*P(a+b)*</p>
            """,
            # 4: Does not contain P
            """
            <h3>Does Not Contain Pattern</h3>
            <p>This tool generates a regular expression for the language:</p>
            <p><b>L = {w ∈ {a,b}* | w does not contain P}</b></p>
            <p><b>Note:</b> This is complex and may not have a simple regex for all patterns.</p>
            """,
            # 5: Contains P and starts with P
            """
            <h3>Contains and Starts With Pattern</h3>
            <p>This tool generates a regular expression for the language:</p>
            <p><b>L = {w ∈ {a,b}* | w contains P and starts with P}</b></p>
            <p><b>Regular Expression:</b> P(a+b)* (since starting with P implies containing P)</p>
            """,
            # 6: Contains P and ends with P
            """
            <h3>Contains and Ends With Pattern</h3>
            <p>This tool generates a regular expression for the language:</p>
            <p><b>L = {w ∈ {a,b}* | w contains P and ends with P}</b></p>
            <p><b>Regular Expression:</b> (a+b)*P (since ending with P implies containing P)</p>
            """,
            # 7: Contains P and starts with P and ends with P
            """
            <h3>Contains, Starts With, and Ends With Pattern</h3>
            <p>This tool generates a regular expression for the language:</p>
            <p><b>L = {w ∈ {a,b}* | w contains P and starts with P and ends with P}</b></p>
            <p><b>Regular Expression:</b> P(a+b)*P or P(middle)* for overlapping patterns</p>
            """,
            # 8: |w| > N
            """
            <h3>Length Greater Than N</h3>
            <p>This tool generates a regular expression for the language:</p>
            <p><b>L = {w ∈ {a,b}* | |w| > N}</b></p>
            <p><b>Regular Expression:</b> (a+b)^(N+1)(a+b)*</p>
            """,
            # 9: |w| < N
            """
            <h3>Length Less Than N</h3>
            <p>This tool generates a regular expression for the language:</p>
            <p><b>L = {w ∈ {a,b}* | |w| < N}</b></p>
            <p><b>Regular Expression:</b> ε + (a+b) + (a+b)^2 + ... + (a+b)^(N-1)</p>
            """,
            # 10: |w| >= N
            """
            <h3>Length Greater Than or Equal To N</h3>
            <p>This tool generates a regular expression for the language:</p>
            <p><b>L = {w ∈ {a,b}* | |w| >= N}</b></p>
            <p><b>Regular Expression:</b> (a+b)^N(a+b)*</p>
            """,
            # 11: |w| <= N
            """
            <h3>Length Less Than or Equal To N</h3>
            <p>This tool generates a regular expression for the language:</p>
            <p><b>L = {w ∈ {a,b}* | |w| <= N}</b></p>
            <p><b>Regular Expression:</b> ε + (a+b) + (a+b)^2 + ... + (a+b)^N</p>
            """,
            # 12: |w| = N
            """
            <h3>Length Equal To N</h3>
            <p>This tool generates a regular expression for the language:</p>
            <p><b>L = {w ∈ {a,b}* | |w| = N}</b></p>
            <p><b>Regular Expression:</b> (a+b)^N</p>
            """,
            # 13: # of P in w is divisible by N
            """
            <h3>Count of P Divisible By N</h3>
            <p>This tool generates a regular expression for the language:</p>
            <p><b>L = {w ∈ {a,b}* | # of P in w is divisible by N}</b></p>
            <p><b>Note:</b> This requires building a finite automaton with N states.</p>
            """,
            # 14: Nth symbol is P
            """
            <h3>Nth Symbol Is P</h3>
            <p>This tool generates a regular expression for the language:</p>
            <p><b>L = {w ∈ {a,b}* | the Nth symbol of w is P}</b></p>
            <p><b>Regular Expression:</b> (a+b)^(N-1)P(a+b)*</p>
            """,
            # 15: Nth symbol from last is P
            """
            <h3>Nth Symbol From Last Is P</h3>
            <p>This tool generates a regular expression for the language:</p>
            <p><b>L = {w ∈ {a,b}* | the Nth symbol from the last is P}</b></p>
            <p><b>Regular Expression:</b> (a+b)*P(a+b)^(N-1)</p>
            """
        ]

        self.explanation_label.setText(explanations[pattern_index])

    def validate_pattern_input(self, text):
        # Only allow 'a' and 'b' characters
        if text and not all(char in ['a', 'b'] for char in text):
            valid_text = ''.join(char for char in text if char in ['a', 'b'])
            self.pattern_input.setText(valid_text)
            self.pattern_input.setCursorPosition(len(valid_text))

    def validate_pattern_input2(self, text):
        # Only allow 'a' and 'b' characters
        if text and not all(char in ['a', 'b'] for char in text):
            valid_text = ''.join(char for char in text if char in ['a', 'b'])
            self.pattern_input2.setText(valid_text)
            self.pattern_input2.setCursorPosition(len(valid_text))

    def validate_pattern_input_p1(self, text):
        # Only allow 'a' and 'b' characters
        if text and not all(char in ['a', 'b'] for char in text):
            valid_text = ''.join(char for char in text if char in ['a', 'b'])
            self.pattern_input_p1.setText(valid_text)
            self.pattern_input_p1.setCursorPosition(len(valid_text))

    def validate_pattern_input_p2(self, text):
        # Only allow 'a' and 'b' characters
        if text and not all(char in ['a', 'b'] for char in text):
            valid_text = ''.join(char for char in text if char in ['a', 'b'])
            self.pattern_input_p2.setText(valid_text)
            self.pattern_input_p2.setCursorPosition(len(valid_text))

    def validate_pattern_input_p3(self, text):
        # Only allow 'a' and 'b' characters
        if text and not all(char in ['a', 'b'] for char in text):
            valid_text = ''.join(char for char in text if char in ['a', 'b'])
            self.pattern_input_p3.setText(valid_text)
            self.pattern_input_p3.setCursorPosition(len(valid_text))

    def generate_regex(self):
        pattern_index = self.pattern_combo.currentIndex()

        # Get inputs based on pattern type
        if pattern_index in [0, 1, 2, 3, 4]:  # Patterns requiring only P
            pattern = self.pattern_input.text()
            if not pattern:
                QMessageBox.warning(self, 'Input Error', 'Please enter a pattern first.')
                return

        elif pattern_index in [8, 9, 10, 11, 12]:  # Patterns requiring only N
            N = self.number_input.value()

        elif pattern_index in [13, 14, 15]:  # Patterns requiring both P and N
            pattern = self.pattern_input2.text()
            N = self.number_input2.value()
            if not pattern:
                QMessageBox.warning(self, 'Input Error', 'Please enter a pattern first.')
                return

        else:  # Patterns requiring multiple patterns (5, 6, 7)
            p1 = self.pattern_input_p1.text()
            p2 = self.pattern_input_p2.text()
            p3 = self.pattern_input_p3.text()

            if not p1 or not p2:
                QMessageBox.warning(self, 'Input Error', 'Please enter at least two patterns.')
                return

        # Generate the regular expression based on selected pattern
        if pattern_index == 0:  # Starts with P
            regex = f"{pattern}(a+b)*"
            desc = f"starts with '{pattern}'"

        elif pattern_index == 1:  # Ends with P
            regex = f"(a+b)*{pattern}"
            desc = f"ends with '{pattern}'"

        elif pattern_index == 2:  # Starts and ends with P
            # Handle overlapping patterns
            overlap_possible = False
            overlap_length = 0

            for i in range(1, len(pattern)):
                if pattern.endswith(pattern[:i]):
                    overlap_possible = True
                    overlap_length = i
                    break

            if overlap_possible and len(pattern) > 0:
                middle_pattern = pattern[overlap_length:]
                if middle_pattern:
                    regex = f"{pattern}({middle_pattern})*"
                else:
                    regex = f"{pattern}({pattern})*"
            else:
                regex = f"{pattern}(a+b)*{pattern}"
            desc = f"starts and ends with '{pattern}'"

        elif pattern_index == 3:  # Contains P
            regex = f"(a+b)*{pattern}(a+b)*"
            desc = f"contains '{pattern}'"

        elif pattern_index == 4:  # Does not contain P
            # Simplified approach for common cases
            if pattern == "aa":
                regex = "b*(ab*)*"
                desc = "does not contain 'aa' (no consecutive a's)"
            elif pattern == "bb":
                regex = "a*(ba*)*"
                desc = "does not contain 'bb' (no consecutive b's)"
            else:
                regex = f"(a+b)* without '{pattern}'"
                desc = f"does not contain '{pattern}'"

        elif pattern_index == 5:  # Contains P and starts with P
            regex = f"{p1}(a+b)*"
            desc = f"contains '{p1}' and starts with '{p1}'"

        elif pattern_index == 6:  # Contains P and ends with P
            regex = f"(a+b)*{p1}"
            desc = f"contains '{p1}' and ends with '{p1}'"

        elif pattern_index == 7:  # Contains P and starts with P and ends with P
            # Use the same logic as starts and ends with P
            overlap_possible = False
            overlap_length = 0

            for i in range(1, len(p1)):
                if p1.endswith(p1[:i]):
                    overlap_possible = True
                    overlap_length = i
                    break

            if overlap_possible and len(p1) > 0:
                middle_pattern = p1[overlap_length:]
                if middle_pattern:
                    regex = f"{p1}({middle_pattern})*"
                else:
                    regex = f"{p1}({p1})*"
            else:
                regex = f"{p1}(a+b)*{p1}"
            desc = f"contains '{p1}', starts with '{p1}', and ends with '{p1}'"

        elif pattern_index == 8:  # |w| > N
            regex = f"(a+b)^{{{N + 1}}}(a+b)*"
            desc = f"has length greater than {N}"

        elif pattern_index == 9:  # |w| < N
            # Create union of all lengths from 0 to N-1
            parts = ["ε"] + [f"(a+b)^{{{i}}}" for i in range(1, N)]
            regex = " + ".join(parts)
            desc = f"has length less than {N}"

        elif pattern_index == 10:  # |w| >= N
            regex = f"(a+b)^{{{N}}}(a+b)*"
            desc = f"has length greater than or equal to {N}"

        elif pattern_index == 11:  # |w| <= N
            # Create union of all lengths from 0 to N
            parts = ["ε"] + [f"(a+b)^{{{i}}}" for i in range(1, N + 1)]
            regex = " + ".join(parts)
            desc = f"has length less than or equal to {N}"

        elif pattern_index == 12:  # |w| = N
            regex = f"(a+b)^{{{N}}}"
            desc = f"has length exactly {N}"

        elif pattern_index == 13:  # # of P in w is divisible by N
            # This is complex - simplified representation
            regex = f"( (a+b)*{pattern}(a+b)* ) where count of '{pattern}' is divisible by {N}"
            desc = f"has count of '{pattern}' divisible by {N}"

        elif pattern_index == 14:  # Nth symbol is P
            if N == 1:
                regex = f"{pattern}(a+b)*"
            else:
                regex = f"(a+b)^{{{N - 1}}}{pattern}(a+b)*"
            desc = f"has the {N}th symbol as '{pattern}'"

        elif pattern_index == 15:  # Nth symbol from last is P
            if N == 1:
                regex = f"(a+b)*{pattern}"
            else:
                regex = f"(a+b)*{pattern}(a+b)^{{{N - 1}}}"
            desc = f"has the {N}th symbol from the last as '{pattern}'"

        # Display the result
        pattern_type = self.pattern_combo.currentText()
        result_text = f"""
        <h3>Generated Regular Expression</h3>
        <p>For <b>{pattern_type}</b></p>
        <p>The regular expression is:</p>
        <div style="background-color: #f0f0f0; padding: 15px; border-radius: 5px; font-family: monospace; font-size: 16px;">
            {regex}
        </div>
        <p style="margin-top: 15px;">This regular expression will match any string that {desc}.</p>
        """

        self.results_display.setHtml(result_text)

    def clear_fields(self):
        self.pattern_input.clear()
        self.pattern_input2.clear()
        self.pattern_input_p1.clear()
        self.pattern_input_p2.clear()
        self.pattern_input_p3.clear()
        self.number_input.setValue(2)
        self.number_input2.setValue(2)
        self.results_display.clear()

        # Set focus to the appropriate input based on current pattern
        pattern_index = self.pattern_combo.currentIndex()
        if pattern_index in [0, 1, 2, 3, 4]:
            self.pattern_input.setFocus()
        elif pattern_index in [8, 9, 10, 11, 12]:
            self.number_input.setFocus()
        elif pattern_index in [13, 14, 15]:
            self.pattern_input2.setFocus()
        else:
            self.pattern_input_p1.setFocus()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RegexGeneratorGUI()
    window.show()
    sys.exit(app.exec_())