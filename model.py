from abc import ABC, abstractmethod
import re


class RegexStrategy(ABC):
    """Abstract base class for regex generation strategies"""

    @abstractmethod
    def generate_regex(self, *args):
        pass

    @abstractmethod
    def get_description(self, *args):
        pass


class StartsWithStrategy(RegexStrategy):
    def generate_regex(self, pattern):
        return f"{pattern}(a+b)*"

    def get_description(self, pattern):
        return f"starts with '{pattern}'"


class EndsWithStrategy(RegexStrategy):
    def generate_regex(self, pattern):
        return f"(a+b)*{pattern}"

    def get_description(self, pattern):
        return f"ends with '{pattern}'"


class StartsAndEndsWithStrategy(RegexStrategy):
    def generate_regex(self, pattern):
        return f"{pattern}(a+b)*{pattern}"

    def get_description(self, pattern):
        return f"starts and ends with '{pattern}'"


class ContainsStrategy(RegexStrategy):
    def generate_regex(self, pattern):
        return f"(a+b)*{pattern}(a+b)*"

    def get_description(self, pattern):
        return f"contains '{pattern}'"


class DoesNotContainStrategy(RegexStrategy):
    def generate_regex(self, pattern):
        if pattern == "aa":
            return "b*(ab*)*"
        elif pattern == "bb":
            return "a*(ba*)*"
        else:
            return f"(a+b)* without '{pattern}'"

    def get_description(self, pattern):
        if pattern == "aa":
            return "does not contain 'aa' (no consecutive a's)"
        elif pattern == "bb":
            return "does not contain 'bb' (no consecutive b's)"
        else:
            return f"does not contain '{pattern}'"


class LengthGreaterThanStrategy(RegexStrategy):
    def generate_regex(self, N):
        return f"(a+b)^{{{N + 1}}}(a+b)*"

    def get_description(self, N):
        return f"has length greater than {N}"


class LengthLessThanStrategy(RegexStrategy):
    def generate_regex(self, N):
        # Create union of all lengths from 0 to N-1
        parts = ["ε"] + [f"(a+b)^{{{i}}}" for i in range(1, N)]
        return " + ".join(parts)

    def get_description(self, N):
        return f"has length less than {N}"


class LengthGreaterThanOrEqualStrategy(RegexStrategy):
    def generate_regex(self, N):
        return f"(a+b)^{{{N}}}(a+b)*"

    def get_description(self, N):
        return f"has length greater than or equal to {N}"


class LengthLessThanOrEqualStrategy(RegexStrategy):
    def generate_regex(self, N):
        # Create union of all lengths from 0 to N
        parts = ["ε"] + [f"(a+b)^{{{i}}}" for i in range(1, N + 1)]
        return " + ".join(parts)

    def get_description(self, N):
        return f"has length less than or equal to {N}"


class LengthEqualStrategy(RegexStrategy):
    def generate_regex(self, N):
        return f"(a+b)^{{{N}}}"

    def get_description(self, N):
        return f"has length exactly {N}"


class CountDivisibleByStrategy(RegexStrategy):
    def generate_regex(self, pattern, N):
        # This is complex - simplified representation
        return f"( (a+b)*{pattern}(a+b)* ) where count of '{pattern}' is divisible by {N}"

    def get_description(self, pattern, N):
        return f"has count of '{pattern}' divisible by {N}"


class NthSymbolIsStrategy(RegexStrategy):
    def generate_regex(self, pattern, N):
        if N == 1:
            return f"{pattern}(a+b)*"
        else:
            return f"(a+b)^{{{N - 1}}}{pattern}(a+b)*"

    def get_description(self, pattern, N):
        return f"has the {N}th symbol as '{pattern}'"


class NthSymbolFromLastIsStrategy(RegexStrategy):
    def generate_regex(self, pattern, N):
        if N == 1:
            return f"(a+b)*{pattern}"
        else:
            return f"(a+b)*{pattern}(a+b)^{{{N - 1}}}"

    def get_description(self, pattern, N):
        return f"has the {N}th symbol from the last as '{pattern}'"


class ContainsAndStartsWithStrategy(RegexStrategy):
    def generate_regex(self, pattern):
        return f"{pattern}(a+b)*"

    def get_description(self, pattern):
        return f"contains '{pattern}' and starts with '{pattern}'"


class ContainsAndEndsWithStrategy(RegexStrategy):
    def generate_regex(self, pattern):
        return f"(a+b)*{pattern}"

    def get_description(self, pattern):
        return f"contains '{pattern}' and ends with '{pattern}'"


class ContainsStartsAndEndsWithStrategy(RegexStrategy):
    def generate_regex(self, pattern):
        # Use the same logic as starts and ends with P
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
                return f"{pattern}({middle_pattern})*"
            else:
                return f"{pattern}({pattern})*"
        else:
            return f"{pattern}(a+b)*{pattern}"

    def get_description(self, pattern):
        return f"contains '{pattern}', starts with '{pattern}', and ends with '{pattern}'"


class RegexModel:
    def __init__(self):
        self.strategies = {
            0: StartsWithStrategy(),
            1: EndsWithStrategy(),
            2: StartsAndEndsWithStrategy(),
            3: ContainsStrategy(),
            4: DoesNotContainStrategy(),
            5: ContainsAndStartsWithStrategy(),
            6: ContainsAndEndsWithStrategy(),
            7: ContainsStartsAndEndsWithStrategy(),
            8: LengthGreaterThanStrategy(),
            9: LengthLessThanStrategy(),
            10: LengthGreaterThanOrEqualStrategy(),
            11: LengthLessThanOrEqualStrategy(),
            12: LengthEqualStrategy(),
            13: CountDivisibleByStrategy(),
            14: NthSymbolIsStrategy(),
            15: NthSymbolFromLastIsStrategy()
        }

        self.patterns = [
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

        self.explanations = [
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

    def get_patterns(self):
        return self.patterns

    def get_explanation(self, index):
        return self.explanations[index]

    def get_strategy(self, index):
        return self.strategies.get(index)

    def validate_pattern(self, text):
        """Validate that text contains only a and b characters"""
        if text and not all(char in ['a', 'b'] for char in text):
            valid_text = ''.join(char for char in text if char in ['a', 'b'])
            return valid_text
        return text