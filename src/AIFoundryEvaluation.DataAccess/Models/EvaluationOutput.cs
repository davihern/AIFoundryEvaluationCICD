namespace AIFoundryEvaluation.DataAccess.Models;

/// <summary>
/// Represents the complete output data for an evaluation.
/// </summary>
public record EvaluationOutput(
    GroundednessOutput? Groundedness,
    SimilarityOutput? Similarity
);
