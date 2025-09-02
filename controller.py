from PyQt5.QtWidgets import QMessageBox


class RegexController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.connect_signals()

    def initialize(self):
        # Set up the view with data from the model
        self.view.set_patterns(self.model.get_patterns())
        self.view.set_explanation(self.model.get_explanation(0))
        self.view.set_input_widget(0)
        self.view.set_focus(0)

    def connect_signals(self):
        # Connect UI signals to controller methods
        self.view.pattern_combo.currentIndexChanged.connect(self.on_pattern_changed)
        self.view.generate_button.clicked.connect(self.on_generate_clicked)
        self.view.clear_button.clicked.connect(self.on_clear_clicked)

        # Connect input validation
        self.view.pattern_input.textChanged.connect(self.on_pattern_input_changed)
        self.view.pattern_input2.textChanged.connect(self.on_pattern_input2_changed)
        self.view.pattern_input_p1.textChanged.connect(self.on_pattern_input_p1_changed)
        self.view.pattern_input_p2.textChanged.connect(self.on_pattern_input_p2_changed)
        self.view.pattern_input_p3.textChanged.connect(self.on_pattern_input_p3_changed)

    def on_pattern_changed(self, index):
        # Update explanation
        self.view.set_explanation(self.model.get_explanation(index))

        # Update input widget based on pattern type
        if index in [0, 1, 2, 3, 4]:  # Patterns requiring only P
            self.view.set_input_widget(0)
            self.view.set_focus(0)
        elif index in [8, 9, 10, 11, 12]:  # Patterns requiring only N
            self.view.set_input_widget(1)
            self.view.set_focus(1)
        elif index in [13, 14, 15]:  # Patterns requiring both P and N
            self.view.set_input_widget(2)
            self.view.set_focus(2)
        else:  # Patterns requiring multiple patterns (5, 6, 7)
            self.view.set_input_widget(3)
            self.view.set_focus(3)

    def on_pattern_input_changed(self, text):
        validated = self.model.validate_pattern(text)
        if validated != text:
            self.view.set_pattern_input(validated)

    def on_pattern_input2_changed(self, text):
        validated = self.model.validate_pattern(text)
        if validated != text:
            self.view.set_pattern_input2(validated)

    def on_pattern_input_p1_changed(self, text):
        validated = self.model.validate_pattern(text)
        if validated != text:
            self.view.set_pattern_input_p1(validated)

    def on_pattern_input_p2_changed(self, text):
        validated = self.model.validate_pattern(text)
        if validated != text:
            self.view.set_pattern_input_p2(validated)

    def on_pattern_input_p3_changed(self, text):
        validated = self.model.validate_pattern(text)
        if validated != text:
            self.view.set_pattern_input_p3(validated)

    def on_generate_clicked(self):
        pattern_index = self.view.get_current_pattern_index()
        strategy = self.model.get_strategy(pattern_index)

        if not strategy:
            QMessageBox.warning(self.view, 'Error', 'No strategy found for this pattern.')
            return

        # Get inputs based on pattern type
        if pattern_index in [0, 1, 2, 3, 4]:  # Patterns requiring only P
            pattern = self.view.get_pattern_input()
            if not pattern:
                QMessageBox.warning(self.view, 'Input Error', 'Please enter a pattern first.')
                return

            regex = strategy.generate_regex(pattern)
            desc = strategy.get_description(pattern)

        elif pattern_index in [8, 9, 10, 11, 12]:  # Patterns requiring only N
            N = self.view.get_number_input()
            regex = strategy.generate_regex(N)
            desc = strategy.get_description(N)

        elif pattern_index in [13, 14, 15]:  # Patterns requiring both P and N
            pattern = self.view.get_pattern_input2()
            N = self.view.get_number_input2()
            if not pattern:
                QMessageBox.warning(self.view, 'Input Error', 'Please enter a pattern first.')
                return

            regex = strategy.generate_regex(pattern, N)
            desc = strategy.get_description(pattern, N)

        else:  # Patterns requiring multiple patterns (5, 6, 7)
            p1 = self.view.get_pattern_input_p1()
            p2 = self.view.get_pattern_input_p2()
            p3 = self.view.get_pattern_input_p3()

            if not p1 or not p2:
                QMessageBox.warning(self.view, 'Input Error', 'Please enter at least two patterns.')
                return

            # For patterns 5-7, we only use the first pattern
            regex = strategy.generate_regex(p1)
            desc = strategy.get_description(p1)

        # Display the result
        pattern_type = self.model.get_patterns()[pattern_index]
        result_text = f"""
        <h3>Generated Regular Expression</h3>
        <p>For <b>{pattern_type}</b></p>
        <p>The regular expression is:</p>
        <div style="background-color: #f0f0f0; padding: 15px; border-radius: 5px; font-family: monospace; font-size: 16px;">
            {regex}
        </div>
        <p style="margin-top: 15px;">This regular expression will match any string that {desc}.</p>
        """

        self.view.set_results(result_text)

    def on_clear_clicked(self):
        self.view.clear_inputs()

        # Set focus to the appropriate input based on current pattern
        pattern_index = self.view.get_current_pattern_index()
        if pattern_index in [0, 1, 2, 3, 4]:
            self.view.set_focus(0)
        elif pattern_index in [8, 9, 10, 11, 12]:
            self.view.set_focus(1)
        elif pattern_index in [13, 14, 15]:
            self.view.set_focus(2)
        else:
            self.view.set_focus(3)