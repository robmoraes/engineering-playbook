# Screen Structure And Content

A screen should present the information and controls needed for its current
task in a predictable order. Use familiar components and consistent language
to reduce interpretation effort.

## Establish Hierarchy

Default composition:

1. Page title and enough context to identify the current object or task.
2. Status or instructions that materially affect the decision.
3. Main content, fields or results grouped by meaning.
4. A clear primary action with nearby secondary actions.
5. Contextual help and supplementary detail where needed.

Each action group SHOULD have one visually dominant action. A page may have
several independent groups; do not force every action into a single global
button or give all controls equal emphasis.

Use headings, spacing and alignment to communicate relationships. Establish
reusable spacing, typography, colors and component states in the existing
design system. Preserve readable contrast in muted text and secondary actions.

## Language And Action Labels

Use the audience's vocabulary and a consistent name for each concept. Prefer
specific verbs that predict the result:

| Ambiguous | More informative when accurate |
| --- | --- |
| Submit | Create customer |
| OK | Save changes |
| Continue on a final action | Send invitation |
| Delete for a reversible state change | Archive customer |
| Error 409 | This record changed while you were editing. Review the latest version. |

Use `Continue` for a step transition and explain when that transition also
saves a draft. Separate `Save draft` from a final submission if their effects
differ. Icons can support labels; unfamiliar icon-only actions add guesswork.

Write errors, help and confirmations alongside the interaction design. Do not
leave them to raw API strings. Keep business meaning and user language
consistent with [Localization Standards](../architecture/internationalization-and-localization.md).

## Navigation

- Use links for navigation and buttons for actions.
- Make current location and selected navigation programmatically available.
- Keep navigation order and names stable across related screens.
- Preserve browser history and meaningful direct links.
- On route changes, update the document title and manage focus deliberately.
- Reveal prerequisites when an action is unavailable; an unexplained disabled
  control does not teach the user how to proceed.

Hide actions irrelevant to the user's role when that reduces confusion. Show
an explanation where understanding a restriction helps complete the task.
Server authorization remains mandatory regardless of what the interface hides.

## Lists, Tables And Search

Show the fields people use to identify, distinguish and act on records. Keep
row actions associated with the correct item; use an accessible name such as
`Edit customer Acme` when several edit buttons appear.

- Give tables meaningful headers and expose sorting state.
- Label search scope, show active filters and provide a clear reset action.
- Distinguish no records, no matching results and a failed request.
- Preserve search, sort and position when returning from a record.
- Prefer explicit pagination for task-oriented record lists when it supports
  returning to a known result; evaluate alternatives for browsing contexts.
- For bulk actions, state whether selection covers this page or all matches,
  show the count and report partial failures by item where appropriate.

On narrow screens, keep identification and core actions available. A
responsive table, scoped horizontal scrolling or a structured list may fit;
do not hide data essential to the decision just to fit a viewport.

## Dialogs And Overlays

Reserve modal dialogs for bounded decisions that need current context. Use a
dedicated page for extensive input, rich navigation or work likely to be
interrupted. Avoid nested dialogs.

A modal must have a name, intentional initial focus, contained keyboard focus
and a usable close/cancel path. Return focus to the trigger or a logical
successor. Closing a confirmation means cancellation, not approval. Follow
the [WAI-ARIA dialog pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/)
and test the actual component.

## Responsive And Realistic Content

Review with long names, missing values, localized text, large counts and the
smallest supported viewport. Use flexible layout and text wrapping. Keep a
logical DOM order when the visual arrangement changes.

Use purposeful motion and stable layouts. Keep controls from shifting during
loading, and ensure persistent headers or action bars do not cover content or
keyboard focus. Accessibility limits and manual checks are defined in
[Accessibility](./accessibility.md).

## Review Questions

- Can a new user name the task and identify the next action?
- Can a frequent user reach the necessary information without repeated search?
- Do labels predict actual effects, including messages sent and data changed?
- Does the same concept behave and look consistently across the product?
- Does the screen remain understandable with realistic content and zoom?
