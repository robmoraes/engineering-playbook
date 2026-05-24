# Users First

## Serving A Human Goal

A user does not normally want a database, a deployment or a form. The user
wants to find a book, submit a request, understand a result, complete a job or
recover from a problem. Engineering starts by understanding that goal well
enough to reduce its friction without creating avoidable risk.

A useful system respects the user's time, attention, data and ability to make
decisions.

## Stakeholders And Users

Stakeholders define funding, policy, priorities and constraints. Their needs
are real. They are not always the same as the daily needs of the person using
the software.

Professional engineering makes that distinction visible:

- translate requests into the user outcome they are intended to improve;
- identify when a requested control creates repeated manual burden or
  confusion for users;
- explain tradeoffs clearly rather than silently implementing a harmful
  interpretation;
- meet organizational obligations without using them as a reason to disregard
  usability, safety or dignity.

The point is not to oppose stakeholders. It is to ensure that delivery serves
the people for whom the system has consequences.

## Evidence Of Usefulness

User-first work does not depend only on personal intuition. Depending on the
system, evidence may include:

- observing the actual workflow before automating it;
- testing language, navigation and error recovery with representative users;
- measuring completion, latency, failure and abandonment where measurement is
  appropriate and respectful;
- examining support requests and incidents for recurring friction;
- verifying accessibility and operation under realistic constraints.

Feedback should be used with humility. A user struggling with the system is
not a failure of the user to understand our design.

## Ordinary Failure Paths

Software affects people most clearly when something is missing, slow or
broken. User-first engineering considers:

- validation messages that explain what can be corrected;
- safe retry or recovery after interruptions;
- accurate status instead of false success;
- clear behavior when no data, no permission or no availability exists;
- supportable audit trails where a consequential action must be understood.

Reliability is part of usability. A workflow that is elegant when healthy but
unrecoverable when interrupted is not complete.

## Review Questions

Before accepting a user-facing change, ask:

- What task becomes easier, safer or more reliable?
- What does a person see when the operation cannot be completed?
- Does this design exclude people unnecessarily through complexity,
  accessibility barriers or poor language?
- Does it ask for, expose or retain more personal data than its purpose
  requires?
- Will operational staff be able to help the user when a problem occurs?
