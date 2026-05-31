# Internationalization and Localization Standards

Internationalization is an architecture concern because language, locale,
formatting, search, accessibility and content operations affect user trust and
data correctness. Localization should not be added as a late text replacement
layer after product behavior, schemas and navigation have already assumed one
language.

## Core Model

Use these concepts explicitly in product, code, schemas and API contracts:

| Concept | Meaning | Examples | Store as |
| --- | --- | --- | --- |
| Language | The human language of content | Portuguese, English, Spanish | BCP 47 language tag where needed |
| Locale | Language plus regional or script conventions | `pt-BR`, `en-US`, `zh-Hant-TW` | BCP 47 locale tag |
| Translation key | Stable application identifier for a message | `checkout.payment_failed` | source-controlled key |
| Message | Localizable user-facing text with placeholders and plural rules | "1 item", "2 items" | message catalog entry |
| Content locale | Locale of authored or editorial content | blog article in `pt-BR` | content metadata |
| User locale preference | User's chosen display language/locale | `en-US` UI preference | user profile or tenant setting |
| Formatting locale | Locale used for dates, numbers, currency and lists | `pt-BR` currency format | explicit formatting input |
| Timezone | Civil-time rules for display or scheduling | `America/Sao_Paulo` | IANA timezone identifier |

Do not collapse these concepts into one field named `language`. A user may read
the UI in English, format currency for Brazil and schedule events in
`Europe/Lisbon`.

## Non-Negotiable Defaults

- Use BCP 47 tags such as `pt-BR`, `en-US`, `es-419` and `zh-Hant` for
  languages and locales. Do not invent custom codes such as `br`, `pt_BR` or
  `english`.
- Keep locale separate from timezone. Locale controls language and formatting;
  timezone controls civil-time interpretation.
- Store source-controlled translation keys, not display text, as durable
  application identifiers.
- Never concatenate translated fragments to build a sentence. Use complete
  messages with placeholders, plural/select rules and translator context.
- Do not localize logs, metrics, traces, audit event names, API error codes or
  machine-readable identifiers. Localize user-facing presentation.
- Format dates, numbers, currency, relative time and lists with locale-aware
  platform libraries instead of hard-coded string patterns.
- Treat missing translations as a release quality issue. Fallbacks are allowed
  for resilience, but they should be observable and reviewed.
- Design interfaces to tolerate longer text, different word order,
  right-to-left direction and locale-specific sorting.

## Locale Selection

Locale selection should be deterministic and visible enough to debug. The
normal precedence is:

1. explicit user preference;
2. tenant, workspace or organization preference;
3. route, domain or product edition locale where the product supports it;
4. browser or client `Accept-Language` preference;
5. documented product default.

Do not permanently overwrite a user preference with browser detection.
Detection is a convenience for first use, not proof of intent.

For web applications, prefer locale in the URL when localized content must be
linkable, cacheable or indexed:

```text
/pt-BR/docs/checkout
/en-US/docs/checkout
```

Session-only locale is acceptable for authenticated application UI where SEO
and shareable localized URLs are not material.

## Message Catalogs

Translation catalogs SHOULD be organized around product domains, not arbitrary
screens:

```text
locales/
  en-US/
    checkout.json
    account.json
  pt-BR/
    checkout.json
    account.json
```

Keys should describe stable meaning, not the current English copy:

```json
{
  "checkout.payment_failed": "Payment could not be completed.",
  "checkout.items_count": "{count, plural, one {# item} other {# items}}"
}
```

Avoid keys such as `submit_button_text` when several submit buttons exist, or
`payment_could_not_be_completed` when copy changes without behavior changing.

Catalog entries that include placeholders SHOULD define enough context for
safe translation:

- placeholder meaning and type;
- whether a value is user-provided or trusted system text;
- plural category behavior;
- character limits where the UI is constrained;
- tone or product context when ambiguity exists.

## Application Boundaries

Internationalization belongs at user-facing boundaries and authored content
boundaries. Internal services should pass stable codes, typed fields and
structured context rather than pre-localized sentences.

```text
Backend/API returns:
{
  "code": "payment_card_declined",
  "message_key": "checkout.card_declined",
  "params": { "last4": "4242" }
}

Frontend renders:
"Your card ending in 4242 was declined."
```

Backend-rendered products may render localized messages on the server, but the
boundary must still keep codes and parameters structured. Do not make clients
parse localized text to determine behavior.

## Formatting Rules

Locale-aware formatting is not the same as translation. Use platform
internationalization APIs or mature libraries for:

- dates and times;
- numbers and percentages;
- currencies;
- relative time;
- lists and conjunctions;
- collation and locale-aware sorting;
- plural categories and gender/select variants where needed.

Currency should be stored as amount plus ISO currency code and formatted at
display time. Do not infer currency from locale; `en-US` users may need EUR,
BRL or JPY.

Dates and times MUST follow
[Time and Timezone Standards](./time-and-timezone-standards.md). Locale may
change display format; it must not silently change the instant or schedule
timezone.

## UI and Accessibility

Interfaces SHOULD be built for linguistic variation:

- allow translated labels to expand without overlap or truncation in critical
  actions;
- support right-to-left direction when the supported locale set requires it;
- avoid embedding text in images unless each locale has a managed asset;
- expose `lang` and, where needed, `dir` attributes in HTML;
- ensure screen-reader labels and validation messages use the active locale;
- keep icons and gestures culturally reviewed when meaning may vary.

Do not use flags as language selectors. Countries are not languages, and many
languages are used across multiple regions.

## Data and Persistence

Persist locale and language preferences as explicit values:

```sql
preferred_locale text not null default 'en-US'
```

Validate persisted locale tags against the application's supported locale
list. A syntactically valid BCP 47 tag does not mean the product has
translations, formatting QA or support coverage for that locale.

For localized content, persist both the content locale and fallback policy:

```text
content_id: pricing-page
locale: pt-BR
fallback_locale: en-US
status: translated | reviewed | stale
```

Fallback should be intentional. Silent fallback can hide incomplete launches,
legal wording gaps or inaccessible flows.

## API Contracts

APIs SHOULD keep machine-readable behavior stable across locales:

- stable error codes;
- stable enum values;
- numeric values as numbers, not localized strings;
- dates/times in contract formats, not localized display formats;
- optional localized display fields only when the API explicitly serves a UI
  or content delivery use case.

When an API accepts locale, name the field precisely:

```yaml
locale:
  type: string
  example: "pt-BR"
timezone_id:
  type: string
  example: "America/Sao_Paulo"
```

Do not use `lang` for formatting, routing, timezone and content selection at
the same time.

## Testing Requirements

Internationalized applications SHOULD test:

- every supported locale loads without missing required keys;
- fallback behavior is explicit and observable;
- pluralization for zero, one and many values, plus language-specific
  categories where applicable;
- interpolation escapes untrusted values and preserves intended markup;
- forms, validation messages and accessibility labels in each supported
  locale;
- long translated strings in compact layouts;
- right-to-left rendering when supported;
- locale-aware sorting and search where user-visible order matters;
- date, number and currency formatting for at least two materially different
  locales.

Automated checks should fail builds for malformed catalogs, missing keys in
required locales and unused keys where that signal is reliable.

## Operational Practices

Localization changes should follow the same delivery discipline as code:

- catalogs are versioned with the application or released through a controlled
  translation delivery system;
- product changes that add user-facing text include translation keys and
  translator context;
- rollout plans identify whether a locale can ship partially or must be fully
  reviewed;
- analytics and support workflows can identify active locale and fallback
  usage without storing unnecessary personal data;
- production incidents use stable codes and UTC operational timestamps, not
  localized messages, as the investigation backbone.

## Reference Basis

This standard adopts external guidance as follows:

- BCP 47 language tags provide the interoperable syntax for language and
  locale identifiers.
- Unicode CLDR provides locale data used by many platforms for formatting,
  plural rules and display names.
- W3C internationalization guidance motivates explicit document language,
  direction and authoring practices.
- ICU MessageFormat-style messages motivate complete messages with plural and
  select rules instead of string concatenation.

See [Architecture References](./references.md) for source links and adoption
notes.

## Review Checklist

- [ ] Are supported locales explicitly listed and validated?
- [ ] Is locale separate from timezone, currency and content region?
- [ ] Are user-facing strings represented by stable translation keys?
- [ ] Are pluralization, interpolation and translator context handled in the
      catalog format?
- [ ] Do APIs expose stable codes instead of localized behavior identifiers?
- [ ] Are missing translations and fallback usage visible in validation or
      telemetry?
- [ ] Does UI layout tolerate longer text and right-to-left direction where
      required?
- [ ] Are dates, times, numbers and currencies formatted with locale-aware
      libraries?
- [ ] Are logs, metrics, traces and audit events kept machine-readable and
      language-neutral?
