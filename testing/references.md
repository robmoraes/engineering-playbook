# References and Adoption Notes

The sources below provide test documentation, test design and
behavior-description guidance. This playbook adopts a deliberately lightweight
artifact: enough context for reliable execution and traceability, without
requiring every project to implement a complete test management framework.

## External Guidance and Adoption

| Source | Relevant original guidance | Adoption in this playbook |
| --- | --- | --- |
| ISO/IEC/IEEE 29119-3:2021, *Test documentation* | Specifies test documentation templates applicable across software lifecycle models and testing activities. | The standard is a reference model; projects use only fields that improve repeatability, evidence, governance or risk control. |
| ISTQB, *Certified Tester Foundation Level Syllabus v4.0.1* | Describes traceability between the test basis, testware, results and risks; covers risk-based testing and established test techniques. | Cases link to expected behavior or risk, and teams select coverage using boundaries, partitions, decision tables and state transitions where relevant. |
| Cucumber, *Gherkin Reference* | Structures examples around initial context, an event and expected outcomes, and recommends keeping examples concise and expressive. | Cases use `Given`, `When` and `Then` semantics for behavior-oriented scenarios without requiring executable Gherkin or Cucumber. |
| Cucumber, *Behaviour-Driven Development* | Treats concrete examples and collaboration as ways to create shared understanding before automation. | Test cases complement specifications and conversation; they are not used as a substitute for clarifying product intent. |

## Source Links

- ISO/IEC/IEEE 29119-3:2021, *Software and systems engineering - Software
  testing - Part 3: Test documentation*:
  <https://www.iso.org/standard/79429.html>
- ISTQB, *Certified Tester Foundation Level Syllabus v4.0.1*:
  <https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf>
- Cucumber, *Gherkin Reference*:
  <https://cucumber.io/docs/gherkin/reference/>
- Cucumber, *Behaviour-Driven Development*:
  <https://cucumber.io/docs/bdd/>

## Local Conventions

The following are playbook decisions rather than universal requirements of the
referenced sources:

- one case verifies one behavior or closely related risk;
- the default case combines concise metadata with a behavior-oriented
  scenario;
- design, execution history, evidence and defects remain distinct artifacts;
- three to five scenario steps are a readability target, not an inflexible
  limit;
- automated and manual cases use the same expected-behavior model;
- documentation depth grows with product risk and coordination needs.
