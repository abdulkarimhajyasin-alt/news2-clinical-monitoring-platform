# UI FIX — HIDE SIDEBAR COMPLETELY WHEN CLOSED

## Objective

Fix the NEWS2 platform sidebar behavior so that when the user closes the menu, the sidebar disappears completely instead of remaining visible as a narrow icon-only rail.

The user explicitly does not want the collapsed icon rail to remain visible.

---

# CURRENT PROBLEM

After the recent navigation simplification, closing the sidebar leaves a narrow dark-blue vertical rail on the right side containing only icon badges such as:

```text
D
P
S
VS
A
E
CO
R
U
```

This is not desired.

Expected behavior:

- When sidebar is closed, it should be fully hidden.
- No icon-only rail should remain visible.
- Main content should expand to full width.
- The top menu button should remain visible so the sidebar can be opened again.
- The internal `×` button should fully hide the sidebar.
- On mobile, closing should remove the drawer and overlay.
- On desktop, closing should also fully hide the sidebar, not collapse to icons.

---

# CRITICAL RULES

Do not redesign the full UI.
Do not remove grouped navigation.
Do not break hash routing.
Do not change backend code.
Do not change API calls.
Do not change RBAC logic.
Do not remove the top menu button.
This is a small frontend layout/behavior fix only.

---

# FILES TO MODIFY

Likely:

```text
app/static/app.js
app/static/styles.css
```

---

# REQUIRED BEHAVIOR

## Open State

When open:

- Sidebar is visible.
- Full labels are visible.
- Groups and children work normally.
- Active route highlighting works.

## Closed State

When closed:

- Sidebar should be completely hidden.
- Width should be `0` or it should be translated fully off-screen.
- Icon-only rail must not appear.
- Main content should occupy the freed space.
- Top menu button remains visible.

---

# IMPLEMENTATION REQUIREMENTS

## Remove / Disable Icon-Only Collapse Mode

Find CSS/classes related to collapsed sidebar, for example:

```text
.sidebar-collapsed
.nav-collapsed
.app-shell.nav-collapsed
.icon-only
```

Update behavior so collapsed state means:

```text
sidebar hidden
```

not:

```text
sidebar narrow icon rail
```

Do not show route badges/icons when sidebar is closed.

---

# CSS EXPECTATION

Desktop closed state should effectively do one of:

```css
.app-shell.nav-collapsed .sidebar {
  transform: translateX(100%);
  width: 0;
  min-width: 0;
  overflow: hidden;
}
```

For RTL/right sidebar, use the correct direction.

Or:

```css
.app-shell.nav-collapsed .sidebar {
  display: none;
}
```

But prefer transform/width if smoother and stable.

Main content should expand:

```css
.app-shell.nav-collapsed .main-content {
  margin-inline-end: 0;
}
```

Use actual current class names.

---

# JAVASCRIPT EXPECTATION

The sidebar state can remain:

```text
open / closed
```

But do not render icon-only version.

If the code currently checks collapsed state and renders only icons, remove that conditional.

When closed:

- Hide the sidebar.
- Do not render a mini rail.

---

# MOBILE BEHAVIOR

On mobile:

- Closed = drawer hidden.
- Open = drawer visible over content.
- Overlay works.
- `×`, ESC, outside click all close fully.

---

# ACCESSIBILITY

Keep:

```text
aria-expanded
aria-controls
aria-label
```

accurate.

When closed:

```text
aria-expanded=false
```

---

# MANUAL VALIDATION

After implementation verify:

1. Open page on desktop.
2. Sidebar is visible.
3. Click top menu button.
4. Sidebar disappears completely.
5. No narrow icon rail remains.
6. Main content expands.
7. Click top menu button again.
8. Sidebar opens normally.
9. Click internal `×`.
10. Sidebar disappears completely.
11. On mobile width, sidebar opens as drawer and closes fully.
12. Grouped navigation still works.
13. Active route highlighting still works.
14. No horizontal overflow.

---

# VALIDATION COMMANDS

Run:

```bash
python -m compileall app
python -m pytest
node --check app/static/app.js
```

---

# DEPLOYMENT

After implementation:

```bash
git add .
git commit -m "Hide sidebar completely when closed"
git push origin main
```

Render will auto-deploy.

---

# EXPECTED FINAL RESPONSE FROM CODEX

When finished, report:

1. Objective
2. Changed files
3. Root cause
4. CSS/JS fix implemented
5. Manual validation results
6. Validation command results
7. Deployment commands
