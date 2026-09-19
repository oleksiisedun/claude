# CSS design system (front-end repos only)

When starting any new project with HTML/CSS, or touching a stylesheet for the first time, define shared primitives **before** writing one-off component rules. Retrofitting this after a stylesheet has grown (duplicated button/overlay rules, 2-3 near-identical accent colors) is real cleanup work — avoid the rework by setting it up from commit one.

**Tokens first**: declare `:root` CSS variables for every recurring value before styling components — colors (primary/accent, focus ring, danger, neutral border, at minimum) and a radius scale (usually one value is enough for small projects). Never hardcode a hex value that represents "the accent color" or "the danger color" — reference the variable. If a genuinely new semantic color is needed, add a new `--color-*` variable rather than inlining a hex value next to an existing similar one.

**Shared classes for repeated patterns**: the moment a button, overlay/modal, or input style is used twice, give it a class (`.btn-primary`, `.btn-secondary`, `.overlay`, etc.) instead of duplicating the rule block under a new ID or element selector. ID/element selectors should only carry what's *different* from the shared class (padding, size, position) — never re-declare color, border, or radius that the shared class already sets.

**One rule per interaction state**: decide once how disabled buttons, focused inputs, and hovered links look, and apply it with a single broad selector (e.g. `button:disabled { opacity: 0.5; cursor: default; }`, one focus-ring `box-shadow` reused on every text input) rather than repeating the same declaration per component ID.

**Before adding a new rule, check what already exists**: a duplicated rule block under a new ID is the main way a stylesheet drifts out of sync with itself — that's how a codebase ends up with three different "primary blue" hex values because each button was styled independently instead of reusing one.
