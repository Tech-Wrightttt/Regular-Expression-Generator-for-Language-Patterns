import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton,
                             QGroupBox, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPalette


class RegexGeneratorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Regular Expression Generator')
        self.setGeometry(100, 100, 800, 600)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)

        # Title
        title = QLabel('Regular Expression Generator: L = {w ∈ {a,b}* | w starts with P}')
        title.setFont(QFont('Arial', 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Input section
        input_group = QGroupBox('Input Pattern P')
        input_layout = QVBoxLayout(input_group)

        # Input field
        input_label = QLabel('Enter the starting pattern P (using a and b characters):')
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

        explanation_text = """
        <h3>Regular Expression Generator</h3>
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
        """

        explanation_label = QLabel(explanation_text)
        explanation_label.setWordWrap(True)
        explanation_layout.addWidget(explanation_label)

        # Add all groups to main layout
        main_layout.addWidget(input_group)
        main_layout.addWidget(results_group)
        main_layout.addWidget(explanation_group)

        # Set initial state
        self.clear_fields()

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

        if not pattern:
            QMessageBox.warning(self, 'Input Error', 'Please enter a pattern first.')
            return

        # Generate the regular expression
        regex = f"{pattern}(a+b)*"

        # Display the result
        result_text = f"""
        <h3>Generated Regular Expression</h3>
        <p>For pattern <b>P = "{pattern}"</b>, the regular expression for</p>
        <p><b>L = {{w ∈ {{a,b}}* | w starts with {pattern}}}</b></p>
        <p>is:</p>
        <div style="background-color: #f0f0f0; padding: 15px; border-radius: 5px; font-family: monospace; font-size: 16px;">
            {regex}
        </div>
        <p style="margin-top: 15px;">This regular expression will match any string that begins with "{pattern}" 
        followed by any combination of a's and b's (including none).</p>
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