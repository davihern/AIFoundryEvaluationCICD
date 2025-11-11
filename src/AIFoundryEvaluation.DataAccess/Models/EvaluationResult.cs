namespace AIFoundryEvaluation.DataAccess.Models;

/// <summary>
/// Represents a single evaluation result row.
/// </summary>
public record EvaluationResult(
    EvaluationInput Inputs,
    EvaluationOutput Outputs,
    int LineNumber
);
