# UX References And Adoption Notes

This book combines usability heuristics, practical public-service design
patterns and web accessibility requirements. It turns those sources into
local engineering decisions for application screens and CRUD journeys.

WCAG is a conformance standard. Nielsen Norman Group heuristics are review
guidance. GOV.UK patterns are developed for government services. Their scopes
are different; adopting a pattern does not by itself prove usability or
accessibility in a different product.

## Source Guidance And Local Adoption

| Source | Guidance used | Local adoption |
| --- | --- | --- |
| [NN/G: Ten usability heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/) | Evaluate understandable state, familiar interaction, control, prevention and recovery | Review the user's task and turn concerns into observable acceptance behavior |
| [GOV.UK: Designing good services](https://www.gov.uk/service-manual/design/introduction-designing-government-services) | Understand the complete user problem and service journey | Include prerequisites, handoffs, completion and support in a short feature brief |
| [GOV.UK: Structuring forms](https://www.gov.uk/service-manual/design/form-structure) | Justify questions and structure them around use | Maintain a field inventory; choose focused steps or grouped entry according to the task |
| [GOV.UK: Question pages](https://design-system.service.gov.uk/patterns/question-pages/) | Make questions understandable and preserve previous answers | Explain required information, support back navigation and avoid repeated entry |
| [GOV.UK: Validation](https://design-system.service.gov.uk/patterns/validation/) | Preserve answers and provide discoverable, specific errors | Use submission validation as the default, linked errors and deliberate focus management |
| [GOV.UK: Check answers](https://design-system.service.gov.uk/patterns/check-answers/) | Allow review and correction before submission | Add review where error consequences justify it; avoid an automatic extra step for every save |
| [GOV.UK: Confirmation pages](https://design-system.service.gov.uk/patterns/confirmation-pages/) | Confirm the outcome and explain next steps | Provide durable confirmation for consequential work and distinguish queued from completed |
| [GOV.UK: Button](https://design-system.service.gov.uk/components/button/) | Communicate action and priority and avoid unexplained unavailable controls | Use accurate verb/object labels, clear action hierarchy and understandable pending behavior |
| [NN/G: Progressive disclosure](https://www.nngroup.com/articles/progressive-disclosure/) | Reveal less frequent complexity when needed | Keep optional advanced detail secondary while leaving material consequences visible |
| [NN/G: The three-click rule](https://www.nngroup.com/articles/3-click-rule/) | A fixed click limit is not a reliable usability rule | Evaluate understanding, completion and total effort, including correction |
| [GOV.UK: Moderated usability testing](https://www.gov.uk/service-manual/user-research/using-moderated-usability-testing) | Observe likely users attempting realistic tasks without coaching | Run proportionate sessions and distinguish observations from proxy reviews |
| [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | Testable accessibility criteria and conformance requirements | Target all applicable A and AA criteria across full pages and complete processes |
| [WAI-ARIA APG](https://www.w3.org/WAI/ARIA/apg/practices/read-me-first/) | Accessible semantics and widget interaction guidance | Prefer native controls and test custom components with actual browser/assistive-technology combinations |
| [WAI: Evaluating accessibility](https://www.w3.org/WAI/test-evaluate/) | Combine methods to evaluate access barriers | Pair automated checks with manual journey evaluation and report coverage limits |

## Accessibility Reading Map

[Accessibility](./accessibility.md) links directly to WAI explanations of
contrast, targets, focus, reflow, text resize, redundant entry, authentication,
status messages and dragging. Additional implementation references:

- [WAI forms tutorial](https://www.w3.org/WAI/tutorials/forms/): labels,
  grouping, instructions and feedback.
- [Error identification](https://www.w3.org/WAI/WCAG22/Understanding/error-identification.html)
  and [error suggestions](https://www.w3.org/WAI/WCAG22/Understanding/error-suggestion.html):
  describe input problems and known correction routes.
- [Error prevention for consequential transactions](https://www.w3.org/WAI/WCAG22/Understanding/error-prevention-legal-financial-data.html):
  alternatives involving reversal, checking or review.
- [Modal dialog pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/):
  focus placement, containment, dismissal and return.

## Local Decisions And Boundaries

- The five user questions, decision order, screen brief and action contract
  are local synthesis. They are not named certification schemes.
- Existing design systems take precedence for visual conventions when they
  satisfy the task and accessibility requirements. No brand palette, font,
  frontend framework or component library is mandated here.
- Single-column forms, submission-first validation, explicit-save defaults
  and larger touch controls are starting decisions with stated tradeoffs.
- One thing per page fits many infrequent public-service tasks. Repetitive
  internal work may benefit from grouped entry; validate with its users.
- The local 44-by-44 CSS-pixel control preference is not the WCAG AA minimum.
- A clean automated scan, a component library and a handful of user sessions
  each supply partial evidence; none alone proves complete conformance.
- Server-confirmed saving, duplicate-effect control and concurrent-edit
  recovery are local application contracts that support trustworthy feedback.
- Small qualitative studies guide iteration. This book promises no universal
  participant count or percentage of defects discovered.

Sources were reviewed in October 2026. Revisit adopted guidance when the
standard, target audience, interaction model or evidence changes.
