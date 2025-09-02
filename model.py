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
        # For simple patterns, we can construct a proper regular expression
        # For complex patterns, this becomes much more difficult

        if len(pattern) == 1:
            # For single character patterns like "a" or "b"
            other_char = 'b' if pattern == 'a' else 'a'
            return f"({other_char})*"

        elif pattern == "aa":
            # Strings with no consecutive a's: b*(ab*)*
            return f"((b)* • ((a) • (b)*))*"

        elif pattern == "bb":
            # Strings with no consecutive b's: a*(ba*)*
            return f"((a)* • ((b) • (a)*))*"

        elif pattern == "ab":
            # Strings that don't contain "ab"
            # This would be strings of all a's followed by all b's, but not mixed
            return f"(a)* + (b)*"

        elif pattern == "ba":
            # Strings that don't contain "ba"
            # This would be strings of all b's followed by all a's, but not mixed
            return f"(b)* + (a)*"

        else:
            # For more complex patterns, we cannot easily express "does not contain P"
            # as a simple regular expression using the basic operations
            # This would typically require complementation, which is not a primitive operation
            # in the definition of regular expressions
            raise ValueError(f"Cannot generate a regular expression for 'does not contain {pattern}' " +
                             "using only the basic operations (•, +, *)")

    def get_description(self, pattern):
        if len(pattern) == 1:
            return f"does not contain '{pattern}'"
        elif pattern == "aa":
            return "does not contain 'aa' (no consecutive a's)"
        elif pattern == "bb":
            return "does not contain 'bb' (no consecutive b's)"
        elif pattern == "ab":
            return "does not contain 'ab' (all a's followed by all b's, or only a's, or only b's)"
        elif pattern == "ba":
            return "does not contain 'ba' (all b's followed by all a's, or only a's, or only b's)"
        else:
            return f"does not contain '{pattern}' (complex pattern - no simple regex available)"


class LengthGreaterThanStrategy(RegexStrategy):
    def generate_regex(self, N):
        return f"(a+b)^{{{N + 1}}}(a+b)*"

    def get_description(self, N):
        return f"has length greater than {N}"


class LengthLessThanStrategy(RegexStrategy):
    def generate_regex(self, N):
        if N <= 0:
            return "∅"  # No strings have length less than 0

        # Create union of all lengths from 0 to N-1 using formal syntax
        parts = ["ε"]  # Empty string

        # For each length from 1 to N-1, create the formal expression
        for i in range(1, N):
            # For strings of length i: all combinations of a and b of length i
            # This is equivalent to (a+b) concatenated i times

            if i == 1:
                part = "((a)+(b))"
            else:
                # Build (a+b) • (a+b) • ... • (a+b) (i times)
                part = "((a)+(b))"
                for _ in range(1, i):
                    part = f"{part}•((a)+(b))"

            parts.append(part)

        # Join all parts with union operator +
        if len(parts) == 1:
            return parts[0]
        else:
            return " + ".join(f"({part})" for part in parts)

    def get_description(self, N):
        return f"has length less than {N}"


class LengthGreaterThanOrEqualStrategy(RegexStrategy):
    def generate_regex(self, N):
        return f"(a+b)^{{{N}}}(a+b)*"

    def get_description(self, N):
        return f"has length greater than or equal to {N}"


class LengthLessThanOrEqualStrategy(RegexStrategy):
    def generate_regex(self, N):
        if N < 0:
            return "∅"  # No strings have length less than or equal to a negative number

        # Create union of all lengths from 0 to N using formal syntax
        parts = ["ε"]  # Empty string

        # For each length from 1 to N, create the formal expression
        for i in range(1, N + 1):
            # For strings of length i: all combinations of a and b of length i
            # This is equivalent to (a+b) concatenated i times

            if i == 1:
                part = "((a)+(b))"
            else:
                # Build (a+b) • (a+b) • ... • (a+b) (i times)
                part = "((a)+(b))"
                for _ in range(1, i):
                    part = f"{part}•((a)+(b))"

            parts.append(part)

        # Join all parts with union operator +
        if len(parts) == 1:
            return parts[0]
        else:
            return " + ".join(f"({part})" for part in parts)

    def get_description(self, N):
        return f"has length less than or equal to {N}"


class LengthEqualStrategy(RegexStrategy):
    def generate_regex(self, N):
        return f"(a+b)^{{{N}}}"

    def get_description(self, N):
        return f"has length exactly {N}"


class CountDivisibleByStrategy(RegexStrategy):
    def generate_regex(self, pattern, N):
        if N <= 0:
            return "∅"  # Divisible by 0 or negative numbers is undefined

        # For the general case, generating a regular expression for
        # "number of occurrences of P is divisible by N" is complex
        # and requires building a finite automaton with N states

        # We can only handle very simple cases directly
        if pattern in ["a", "b"] and N == 1:
            # Any number of the pattern (divisible by 1)
            other_char = "b" if pattern == "a" else "a"
            return f"(({other_char})*•({pattern})•({other_char})*)*"

        elif pattern in ["a", "b"] and N == 2:
            # Even number of the pattern
            other_char = "b" if pattern == "a" else "a"
            return f"(({other_char})*•({pattern})•({other_char})*•({pattern})•({other_char})*)*"

        else:
            # For more complex cases, we cannot easily express this
            # as a simple regular expression using basic operations
            raise ValueError(f"Cannot generate a regular expression for 'count of {pattern} divisible by {N}' " +
                             "using only the basic operations (•, +, *). " +
                             "This would require building a finite automaton with {N} states.")

    def get_description(self, pattern, N):
        if N == 1:
            return f"has any number of '{pattern}' (count divisible by 1)"
        else:
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
        # Convert the pattern to proper regular expression syntax
        if len(pattern) == 0:
            return "∅"  # Empty pattern case

        # Convert each character in the pattern to the formal representation
        pattern_expr = f"({pattern[0]})"
        for char in pattern[1:]:
            pattern_expr = f"{pattern_expr}•({char})"

        # For strings that start with P and contain P
        # Since it starts with P, it automatically contains P
        # So we just need: P • (any combination of a and b)*

        # Represent (a+b)* in formal syntax as ((a)+(b))*
        any_string = "((a)+(b))*"

        # Return the complete formal regular expression
        return f"{pattern_expr}•{any_string}"

    def get_description(self, pattern):
        return f"contains '{pattern}' and starts with '{pattern}' (starting with P implies containing P)"


class ContainsAndEndsWithStrategy(RegexStrategy):
    def generate_regex(self, pattern):
        # Convert the pattern to proper regular expression syntax
        if len(pattern) == 0:
            return "∅"  # Empty pattern case

        # Convert each character in the pattern to the formal representation
        pattern_expr = f"({pattern[0]})"
        for char in pattern[1:]:
            pattern_expr = f"{pattern_expr}•({char})"

        # For strings that end with P and contain P
        # Since it ends with P, it automatically contains P
        # So we just need: (any combination of a and b)* • P

        # Represent (a+b)* in formal syntax as ((a)+(b))*
        any_string = "((a)+(b))*"

        # Return the complete formal regular expression
        return f"{any_string}•{pattern_expr}"

    def get_description(self, pattern):
        return f"contains '{pattern}' and ends with '{pattern}' (ending with P implies containing P)"


class ContainsStartsAndEndsWithStrategy(RegexStrategy):
    def generate_regex(self, pattern):
        # For strings that:
        # 1. Start with the first character of P
        # 2. End with the last character of P
        # 3. Contain the full pattern P somewhere

        if len(pattern) == 0:
            return "∅"  # Empty pattern case

        # Convert the full pattern to formal syntax
        full_pattern_expr = f"({pattern[0]})"
        for char in pattern[1:]:
            full_pattern_expr = f"{full_pattern_expr}•({char})"

        # Get the first and last characters
        start_char = pattern[0]
        end_char = pattern[-1]

        # Represent (a+b)* in formal syntax as ((a)+(b))*
        any_string = "((a)+(b))*"

        # The regular expression is:
        # start_char • (any_string) • full_pattern • (any_string) • end_char
        return f"({start_char})•{any_string}•{full_pattern_expr}•{any_string}•({end_char})"

    def get_description(self, pattern):
        if len(pattern) == 0:
            return "empty pattern"
        elif len(pattern) == 1:
            return f"contains '{pattern}', starts with '{pattern}', and ends with '{pattern}'"
        else:
            return f"contains '{pattern}', starts with '{pattern[0]}', and ends with '{pattern[-1]}'"


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