"""Implementation of Rule L001."""
from typing import Tuple

from sqlfluff.core.parser.segments import BaseSegment, RawSegment
from sqlfluff.core.rules.base import BaseRule, LintResult, LintFix
from sqlfluff.core.rules.doc_decorators import document_fix_compatible
from sqlfluff.core.templaters import TemplatedFile


@document_fix_compatible
class Rule_L001(BaseRule):
    """Unnecessary trailing whitespace.

    | **Anti-pattern**
    | The • character represents a space.

    .. code-block:: sql
       :force:

        SELECT
            a
        FROM foo••

    | **Best practice**
    | Remove trailing spaces.

    .. code-block:: sql

        SELECT
            a
        FROM foo
    """

    def _eval(  # type: ignore
        self,
        segment: BaseSegment,
        raw_stack: Tuple[RawSegment, ...],
        templated_file: TemplatedFile,
        **kwargs
    ) -> LintResult:
        """Unnecessary trailing whitespace.

        Look for newline segments, and then evaluate what
        it was preceded by.
        """
        # We only trigger on newlines
        if (
            segment.is_type("newline")
            and len(raw_stack) > 0
            and raw_stack[-1].is_type("whitespace")
        ):
            # If we find a newline, which is preceded by whitespace, then bad
            deletions = []
            idx = -1
            while abs(idx) <= len(raw_stack) and raw_stack[idx].is_type("whitespace"):
                deletions.append(raw_stack[idx])
                idx -= 1
            last_deletion_slice = deletions[-1].pos_marker.source_slice

            # Check the raw source (before template expansion) immediately
            # following the whitespace we want to delete. Often, what looks
            # like trailing whitespace in rendered SQL is actually a line like:
            # "    {% for elem in elements %}\n", in which case the code is
            # fine -- it's not trailing whitespace from a source code
            # perspective.
            next_raw_slice = templated_file.raw_slices_spanning_source_slice(
                slice(last_deletion_slice.stop, last_deletion_slice.stop)
            )
            # If the next slice is literal, that means it's regular code, so
            # it's safe to delete the trailing whitespace. If it's anything
            # else, it's template code, so don't delete the whitespace because
            # it's not REALLY trailing whitespace in terms of the raw source
            # code.
            if next_raw_slice[0].slice_type == "literal":
                return LintResult(
                    anchor=deletions[-1],
                    fixes=[LintFix("delete", d) for d in deletions],
                )
        return LintResult()
