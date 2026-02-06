namespace AIFoundryEvaluation.DataAccess.Models;

/// <summary>
/// Represents the input data for an evaluation.
/// </summary>
public record EvaluationInput(
    string Query,
    string? GroundTruth,
    string? Response,
    string? Context,
    double? Latency,
    int? ResponseLength
);
