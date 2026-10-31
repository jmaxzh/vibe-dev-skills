---
name: sdlc-ui-interaction
description: Design, implement, modify, review, or optimize user interfaces and interactions for desktop, mobile, and web, or provide guidance on UI and interaction design principles. Use when the task concerns interface or interaction behavior; do not apply to backend-only, database-only, or other tasks without UI or interaction work.
---

# UI and Interaction Design

## Applicability

- Apply automatically when the task involves desktop, mobile, or web UI and interaction design, implementation, modification, review, optimization, or advice on the corresponding principles; explicit invocation is unnecessary.
- This skill works independently of the SDLC workflow. Do not apply to backend-only, database-only, or other tasks without UI or interaction work.
- When only principle guidance is requested, do not automatically expand into product-specific design, implementation, or acceptance testing.

## Read on demand

- Follow the shared principles below and read platform references for the actual target and scenario; do not load all platform rules by default.
- Desktop: read [desktop principles](references/desktop-ui-interaction.md).
- Mobile: read [mobile principles](references/mobile-ui-interaction.md).
- Web: read [web principles](references/web-ui-interaction.md).
- For mobile web, read both mobile and web principles. For other combinations, load additional references according to the selected documents' conditions.
- If the platform is unspecified, infer it from the task and project context first. For general advice, use only shared principles. Ask for clarification only if a concrete task still lacks a necessary platform decision.

## Shared principles

### Usage

- Select principles for the target platform and scenario. Give general guidance directly when no specific product is identified.
- Explain applicability conditions and tradeoffs; do not prescribe a particular visual style universally.
- Before quoting numeric values, verify the target platform's standards, units, and applicability.

### Design principles

- **Tasks and entry points**: organize the UI by user goals and operation order. Prioritize current tasks, make primary entry points recognizable, name actions and objects in buttons, and label ambiguous icons.
- **Cognitive load**: present options and context needed for decisions, reduce memorization and repeated input, and let users inspect and change defaults. Do not hide necessary information merely to reduce steps.
- **Consistency and style**: follow platform conventions and consistent control behavior. Align icons, components, and decoration with product purpose and existing design conventions; prevent decoration from obstructing content or actions.
- **Status and waiting feedback**: show location, processing status, and outcomes. Distinguish loading, empty data, and failure. Respond promptly, provide credible status for long operations, and actual progress when measurable. Scale feedback to importance without frequent interruption.
- **User control**: provide discoverable exit, cancel, and return actions. Support undo and redo where appropriate and clarify their effects. Explain consequences before irreversible actions.
- **Error prevention and recovery**: state input and operation constraints in advance; require confirmation according to consequences. Validate at appropriate times without interrupting incomplete input. On failure, preserve valid input, locate the issue, explain why it occurred, and offer recovery.
- **Typography**: choose fonts and sizes for reading conditions. Establish hierarchy through size and weight; keep body and supporting text readable, including when enlarged, without clipping or hiding necessary content or controls.
- **Layout and spacing**: use position and grouping to express importance and relationships. Apply alignment and spacing consistently. Match density to reading, comparison, and operation needs; avoid competing emphasis.
- **Color and contrast**: define primary, supporting, and status colors and use them consistently. Ensure adequate contrast for text, controls, and states; supplement color with text or shapes.
- **Interaction targets**: size and space targets for mouse, touch, or other input methods, making them easy to select without accidental adjacent activation.
- **Accessibility**: support keyboard and assistive technology in the target environment, with identifiable control names, states, and focus. Provide equivalent actions for precision input or complex gestures.
