# Design Decisions

## Why 1 row = 1 currency rate
Each currency rate at a given date represents a single stand-alone business fact.

## Why main.py is thin
Pipeline coordination is separated from business logic to keep modules testable.

## Why raw and processed folders are git-ignored
Data should not be versioned in a source repository.

## Why the pipeline is idempotent
The pipeline rewrites the output file for a given logical date instead of appending blindly.
This ensures rerunning the same date produces identical results without duplication.

# Reasoning:
Data pipelines must tolerate retries and partial failures without corrupting downstream data.

