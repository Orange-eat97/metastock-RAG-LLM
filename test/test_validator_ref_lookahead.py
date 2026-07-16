import unittest

from src.validator import (
    contains_positive_ref,
    extract_ref_calls,
    split_top_level_args,
    validate_explorer_output,
    validate_formula,
    validate_ref_lookahead,
)


class RefLookaheadValidationTests(unittest.TestCase):
    def test_nested_historical_ref_does_not_trigger_lookahead(self) -> None:
        formula = "Ref(HHV(H,20),-1)"

        self.assertFalse(
            contains_positive_ref(formula)
        )
        self.assertEqual(
            validate_ref_lookahead(formula),
            [],
        )
        self.assertEqual(
            validate_formula(formula),
            [],
        )

    def test_nested_moving_average_ref_does_not_trigger_lookahead(
        self,
    ) -> None:
        formula = "Ref(Mov(V,30,S),-1)"

        self.assertFalse(
            contains_positive_ref(formula)
        )
        self.assertEqual(
            validate_formula(formula),
            [],
        )

    def test_positive_direct_ref_is_rejected(self) -> None:
        formula = "Ref(C,1)"

        errors = validate_formula(formula)

        self.assertTrue(
            any(
                "Positive Ref offset 1" in error
                for error in errors
            ),
            errors,
        )

    def test_explicit_positive_direct_ref_is_rejected(
        self,
    ) -> None:
        formula = "Ref(C,+2)"

        errors = validate_formula(formula)

        self.assertTrue(
            any(
                "Positive Ref offset +2" in error
                for error in errors
            ),
            errors,
        )

    def test_positive_nested_expression_ref_is_rejected(
        self,
    ) -> None:
        formula = "Ref(HHV(H,20),2)"

        errors = validate_formula(formula)

        self.assertTrue(
            any(
                "Positive Ref offset 2" in error
                for error in errors
            ),
            errors,
        )

    def test_positive_outer_nested_ref_is_rejected(self) -> None:
        formula = "Ref(Ref(C,-1),1)"

        errors = validate_formula(formula)

        self.assertTrue(
            any(
                "Positive Ref offset 1" in error
                for error in errors
            ),
            errors,
        )

    def test_zero_ref_offset_is_allowed(self) -> None:
        self.assertEqual(
            validate_formula("Ref(C,0)"),
            [],
        )
        self.assertEqual(
            validate_formula("Ref(C,+0)"),
            [],
        )

    def test_negative_ref_offset_is_allowed(self) -> None:
        self.assertEqual(
            validate_formula("Ref(C,-1)"),
            [],
        )
        self.assertEqual(
            validate_formula("Ref(HHV(H,20),-2)"),
            [],
        )

    def test_ref_call_parser_handles_nested_arguments(self) -> None:
        formula = (
            "Ref(C,-1) <= Ref(HHV(H,20),-2) "
            "AND C > Ref(HHV(H,20),-1)"
        )

        calls = extract_ref_calls(formula)

        self.assertEqual(
            calls,
            [
                "C,-1",
                "HHV(H,20),-2",
                "HHV(H,20),-1",
            ],
        )

        self.assertEqual(
            split_top_level_args(
                "HHV(H,20),-2"
            ),
            [
                "HHV(H,20)",
                "-2",
            ],
        )

    def test_invalid_ref_argument_count_is_rejected(
        self,
    ) -> None:
        errors = validate_formula(
            "Ref(C,-1,2)"
        )

        self.assertTrue(
            any(
                "Ref() should have exactly 2 arguments"
                in error
                for error in errors
            ),
            errors,
        )

    def test_confirmed_breakout_explorer_passes(
        self,
    ) -> None:
        explorer = {
            "explorer_name": (
                "AI_Confirmed Breakout Momentum"
            ),
            "explorer_code_body": (
                "Ref(C,-1) <= Ref(HHV(H,20),-2) "
                "AND C > Ref(HHV(H,20),-1) "
                "AND V >= 1.5 * Ref(Mov(V,30,S),-1) "
                "AND RSI(14) > 55 "
                "AND C > Ref(Mov(C,50,S),-1) "
                "AND ATR(14) > "
                "Ref(Mov(ATR(14),20,S),-1)"
            ),
            "col_definitions": [
                {
                    "col_letter": "A",
                    "col_code": "C",
                },
                {
                    "col_letter": "B",
                    "col_code": (
                        "Ref(HHV(H,20),-1)"
                    ),
                },
                {
                    "col_letter": "C",
                    "col_code": (
                        "V / Ref(Mov(V,30,S),-1)"
                    ),
                },
                {
                    "col_letter": "D",
                    "col_code": "RSI(14)",
                },
                {
                    "col_letter": "E",
                    "col_code": (
                        "Ref(Mov(C,50,S),-1)"
                    ),
                },
                {
                    "col_letter": "F",
                    "col_code": (
                        "ATR(14) / "
                        "Ref(Mov(ATR(14),20,S),-1)"
                    ),
                },
            ],
        }

        errors = validate_explorer_output(
            explorer
        )

        self.assertEqual(
            errors,
            [],
        )


if __name__ == "__main__":
    unittest.main()