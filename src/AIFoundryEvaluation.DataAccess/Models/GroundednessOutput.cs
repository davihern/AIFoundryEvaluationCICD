namespace AIFoundryEvaluation.DataAccess.Models;

/// <summary>
/// Represents the groundedness evaluation output.
/// </summary>
public record GroundednessOutput(
    double Groundedness,
    double GptGroundedness,
    string GroundednessReason,
    string GroundednessResult,
    double GroundednessThreshold
);
