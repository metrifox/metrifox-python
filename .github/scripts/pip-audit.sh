#!/usr/bin/env bash
# Auto-discovers every requirements*.txt in the repo and audits each with
# pip-audit. Shipped paths block the PR; test/dev/example/blind-spot paths are
# report-only. Writes pip-audit's native markdown findings table to the PR
# check's Summary page (Name / Version / Advisory ID / Fix Versions).
#
# Kept in a script file (not inline) so the Actions log stays clean — the
# workflow step only echoes "bash .github/scripts/pip-audit.sh".
set -uo pipefail

shipped_failed=0
printf '## 🔒 pip-audit\n\n' >> "$GITHUB_STEP_SUMMARY"
while IFS= read -r req; do
  # Classify: test/dev/example/blind-spot path or filename => report-only.
  case "$req" in
    *demo*|*example*|*e2e*|*fixture*|*sample*|*test*|*spec*|*dev*) mode=report-only ;;
    *) mode=blocking ;;
  esac
  # pip-audit exits 0 when clean, non-zero when advisories are found.
  if md=$(pip-audit -r "$req" -f markdown 2>/dev/null); then
    printf -- '- ✅ `%s` — no known advisories\n' "$req" >> "$GITHUB_STEP_SUMMARY"
    continue
  fi
  if [ "$mode" = blocking ]; then badge='🔴 blocking'; shipped_failed=1; else badge='🟡 report-only'; fi
  # Findings table -> PR check Summary page.
  {
    printf '\n### `%s` — %s\n\n' "$req" "$badge"
    printf '%s\n' "$md"
  } >> "$GITHUB_STEP_SUMMARY"
  # Same findings -> step log (so they're visible inline, not only the Summary).
  printf -- '── %s — %s findings ──\n' "$req" "$mode"
  printf '%s\n' "$md"
  if [ "$mode" = blocking ]; then
    printf '::error::vulnerable dependency in shipped requirements: %s\n' "$req"
  else
    printf '::warning::vulnerable dependency in report-only requirements: %s (not blocking)\n' "$req"
  fi
done < <(find . -name 'requirements*.txt' -not -path '*/.git/*' | sort)
if [ "$shipped_failed" = 1 ]; then
  printf '\n> ❌ **Fix the 🔴 blocking requirements above** (apply the "Fix Versions" column) before this PR can merge.\n' >> "$GITHUB_STEP_SUMMARY"
fi
exit $shipped_failed
