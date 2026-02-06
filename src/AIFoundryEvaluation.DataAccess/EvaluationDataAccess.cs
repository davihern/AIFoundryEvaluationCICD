using System.Text.Json;
using System.Text.Json.Serialization;
using AIFoundryEvaluation.DataAccess.Models;

namespace AIFoundryEvaluation.DataAccess;

/// <summary>
/// Provides data access methods for reading and querying AI Foundry evaluation results.
/// </summary>
public class EvaluationDataAccess
{
    private static readonly JsonSerializerOptions JsonOptions = new()
    {
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
        PropertyNameCaseInsensitive = true,
        Converters = { new EvaluationResultConverter() }
    };

    /// <summary>
    /// Reads evaluation results from a JSON file asynchronously.
    /// </summary>
    /// <param name="filePath">The path to the JSON file containing evaluation results.</param>
    /// <param name="cancellationToken">A cancellation token to cancel the operation.</param>
    /// <returns>An <see cref="EvaluationResultDocument"/> containing the evaluation results.</returns>
    /// <exception cref="ArgumentException">Thrown when filePath is null or whitespace.</exception>
    /// <exception cref="FileNotFoundException">Thrown when the specified file does not exist.</exception>
    public async Task<EvaluationResultDocument> ReadEvaluationResultsAsync(
        string filePath,
        CancellationToken cancellationToken = default)
    {
        if (string.IsNullOrWhiteSpace(filePath))
        {
            throw new ArgumentException("File path cannot be null or whitespace.", nameof(filePath));
        }

        if (!File.Exists(filePath))
        {
            throw new FileNotFoundException($"Evaluation results file not found: {filePath}", filePath);
        }

        await using var fileStream = File.OpenRead(filePath);
        using var jsonDocument = await JsonDocument.ParseAsync(fileStream, default, cancellationToken)
            .ConfigureAwait(false);

        var rows = jsonDocument.RootElement.GetProperty("rows");
        var results = new List<EvaluationResult>();

        foreach (var row in rows.EnumerateArray())
        {
            var result = ParseEvaluationResult(row);
            results.Add(result);
        }

        return new EvaluationResultDocument(results);
    }

    /// <summary>
    /// Filters evaluation results based on groundedness threshold.
    /// </summary>
    /// <param name="document">The evaluation result document to filter.</param>
    /// <param name="minimumGroundedness">The minimum groundedness score to include.</param>
    /// <returns>A filtered list of evaluation results.</returns>
    public IReadOnlyList<EvaluationResult> FilterByGroundedness(
        EvaluationResultDocument document,
        double minimumGroundedness)
    {
        ArgumentNullException.ThrowIfNull(document);

        return document.Rows
            .Where(r => r.Outputs.Groundedness?.Groundedness >= minimumGroundedness)
            .ToList();
    }

    /// <summary>
    /// Filters evaluation results that have failed groundedness evaluation.
    /// </summary>
    /// <param name="document">The evaluation result document to filter.</param>
    /// <returns>A filtered list of failed evaluation results.</returns>
    public IReadOnlyList<EvaluationResult> GetFailedResults(EvaluationResultDocument document)
    {
        ArgumentNullException.ThrowIfNull(document);

        return document.Rows
            .Where(r => r.Outputs.Groundedness?.GroundednessResult.Equals("fail", StringComparison.OrdinalIgnoreCase) == true ||
                       r.Outputs.Similarity?.SimilarityResult.Equals("fail", StringComparison.OrdinalIgnoreCase) == true)
            .ToList();
    }

    /// <summary>
    /// Gets evaluation results that passed all checks.
    /// </summary>
    /// <param name="document">The evaluation result document to filter.</param>
    /// <returns>A filtered list of passed evaluation results.</returns>
    public IReadOnlyList<EvaluationResult> GetPassedResults(EvaluationResultDocument document)
    {
        ArgumentNullException.ThrowIfNull(document);

        return document.Rows
            .Where(r => r.Outputs.Groundedness?.GroundednessResult.Equals("pass", StringComparison.OrdinalIgnoreCase) == true &&
                       r.Outputs.Similarity?.SimilarityResult.Equals("pass", StringComparison.OrdinalIgnoreCase) == true)
            .ToList();
    }

    private static EvaluationResult ParseEvaluationResult(JsonElement row)
    {
        var inputs = new EvaluationInput(
            Query: GetStringProperty(row, "inputs.query") ?? string.Empty,
            GroundTruth: GetStringProperty(row, "inputs.ground_truth"),
            Response: GetStringProperty(row, "inputs.response"),
            Context: GetStringProperty(row, "inputs.context"),
            Latency: GetDoubleProperty(row, "inputs.latency"),
            ResponseLength: GetIntProperty(row, "inputs.response_length")
        );

        GroundednessOutput? groundedness = null;
        if (row.TryGetProperty("outputs.groundedness.groundedness", out _))
        {
            groundedness = new GroundednessOutput(
                Groundedness: GetDoubleProperty(row, "outputs.groundedness.groundedness") ?? 0,
                GptGroundedness: GetDoubleProperty(row, "outputs.groundedness.gpt_groundedness") ?? 0,
                GroundednessReason: GetStringProperty(row, "outputs.groundedness.groundedness_reason") ?? string.Empty,
                GroundednessResult: GetStringProperty(row, "outputs.groundedness.groundedness_result") ?? string.Empty,
                GroundednessThreshold: GetDoubleProperty(row, "outputs.groundedness.groundedness_threshold") ?? 0
            );
        }

        SimilarityOutput? similarity = null;
        if (row.TryGetProperty("outputs.similarity.similarity", out _))
        {
            similarity = new SimilarityOutput(
                Similarity: GetDoubleProperty(row, "outputs.similarity.similarity") ?? 0,
                GptSimilarity: GetDoubleProperty(row, "outputs.similarity.gpt_similarity") ?? 0,
                SimilarityResult: GetStringProperty(row, "outputs.similarity.similarity_result") ?? string.Empty,
                SimilarityThreshold: GetDoubleProperty(row, "outputs.similarity.similarity_threshold") ?? 0
            );
        }

        var outputs = new EvaluationOutput(groundedness, similarity);
        var lineNumber = GetIntProperty(row, "line_number") ?? 0;

        return new EvaluationResult(inputs, outputs, lineNumber);
    }

    private static string? GetStringProperty(JsonElement element, string propertyName)
    {
        return element.TryGetProperty(propertyName, out var property) && property.ValueKind == JsonValueKind.String
            ? property.GetString()
            : null;
    }

    private static double? GetDoubleProperty(JsonElement element, string propertyName)
    {
        return element.TryGetProperty(propertyName, out var property) && property.ValueKind == JsonValueKind.Number
            ? property.GetDouble()
            : null;
    }

    private static int? GetIntProperty(JsonElement element, string propertyName)
    {
        return element.TryGetProperty(propertyName, out var property) && property.ValueKind == JsonValueKind.Number
            ? property.GetInt32()
            : null;
    }
}

/// <summary>
/// Custom JSON converter for evaluation results.
/// </summary>
internal class EvaluationResultConverter : JsonConverter<EvaluationResult>
{
    public override EvaluationResult? Read(ref Utf8JsonReader reader, Type typeToConvert, JsonSerializerOptions options)
    {
        throw new NotImplementedException("Direct deserialization is not supported. Use EvaluationDataAccess methods.");
    }

    public override void Write(Utf8JsonWriter writer, EvaluationResult value, JsonSerializerOptions options)
    {
        throw new NotImplementedException("Serialization is not currently supported.");
    }
}
