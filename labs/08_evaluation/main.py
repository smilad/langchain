"""Print/write actual per-case reports; held-out review requires frozen development config."""
from pathlib import Path
import json

from langchain_learning.evaluation import (apply_human_reviews, enforce_frozen_config, evaluate,
                                          experiment_config, load_cases, load_reviews)
from langchain_learning.runtime import emit, lab_parser, preflight, run_lab


def main():
    parser = lab_parser(__doc__)
    parser.add_argument("--split", choices=["dev", "held_out"], default="dev")
    parser.add_argument("--strategy", choices=["lexical", "semantic", "hybrid"], default="lexical")
    parser.add_argument("--compare-strategy", choices=["lexical", "semantic", "hybrid"])
    parser.add_argument("--k", type=int, default=3)
    parser.add_argument("--trials", type=int, default=1)
    parser.add_argument("--judge", action="store_true", help="Paid fallible model grader, separate from human support review")
    parser.add_argument("--freeze-config", type=Path)
    parser.add_argument("--config", type=Path)
    parser.add_argument("--human-review", type=Path, help="JSON list of case_id,strategy,trial,reviewer,grade; requires --review-report")
    parser.add_argument("--review-report", type=Path, help="Annotate this saved report offline; never regenerate reviewed answers")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    emit({"preflight": preflight()})
    if args.human_review and not args.review_report:
        raise ValueError("Use --review-report with --human-review to grade saved outputs, not a new generation")
    if args.review_report:
        if not args.human_review or args.live or args.judge or args.config or args.freeze_config:
            raise ValueError("Saved-report review requires --human-review and no live/judge/config/freeze flags")
        report = apply_human_reviews(json.loads(args.review_report.read_text()), load_reviews(args.human_review))
    else:
        load_cases()  # validates exact category/split distribution and frozen bytes
        config = experiment_config(strategy=args.strategy, k=args.k, trials=args.trials,
                                   compare_strategy=args.compare_strategy, live=args.live, judge=args.judge)
        enforce_frozen_config(config, split=args.split, path=args.config, freeze=args.freeze_config)
        report = evaluate(split=args.split, strategy=args.strategy, k=args.k, trials=args.trials,
                          live=args.live, judge=args.judge, compare_strategy=args.compare_strategy)
        report["configuration"] = config
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x") as stream:
            json.dump(report, stream, indent=2)
    emit(report)
    if any("error_type" in row for row in report["cases"]):
        raise ValueError("Some evaluation cases failed execution; inspect per-case error types in the report")


if __name__ == "__main__":
    run_lab(main)
