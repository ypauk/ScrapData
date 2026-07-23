# TASK

## MILESTONE 6 — Resilience

# Implement Resume Support

---

## Goal

Implement a Resume Support component that allows the scraping framework to automatically continue a previously interrupted scraping session.

The component must use the existing Checkpoint Manager and Incremental Saving infrastructure.

It must **not** duplicate checkpoint logic.

---

## Existing Architecture

The project already contains:

* Configuration Manager
* Logging
* Error Handling
* Incremental Saving
* Batch Writer
* Checkpoint Manager
* Requests Engine
* Playwright Engine
* Proxy Layer

Resume Support must integrate with these components.

Do not replace existing functionality.

---

## Before Implementation

First analyze the existing architecture.

Explain:

* how Checkpoint Manager stores state;
* how Incremental Saving currently works;
* how Resume Support should integrate with them;
* which files require modification;
* possible risks.

Wait for approval before writing code.

---

## Responsibilities

Resume Support must:

* detect an existing checkpoint automatically;
* restore the previous scraping state;
* continue scraping from the last saved position;
* avoid reprocessing already completed work;
* work transparently for the scraper.

Resume Support must NOT:

* implement checkpoint creation;
* write export files directly;
* perform parsing;
* duplicate state management.

---

## Resume Sources

The component should restore information such as:

* current page;
* current URL;
* current cursor/token;
* exported record count;
* processed record count;
* current scraping mode;
* execution metadata.

The implementation should be extensible for future scraper types.

---

## Startup Behaviour

On scraper startup:

If no checkpoint exists:

* start a new scraping session.

If a checkpoint exists:

* validate it;
* restore the saved state;
* continue automatically.

Future versions may optionally ask the user whether to resume or restart.

---

## Integration with Incremental Saving

Resume Support must work together with Incremental Saving.

Previously exported records must remain intact.

Resume Support must never overwrite existing output files.

---

## Integration with Batch Writer

Before restoring:

* ensure pending batches have already been flushed;
* avoid duplicate writes after resume.

---

## Duplicate Protection

Resume Support must prevent duplicate processing after recovery.

The restored state should continue exactly after the last successfully completed checkpoint.

---

## Error Handling

Handle:

* missing checkpoint;
* corrupted checkpoint;
* incompatible checkpoint version;
* incomplete checkpoint data.

If recovery is impossible:

* log the error;
* safely start a new scraping session.

The framework must never crash because of an invalid checkpoint.

---

## Logging

Integrate with the centralized Logging component.

Log:

* checkpoint detected;
* checkpoint loaded;
* resume started;
* resume completed;
* invalid checkpoint;
* recovery failures.

Avoid excessive log output.

---

## Configuration

Use the existing Configuration Manager.

Support future configuration for:

* automatic resume;
* manual resume;
* resume confirmation;
* checkpoint expiration.

Avoid hardcoded values.

---

## Design Rules

Before creating any new file:

* inspect existing modules;
* reuse existing functionality;
* explain why a new file is needed;
* avoid duplicated code.

Prefer extending existing modules instead of introducing unnecessary abstractions.

---

## Allowed Changes

Modify only the files required for this task.

Do not refactor unrelated parts of the project.

Avoid modifying more than 5 files.

---

## Expected Result

After implementation:

* interrupted scraping sessions can continue automatically;
* already exported records remain untouched;
* duplicate processing is prevented;
* integration with Checkpoint Manager is seamless;
* backward compatibility is preserved.

---

## Deliverables

Provide:

1. Architecture explanation.
2. List of modified files.
3. Implementation.
4. Verification that existing functionality still works.
5. Demonstration of a successful resume after an interrupted scraping session.

---

## Success Criteria

The task is complete when:

* the framework automatically resumes interrupted scraping;
* existing checkpoints are reused;
* duplicate processing is prevented;
* existing exported data is preserved;
* backward compatibility is maintained;
* the implementation remains reusable, extensible and framework-independent.
