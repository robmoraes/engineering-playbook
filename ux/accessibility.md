# Accessibility

Adopt WCAG 2.2 level AA for production web interfaces. That target includes all
applicable level A and AA criteria across full pages and complete processes.
This chapter supplies practical checks; it is not an exhaustive conformance
assessment. [WCAG 2.2](https://www.w3.org/TR/WCAG22/)

WCAG success criteria and conformance requirements are normative. WAI
Understanding documents and ARIA Authoring Practices explain implementation
but do not replace the standard. Local defaults below may be stronger than
the minimum.

## Semantics First

Use native headings, landmarks, links, buttons, labels, fieldsets, legends
and tables for their intended meanings. Supply a useful document title and
correct language. Accessible names should include visible label text so
speech-input users can identify controls.

Use maintained components and test their integration. ARIA adds semantics; it
does not implement keyboard interaction. A clickable generic element with a
role is not automatically equivalent to a native button.
[WAI-ARIA implementation guidance](https://www.w3.org/WAI/ARIA/apg/practices/read-me-first/)

## Keyboard And Focus

- Complete the main task using keyboard alone, with a logical focus order.
- Keep focus visible and avoid positive `tabindex` values that reorder it.
- Make repeated navigation bypassable, for example with a skip link.
- Keep focus in a modal while it is open and return it appropriately on close.
- Move focus deliberately after route changes and failed submissions.
- Ensure disclosure widgets expose their expanded/collapsed state.

WCAG AA requires visible focus and prevents the focused component from being
entirely hidden by author-created content. The local default is to keep both
the control and focus indicator fully visible, including beneath sticky bars.
A particular two-pixel ring is not an AA mandate.
[Focus visible](https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html),
[focus not obscured](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html)

## Visual And Responsive Checks

| Concern | WCAG requirement or test | Local application |
| --- | --- | --- |
| Text contrast | 1.4.3 AA: 4.5:1; 3:1 for large text, with stated exceptions | Check actual colors across themes and states |
| Meaningful non-text contrast | 1.4.11 AA: 3:1 for required control/state/graphic information, with exceptions | Check relevant input boundaries and selected states |
| Pointer targets | 2.5.8 AA: at least 24 by 24 CSS pixels or a qualifying exception | Prefer 44 by 44 CSS pixels for common standalone controls, especially touch |
| Reflow | 1.4.10 AA: vertical content at 320 CSS pixels wide without loss or two-direction scrolling, except necessary two-dimensional regions | Test narrow layout and zoom; scope table scrolling to the table |
| Text resizing | 1.4.4 AA: up to 200% without loss, subject to stated exceptions | Test text resize independently of viewport changes |

Large text in the contrast rule means at least 18 pt regular or 14 pt bold.
Do not round a failing contrast result upward. A required indicator cannot
depend on color alone; add text, shape or another usable cue.

The target-size criterion includes spacing, equivalent-control, inline,
unmodified user-agent and essential exceptions. Consult the actual geometry;
it is not a universal requirement for 24-pixel gaps. The 44-pixel enhanced
target criterion is AAA; our larger-control preference is a local default.

Sources: [text contrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html),
[non-text contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html),
[target minimum](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html),
[target enhanced](https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced.html),
[reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html),
[text resize](https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html).

Also check that user overrides of line, paragraph, word and letter spacing do
not clip text or controls. These override tests are not required authored
typography values. [Text spacing](https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html)

## Forms, Errors And Status

Associate controls with labels, hints and error text. Mark invalid fields
programmatically and provide specific correction suggestions when known and
safe. Use the error-summary pattern in [Forms and Data Entry](./forms-and-data-entry.md)
where it helps locate problems.

When previously provided information is needed again within the same process,
prefill it or make it selectable unless a relevant exception applies, such as
security, essential re-entry or obsolete information. Browser autocomplete
alone does not satisfy this requirement.
[Redundant entry](https://www.w3.org/WAI/WCAG22/Understanding/redundant-entry.html)

Expose saving, success, failure and result-count status programmatically
without requiring focus to move to the message. Use polite live status for
routine updates and urgent announcements sparingly. Avoid announcing every
keystroke or every unrelated data change.
[Status messages](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html)

## Authentication And Alternative Interaction

Allow password managers, autocomplete and paste for credentials and one-time
codes. Avoid requiring users to remember or manually transcribe information
when assistance or an accessible alternative can support the task. WCAG's
accessible-authentication criterion permits specified mechanisms and
exceptions; it does not ban passwords.
[Accessible authentication](https://www.w3.org/WAI/WCAG22/Understanding/accessible-authentication-minimum.html)

Provide a non-dragging single-pointer alternative to drag operations, such as
move controls. Keyboard support is also necessary but does not alone satisfy
the dragging criterion. [Dragging movements](https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html)

Avoid hover-only information, unnecessary motion and gesture-only actions.
Honor reduced-motion preferences and retain usable alternatives. Give
meaningful images appropriate text alternatives and mark decorative images
accordingly. Include applicable captions or other alternatives for media.
Review time limits and session warnings against the complete WCAG criteria.

## Verification Evidence

Combine automated checks with manual keyboard, zoom/reflow, contrast and
screen-reader checks of the actual journey. Record browser, assistive
technology, tested state, result and remaining failures. Test with disabled
users where possible; developer checks provide different evidence.

A component library or a clean automated scan cannot establish conformance.
An accepted project exception also does not make a failing criterion conform.
Use the complete applicable standard for any conformance claim.
[WAI evaluation overview](https://www.w3.org/WAI/test-evaluate/)
