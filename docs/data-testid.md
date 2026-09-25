# data-testid (front-end repos only)

In front-end projects that use `data-testid` attributes, put them on interactive and key container elements to support automated testing.

**Naming**: always kebab-case, semantic (what the element IS or DOES, not implementation).

**Static IDs** — most common, use a plain string:

```tsx
<button data-testid="confirm-button" />
<div data-testid="checkout-popup" />
```

**Dynamic labels** — convert text with a helper (spaces → hyphens, lowercase). If the project already has one (search for `toDataTestid` or similar, including shared utility packages), use it; otherwise add this implementation once in the project's utils:

```tsx
const toDataTestid = (str?: string | null) => (str ?? '').replace(/\s+/g, '-').toLowerCase();

<div data-testid={toDataTestid(name)} />
// Namespaced translation key: strip the namespace, then convert
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
<div data-testid={`account-${isVerified ? 'verified' : 'unverified'}-banner`} />
```

**Tab pattern**:

```tsx
data-testid={`${tab.dataTestid ?? toDataTestid(tab.name)}-tab${isActive ? '-active' : ''}`}
```

**Suffix conventions**:

- Buttons: `-button` (e.g. `confirm-button`, `edit-button`)
- Links: `-link` (if the project has a shared link component, pass the ID via its `dataTestid` prop and let it add the suffix)
- Tabs: `-tab`, `-tab-active`
- Containers: no suffix (e.g. `cart-tooltip`, `user-block`)
- Child elements: `{base}-{role}` (e.g. `slider-thumb`, `slider-min-value`)

**Prop name**: use `dataTestid` (camelCase) when passing as a component prop.
