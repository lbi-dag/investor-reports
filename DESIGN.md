---
name: Investor Reports
description: An analytical observatory for evidence-based public-company research.
colors:
  observatory-blue: "#1f3a8a"
  observatory-blue-deep: "#172e70"
  midnight: "#1e1b4b"
  ink: "#111827"
  body-ink: "#374151"
  muted-ink: "#6b7280"
  canvas: "#f4f6f9"
  surface: "#ffffff"
  surface-muted: "#f8fafc"
  divider: "#e5e7eb"
  focus-amber: "#f59e0b"
  success-bg: "#dcfce7"
  success-ink: "#166534"
typography:
  headline:
    fontFamily: "Segoe UI, Arial, sans-serif"
    fontSize: "32px"
    fontWeight: 700
    lineHeight: 1.2
  title:
    fontFamily: "Segoe UI, Arial, sans-serif"
    fontSize: "19px"
    fontWeight: 700
    lineHeight: 1.3
  body:
    fontFamily: "Segoe UI, Arial, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.55
  label:
    fontFamily: "Segoe UI, Arial, sans-serif"
    fontSize: "12px"
    fontWeight: 600
    lineHeight: 1.3
rounded:
  action: "7px"
  inset: "9px"
  surface: "12px"
  feature: "14px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "14px"
  lg: "20px"
  xl: "30px"
  page: "40px"
components:
  button-primary:
    backgroundColor: "{colors.observatory-blue}"
    textColor: "{colors.surface}"
    rounded: "{rounded.action}"
    padding: "8px 15px"
  button-primary-hover:
    backgroundColor: "{colors.observatory-blue-deep}"
    textColor: "{colors.surface}"
  status-analyzed:
    backgroundColor: "{colors.success-bg}"
    textColor: "{colors.success-ink}"
    rounded: "20px"
    padding: "4px 10px"
  card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.surface}"
    padding: "20px"
---

# Design System: Investor Reports

## 1. Overview

**Creative North Star: "The Analytical Observatory"**

Investor Reports should feel like a calm instrument for seeing relationships
that individual company filings obscure. The interface is structured, precise,
and readable at a glance. It uses hierarchy and alignment to help readers move
from sector overview to company evidence without mistaking visual emphasis for
investment significance.

The current blue, white, and cool-neutral system is the starting vocabulary.
Future work should reduce decorative gradients, wide ambient shadows, colored
side stripes, and repeated metric-card layouts. The product must not resemble a
promotional corporate investor-relations site, a generic SaaS dashboard, or a
noisy trading terminal.

**Key Characteristics:**

- Restrained blue accent used for navigation, actions, and meaningful state.
- High-information layouts with deliberate whitespace and strong alignment.
- Compact, familiar controls that disappear into the research task.
- Conclusions and comparison signals placed before supporting detail.
- Consistent responsive behavior across directory, company, and report pages.

## 2. Colors

The palette is a cool analytical blue anchored by neutral surfaces and dark,
high-contrast text.

### Primary

- **Observatory Blue** (`#1f3a8a`): Primary actions, active navigation, and
  selective analytical emphasis.
- **Deep Observatory Blue** (`#172e70`): Hover and active states.

### Secondary

- **Midnight** (`#1e1b4b`): Existing deep header tone. Use sparingly and avoid
  decorative blue-to-purple gradients.
- **Focus Amber** (`#f59e0b`): Keyboard focus only, where its contrast makes
  interaction state unmistakable.

### Neutral

- **Ink** (`#111827`): Headings, periods, and high-priority figures.
- **Body Ink** (`#374151`): Explanatory text and report briefs.
- **Muted Ink** (`#6b7280`): Metadata and secondary labels, never essential
  body copy on low-contrast surfaces.
- **Canvas** (`#f4f6f9`): Page background.
- **Surface** (`#ffffff`): Primary content surface.
- **Muted Surface** (`#f8fafc`): Table headers, logo stages, and grouped context.
- **Divider** (`#e5e7eb`): Structural separation.
- **Analyzed Green** (`#dcfce7` / `#166534`): Completed-analysis status only.

**The Signal Rule.** Observatory Blue marks action, selection, or meaningful
analytical emphasis. It is not general decoration.

## 3. Typography

**Display Font:** Segoe UI (with Arial and sans-serif fallbacks)  
**Body Font:** Segoe UI (with Arial and sans-serif fallbacks)  
**Label/Mono Font:** Segoe UI for labels; use the system monospace stack only
when presenting source hashes or code-like metadata.

**Character:** One familiar system sans keeps attention on evidence. Hierarchy
comes from weight, size, spacing, and placement rather than a decorative font
pairing.

### Hierarchy

- **Headline** (700, `32px`, `1.2`): Page and company identity.
- **Title** (700, `19px`, `1.3`): Section headings and major company labels.
- **Feature Brief** (650, `18px`, `1.4`): Latest-analysis conclusion.
- **Body** (400, `16px`, `1.55`): Explanatory prose, capped near `70ch`.
- **Data Body** (400-700, `14px`, `1.45`): Tables, archives, and comparison
  summaries.
- **Label** (600-700, `11px` to `12px`, restrained uppercase only): Status,
  short metadata, and compact column labels.

**The Evidence Hierarchy Rule.** A conclusion may be larger than its supporting
details, but a decorative heading must never overpower the conclusion.

## 4. Elevation

The system is structurally layered, not softly floating. Use background tone,
dividers, and spacing before shadows. Existing wide ambient shadows should be
reduced during redesign work; shadows are reserved for a featured surface or a
clear interactive elevation change.

### Shadow Vocabulary

- **Low Structural Lift** (`0 3px 8px rgba(15, 23, 42, .08)`): Maximum resting
  elevation for a featured surface when a divider is insufficient.
- **Interactive Lift** (`0 4px 8px rgba(15, 23, 42, .12)`): Hover state for an
  element that physically lifts by no more than `1px`.

**The Flat-by-Default Rule.** Most surfaces rest on the canvas without a
shadow. Depth must communicate grouping or interaction, not polish for its own
sake.

## 5. Components

Components are compact, familiar, and consistent. Every interactive element
needs a visible hover and keyboard-focus state.

### Buttons

- **Shape:** Compact rounded rectangle (`7px`), never a large pill.
- **Primary:** Observatory Blue with white text and `8px 15px` padding.
- **Hover / Focus:** Deep Observatory Blue on hover; `3px` Focus Amber outline
  with `3px` offset for keyboard focus.
- **Secondary:** Transparent or neutral surface with a clear structural border.

### Chips

- **Style:** Full pills are reserved for short status values such as Analyzed
  and Pending.
- **State:** Color communicates a defined status, not generic decoration.

### Cards / Containers

- **Corner Style:** `12px` for standard surfaces, up to `14px` for a single
  featured analysis surface.
- **Background:** Surface or Muted Surface, selected by hierarchy.
- **Shadow Strategy:** Flat by default; use Low Structural Lift selectively.
- **Border:** Full `1px` divider where separation is needed. Never use a thick
  colored side stripe.
- **Internal Padding:** `20px` standard, `26px` to `28px` only for a featured
  analysis surface.

### Inputs / Fields

- **Style:** Use native, familiar controls with Surface background, Divider
  stroke, and `7px` radius.
- **Focus:** Use the same Focus Amber outline as links and buttons.
- **Error / Disabled:** Preserve readable contrast and communicate state with
  text, not color alone.

### Navigation

Navigation is quiet and descriptive. Link labels state the destination, active
state uses Observatory Blue, and mobile layouts preserve the same information
architecture rather than hiding essential routes.

### Report Archive

Desktop archives use compact tables with strong column alignment and subtle row
hover. Mobile archives become stacked report entries with the period, status,
brief, and action kept in a predictable reading order.

## 6. Do's and Don'ts

### Do:

- **Do** lead with the latest conclusion and make source-backed detail easy to
  reach.
- **Do** use Observatory Blue for actions, active state, and meaningful signal.
- **Do** use full dividers, background tones, and alignment to establish
  structure.
- **Do** keep company and period comparisons visually consistent.
- **Do** preserve readable contrast, visible focus, semantic HTML, and usable
  narrow-screen layouts.

### Don't:

- **Don't** resemble promotional corporate investor-relations sites that
  prioritize brand imagery or management messaging over evidence.
- **Don't** resemble generic SaaS dashboards built from interchangeable metric
  cards, excessive gradients, decorative icons, and inflated marketing copy.
- **Don't** resemble trading terminals that create density without clarifying
  signal.
- **Don't** use thick colored side stripes on cards or callouts.
- **Don't** pair a full border with a wide decorative shadow.
- **Don't** use blue-to-purple gradients as a default header treatment.
- **Don't** add motion unless it communicates interaction or state, and always
  provide reduced-motion handling.
