# Active Systems Research Lab

This directory is an isolated research workspace. It does not modify the Book Factory writing pipeline.

## First study: Van der Pol parameter sweep

The study prompt is in `prompts/vanderpol_parameter_study.md`. A manually dispatched GitHub Actions workflow sends it to Gemini using the repository's existing `GEMINI_API_KEY` secret and uploads the raw response as an artifact.

## Run

1. Open **Actions → Gemini Research Bridge**.
2. Choose **Run workflow** on branch `research/active-systems-lab`.
3. Optionally enter a model name. The default is the repository variable `GEMINI_MODEL`, falling back to `gemini-3.8-flash`.
4. Download the workflow artifact and inspect the JSON response.

The workflow is manual-only, read-only with respect to repository contents, and does not print or persist the API key. It does not commit generated research results.

## Validation policy

Gemini's numerical claims are hypotheses until independently reproduced. Check equations, solver tolerances, transient removal, period estimation, Floquet exponent, and convergence before using results in the book.
