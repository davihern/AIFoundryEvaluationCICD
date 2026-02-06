namespace AIFoundryEvaluation.DataAccess.Models;

/// <summary>
/// Represents the similarity evaluation output.
/// </summary>
public record SimilarityOutput(
    double Similarity,
    double GptSimilarity,
    string SimilarityResult,
    double SimilarityThreshold
);
