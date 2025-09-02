from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton,
                             QGroupBox, QComboBox, QSpinBox, QStackedWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon


class RegexView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowIcon(QIcon("2bLogo.jpg"))

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
        pattern2_label = QLabel('Enter pattern P2 (using a and b characters):')
        self.pattern_input_p2 = QLineEdit()
        self.pattern_input_p2.setPlaceholderText('Enter second pattern')
        pattern3_label = QLabel('Enter pattern P3 (using a and b characters):')
        self.pattern_input_p3 = QLineEdit()
        self.pattern_input_p3.setPlaceholderText('Enter third pattern (optional)')
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
        self.generate_button = QPushButton('Generate Regular Expression')
        self.clear_button = QPushButton('Clear')
        button_layout.addWidget(self.generate_button)
        button_layout.addWidget(self.clear_button)
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

    def set_patterns(self, patterns):
        self.pattern_combo.clear()
        self.pattern_combo.addItems(patterns)

    def set_explanation(self, text):
        self.explanation_label.setText(text)

    def set_results(self, text):
        self.results_display.setHtml(text)

    def clear_inputs(self):
        self.pattern_input.clear()
        self.pattern_input2.clear()
        self.pattern_input_p1.clear()
        self.pattern_input_p2.clear()
        self.pattern_input_p3.clear()
        self.number_input.setValue(2)
        self.number_input2.setValue(2)
        self.results_display.clear()

    def set_input_widget(self, index):
        self.stacked_inputs.setCurrentIndex(index)

    def set_focus(self, index):
        if index == 0:
            self.pattern_input.setFocus()
        elif index == 1:
            self.number_input.setFocus()
        elif index == 2:
            self.pattern_input2.setFocus()
        else:
            self.pattern_input_p1.setFocus()

    def get_current_pattern_index(self):
        return self.pattern_combo.currentIndex()

    def get_pattern_input(self):
        return self.pattern_input.text()

    def get_pattern_input2(self):
        return self.pattern_input2.text()

    def get_number_input(self):
        return self.number_input.value()

    def get_number_input2(self):
        return self.number_input2.value()

    def get_pattern_input_p1(self):
        return self.pattern_input_p1.text()

    def get_pattern_input_p2(self):
        return self.pattern_input_p2.text()

    def get_pattern_input_p3(self):
        return self.pattern_input_p3.text()

    def set_pattern_input(self, text):
        self.pattern_input.setText(text)

    def set_pattern_input2(self, text):
        self.pattern_input2.setText(text)

    def set_pattern_input_p1(self, text):
        self.pattern_input_p1.setText(text)

    def set_pattern_input_p2(self, text):
        self.pattern_input_p2.setText(text)

    def set_pattern_input_p3(self, text):
        self.pattern_input_p3.setText(text)