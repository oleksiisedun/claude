#!/usr/bin/env bash
# Claude Code status line: model, effort level, session (5h) usage bar, context usage bar.
# Usage: configured as statusLine.command in settings.json; reads session JSON on stdin.
set -euo pipefail

readonly BAR_WIDTH=10
readonly WARN_PCT=50
readonly CRIT_PCT=80
readonly GREEN=$'\e[32m' YELLOW=$'\e[33m' RED=$'\e[31m' DIM=$'\e[2m' RESET=$'\e[0m'

# Print "<label> <colored bar> <pct>%" for an integer 0-100 percentage, or "<label> --" if empty.
progress_bar() {
  local label=$1 raw=$2
  if [[ -z "$raw" ]]; then
    printf '%s %s--%s' "$label" "$DIM" "$RESET"
    return
  fi
  local pct=$raw filled color bar=""
  ((pct > 100)) && pct=100
  filled=$((pct * BAR_WIDTH / 100))
  if ((pct >= CRIT_PCT)); then
    color=$RED
  elif ((pct >= WARN_PCT)); then
    color=$YELLOW
  else
    color=$GREEN
  fi
  for ((i = 0; i < BAR_WIDTH; i++)); do
    if ((i < filled)); then bar+="█"; else bar+="░"; fi
  done
  printf '%s %s%s%s %d%%' "$label" "$color" "$bar" "$RESET" "$pct"
}

input=$(cat)
IFS=$'\t' read -r model effort session_pct ctx_pct < <(
  printf '%s' "$input" | jq -r '[
    .model.display_name // "?",
    .effort.level // "-",
    (.rate_limits.five_hour.used_percentage // null | if . == null then "" else round | tostring end),
    (.context_window.used_percentage // null | if . == null then "" else round | tostring end)
  ] | @tsv'
)

printf '%s %s| effort %s |%s %s %s|%s %s' \
  "$model" "$DIM" "$effort" "$RESET" \
  "$(progress_bar session "$session_pct")" \
  "$DIM" "$RESET" \
  "$(progress_bar ctx "$ctx_pct")"
