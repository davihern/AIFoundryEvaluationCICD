# AI Foundry Evaluation Data Access Layer

A .NET class library for reading and querying AI Foundry evaluation results.

## Overview

This library provides a clean, type-safe way to work with AI Foundry evaluation data in .NET applications. It includes models and data access methods for reading evaluation results from JSON files.

## Features

- **Type-safe data models** using C# records
- **Async/await support** for file I/O operations
- **LINQ-friendly filtering** methods
- **Comprehensive error handling** with proper exception types
- **Full unit test coverage** with xUnit

## Getting Started

### Prerequisites

- .NET 9.0 SDK or later

### Building the Project

```bash
dotnet build
```

### Running Tests

```bash
dotnet test
```

## Usage

### Reading Evaluation Results

```csharp
using AIFoundryEvaluation.DataAccess;

var dataAccess = new EvaluationDataAccess();
var results = await dataAccess.ReadEvaluationResultsAsync("myevalresults.json");

Console.WriteLine($"Total results: {results.Rows.Count}");
```

### Filtering by Groundedness

```csharp
var highQualityResults = dataAccess.FilterByGroundedness(results, minimumGroundedness: 4.0);
Console.WriteLine($"High quality results: {highQualityResults.Count}");
```

### Getting Failed Results

```csharp
var failedResults = dataAccess.GetFailedResults(results);
foreach (var result in failedResults)
{
    Console.WriteLine($"Failed query: {result.Inputs.Query}");
    Console.WriteLine($"Reason: {result.Outputs.Groundedness?.GroundednessReason}");
}
```

### Getting Passed Results

```csharp
var passedResults = dataAccess.GetPassedResults(results);
Console.WriteLine($"Passed evaluations: {passedResults.Count}");
```

## Data Models

### EvaluationInput
Contains the input data for an evaluation:
- Query
- Ground Truth
- Response
- Context
- Latency
- Response Length

### EvaluationOutput
Contains the evaluation results:
- Groundedness metrics and results
- Similarity metrics and results

### EvaluationResult
Combines input and output data for a single evaluation.

### EvaluationResultDocument
Container for multiple evaluation results.

## Architecture

The library follows .NET best practices:
- **Records for immutability** - All models use C# records for value semantics
- **Nullable reference types** - Full nullable annotation for safer code
- **Async patterns** - ConfigureAwait(false) for library code
- **Proper exception handling** - Specific exception types with clear messages
- **SOLID principles** - Single responsibility, simple and focused classes

## Testing

The library includes comprehensive unit tests covering:
- Valid and invalid input scenarios
- Edge cases and error conditions
- Data parsing and transformation
- Filtering and querying operations

Run tests with coverage:
```bash
dotnet-coverage collect -f cobertura -o coverage.cobertura.xml dotnet test
```

## Project Structure

```
src/
  AIFoundryEvaluation.DataAccess/
    Models/                      # Data models
    EvaluationDataAccess.cs     # Main data access class

tests/
  AIFoundryEvaluation.DataAccess.Tests/
    EvaluationDataAccessTests.cs # Unit tests
```

## License

See the LICENSE file in the repository root.
