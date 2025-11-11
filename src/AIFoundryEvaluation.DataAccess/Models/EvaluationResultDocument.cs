namespace AIFoundryEvaluation.DataAccess.Models;

/// <summary>
/// Represents the complete evaluation results document.
/// </summary>
public record EvaluationResultDocument(
    IReadOnlyList<EvaluationResult> Rows
);
