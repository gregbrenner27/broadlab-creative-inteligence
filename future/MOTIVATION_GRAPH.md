# Future Integration: Broadlab Motivation Graph

## What the Motivation Graph Is

Broadlab's Motivation Graph is a proprietary mapping of audience motivational states used across their platform. It encodes how different UK audience segments are motivated at a postcode level, enabling precise targeting based on psychological drivers rather than just demographic proxies.

## Current State

The Creative Intelligence Platform currently uses a generic five-state motivational framework:
1. Achievement and Mastery
2. Belonging and Social Validation
3. Security and Reliability
4. Status and Aspiration
5. Value and Fairness

This is a reasonable approximation but does not reflect Broadlab's actual motivation taxonomy, which is likely more granular and cross-referenced with their postcode audience graph.

## Where to Update When Document Becomes Available

When the Motivation Graph documentation is received from the Broadlab data team:

1. **Encode the full motivation taxonomy here** — replace the generic five-state list above with Broadlab's actual motivation categories

2. **Update `framework/SCORING_RUBRIC.md`** — the Dimension 4 (Motivational Alignment) scoring section references the generic five states. Update these to match Broadlab's categories.

3. **Update `framework/PERSONA_TEMPLATE.md`** — the pre-built personas use generic motivation labels. Update the `primary_motivation` and `secondary_motivation` fields to use Broadlab's taxonomy.

4. **Update `prompts/RESONANCE_PROMPT.md`** — the resonance prompt instructs Claude to score motivational alignment. Update the motivation categories it references.

5. **Update the frontend dropdown** — the motivation selector in `InputForm.jsx` currently shows the five generic options. Update the options to match Broadlab's taxonomy.

## Expected Benefit

Using Broadlab's actual Motivation Graph will:
- Improve Dimension 4 accuracy significantly
- Enable direct cross-referencing between resonance scores and the postcode audience graph in Snowflake
- Produce targeting recommendations that map directly to Broadlab's existing campaign targeting infrastructure

## Contact

Motivation Graph documentation should be requested from the Broadlab data or strategy team. Once received, pass to the development team to implement the updates listed above.
