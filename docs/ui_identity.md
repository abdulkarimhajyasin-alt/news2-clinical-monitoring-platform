# UI Identity

The UI is Arabic-first and RTL by default. Future English support should be implemented through a translation layer and direction-aware layout rules.

The visual identity uses a medical blue palette:

- Primary: `#0B5CAD`
- Secondary: `#0EA5E9`
- Success: `#22C55E`
- Warning: `#F59E0B`
- Danger: `#DC2626`
- Background: `#F8FAFC`
- Cards: `#FFFFFF`

The interface uses white clinical cards, soft shadows, compact information density, sidebar navigation, KPI cards, NEWS2 risk colors, alert severity badges, and subtle medical animations.

NEWS2 colors should map to operational risk:

- Low: green/success
- Medium: amber/warning
- High: red/danger
- Critical: red with restrained pulse animation

Accessibility direction:

- Preserve semantic HTML where possible.
- Keep RTL alignment consistent.
- Add accessible labels for icon controls.
- Ensure color is not the only risk indicator.
- Respect reduced motion preferences in later UI hardening.
