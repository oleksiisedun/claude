# data-testid (front-end repos only)

In front-end projects that use `data-testid` attributes:

Use `data-testid` on interactive and key container elements to support automated testing.

**Naming**: always kebab-case, semantic (what the element IS or DOES, not implementation).

**Static IDs** — most common, use a plain string:

```tsx
<button data-testid="confirm-button" />
<div data-testid="cash-out-popup" />
```

**Dynamic labels** — use a `toDataTestid` helper to convert text (spaces → hyphens, lowercase). Import it from `@sportsbook/utils-fe` if the project has that package; otherwise inline this implementation:

```tsx
const toDataTestid = (str: string = '') => (str ?? '').replace(/\s+/g, '-').toLowerCase();

<div data-testid={toDataTestid(name)} />
// Translation key suffix: strip namespace, then convert
<div data-testid={toDataTestid(text.split('::').at(-1))} />
```

**Compound IDs** — append a suffix to a base testid prop for sub-elements:

```tsx
// In a reusable component receiving dataTestid prop:
<div data-testid={dataTestid} />
<span data-testid={`${dataTestid}-label`} />
<ul data-testid={`${dataTestid}-options`} />
```

**State-based IDs** — reflect current state in the ID:

```tsx
<button data-testid={`${isExpanded ? 'collapse' : 'expand'}-button`} />
<div data-testid={`benefits-${isAllowed ? 'general' : 'suspicious'}-user`} />
```

**Tab pattern**:

```tsx
data-testid={`${tab.dataTestid ?? toDataTestid(tab.name)}-tab${isActive ? '-active' : ''}`}
```

**Suffix conventions**:

- Buttons: `-button` (e.g. `confirm-button`, `edit-button`)
- Links: `-link` (handled by `Link` component via `dataTestid` prop)
- Tabs: `-tab`, `-tab-active`
- Containers: no suffix (e.g. `betslip-tooltip`, `user-block`)
- Child elements: `{base}-{role}` (e.g. `slider-thumb`, `slider-min-value`)

**Prop name**: use `dataTestid` (camelCase) when passing as a component prop.
