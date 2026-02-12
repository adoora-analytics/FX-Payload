# Design Decisions

## Why 1 row = 1 currency rate
Each currency rate at a given date represents a single stand-alone business fact.

## Why main.py is thin
Pipeline coordination is separated from business logic to keep modules testable.

## Why raw and processed folders are git-ignored
Data should not be versioned in a source repository.
