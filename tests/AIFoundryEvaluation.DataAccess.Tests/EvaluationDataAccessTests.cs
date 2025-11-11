using AIFoundryEvaluation.DataAccess;
using AIFoundryEvaluation.DataAccess.Models;

namespace AIFoundryEvaluation.DataAccess.Tests;

public class EvaluationDataAccessTests
{
    private readonly EvaluationDataAccess _dataAccess;

    public EvaluationDataAccessTests()
    {
        _dataAccess = new EvaluationDataAccess();
    }

    [Fact]
    public async Task ReadEvaluationResultsAsync_WithValidFile_ReturnsDocument()
    {
        // Arrange
        var testFilePath = CreateTestJsonFile();

        try
        {
            // Act
            var result = await _dataAccess.ReadEvaluationResultsAsync(testFilePath);

            // Assert
            Assert.NotNull(result);
            Assert.NotEmpty(result.Rows);
            Assert.Equal(2, result.Rows.Count);
        }
        finally
        {
            // Cleanup
            if (File.Exists(testFilePath))
            {
                File.Delete(testFilePath);
            }
        }
    }

    [Fact]
    public async Task ReadEvaluationResultsAsync_WithNullFilePath_ThrowsArgumentException()
    {
        // Act & Assert
        await Assert.ThrowsAsync<ArgumentException>(
            () => _dataAccess.ReadEvaluationResultsAsync(null!));
    }

    [Fact]
    public async Task ReadEvaluationResultsAsync_WithEmptyFilePath_ThrowsArgumentException()
    {
        // Act & Assert
        await Assert.ThrowsAsync<ArgumentException>(
            () => _dataAccess.ReadEvaluationResultsAsync(string.Empty));
    }

    [Fact]
    public async Task ReadEvaluationResultsAsync_WithWhitespaceFilePath_ThrowsArgumentException()
    {
        // Act & Assert
        await Assert.ThrowsAsync<ArgumentException>(
            () => _dataAccess.ReadEvaluationResultsAsync("   "));
    }

    [Fact]
    public async Task ReadEvaluationResultsAsync_WithNonExistentFile_ThrowsFileNotFoundException()
    {
        // Act & Assert
        await Assert.ThrowsAsync<FileNotFoundException>(
            () => _dataAccess.ReadEvaluationResultsAsync("/non/existent/file.json"));
    }

    [Fact]
    public async Task ReadEvaluationResultsAsync_ParsesInputsCorrectly()
    {
        // Arrange
        var testFilePath = CreateTestJsonFile();

        try
        {
            // Act
            var result = await _dataAccess.ReadEvaluationResultsAsync(testFilePath);

            // Assert
            var firstRow = result.Rows[0];
            Assert.Equal("What is the test query?", firstRow.Inputs.Query);
            Assert.Equal("Test ground truth", firstRow.Inputs.GroundTruth);
            Assert.Equal("Test response", firstRow.Inputs.Response);
            Assert.Equal("Test context", firstRow.Inputs.Context);
            Assert.Equal(8.5, firstRow.Inputs.Latency);
            Assert.Equal(100, firstRow.Inputs.ResponseLength);
        }
        finally
        {
            if (File.Exists(testFilePath))
            {
                File.Delete(testFilePath);
            }
        }
    }

    [Fact]
    public async Task ReadEvaluationResultsAsync_ParsesGroundednessOutputCorrectly()
    {
        // Arrange
        var testFilePath = CreateTestJsonFile();

        try
        {
            // Act
            var result = await _dataAccess.ReadEvaluationResultsAsync(testFilePath);

            // Assert
            var firstRow = result.Rows[0];
            Assert.NotNull(firstRow.Outputs.Groundedness);
            Assert.Equal(5.0, firstRow.Outputs.Groundedness.Groundedness);
            Assert.Equal(5.0, firstRow.Outputs.Groundedness.GptGroundedness);
            Assert.Equal("pass", firstRow.Outputs.Groundedness.GroundednessResult);
            Assert.Equal(3.0, firstRow.Outputs.Groundedness.GroundednessThreshold);
        }
        finally
        {
            if (File.Exists(testFilePath))
            {
                File.Delete(testFilePath);
            }
        }
    }

    [Fact]
    public async Task ReadEvaluationResultsAsync_ParsesSimilarityOutputCorrectly()
    {
        // Arrange
        var testFilePath = CreateTestJsonFile();

        try
        {
            // Act
            var result = await _dataAccess.ReadEvaluationResultsAsync(testFilePath);

            // Assert
            var firstRow = result.Rows[0];
            Assert.NotNull(firstRow.Outputs.Similarity);
            Assert.Equal(4.0, firstRow.Outputs.Similarity.Similarity);
            Assert.Equal(4.0, firstRow.Outputs.Similarity.GptSimilarity);
            Assert.Equal("pass", firstRow.Outputs.Similarity.SimilarityResult);
            Assert.Equal(3.0, firstRow.Outputs.Similarity.SimilarityThreshold);
        }
        finally
        {
            if (File.Exists(testFilePath))
            {
                File.Delete(testFilePath);
            }
        }
    }

    [Fact]
    public void FilterByGroundedness_WithValidThreshold_ReturnsFilteredResults()
    {
        // Arrange
        var document = CreateTestDocument();

        // Act
        var result = _dataAccess.FilterByGroundedness(document, 4.0);

        // Assert
        Assert.Single(result);
        Assert.Equal(5.0, result[0].Outputs.Groundedness?.Groundedness);
    }

    [Fact]
    public void FilterByGroundedness_WithNullDocument_ThrowsArgumentNullException()
    {
        // Act & Assert
        Assert.Throws<ArgumentNullException>(
            () => _dataAccess.FilterByGroundedness(null!, 3.0));
    }

    [Fact]
    public void GetFailedResults_ReturnsOnlyFailedResults()
    {
        // Arrange
        var document = CreateTestDocument();

        // Act
        var result = _dataAccess.GetFailedResults(document);

        // Assert
        Assert.Single(result);
        Assert.Equal("fail", result[0].Outputs.Groundedness?.GroundednessResult);
    }

    [Fact]
    public void GetFailedResults_WithNullDocument_ThrowsArgumentNullException()
    {
        // Act & Assert
        Assert.Throws<ArgumentNullException>(
            () => _dataAccess.GetFailedResults(null!));
    }

    [Fact]
    public void GetPassedResults_ReturnsOnlyPassedResults()
    {
        // Arrange
        var document = CreateTestDocument();

        // Act
        var result = _dataAccess.GetPassedResults(document);

        // Assert
        Assert.Single(result);
        Assert.Equal("pass", result[0].Outputs.Groundedness?.GroundednessResult);
        Assert.Equal("pass", result[0].Outputs.Similarity?.SimilarityResult);
    }

    [Fact]
    public void GetPassedResults_WithNullDocument_ThrowsArgumentNullException()
    {
        // Act & Assert
        Assert.Throws<ArgumentNullException>(
            () => _dataAccess.GetPassedResults(null!));
    }

    private static string CreateTestJsonFile()
    {
        var tempFile = Path.Combine(Path.GetTempPath(), $"test_eval_{Guid.NewGuid()}.json");
        var json = """
        {
          "rows": [
            {
              "inputs.query": "What is the test query?",
              "inputs.ground_truth": "Test ground truth",
              "inputs.response": "Test response",
              "inputs.context": "Test context",
              "inputs.latency": 8.5,
              "inputs.response_length": 100,
              "outputs.groundedness.groundedness": 5.0,
              "outputs.groundedness.gpt_groundedness": 5.0,
              "outputs.groundedness.groundedness_reason": "Test reason",
              "outputs.groundedness.groundedness_result": "pass",
              "outputs.groundedness.groundedness_threshold": 3.0,
              "outputs.similarity.similarity": 4.0,
              "outputs.similarity.gpt_similarity": 4.0,
              "outputs.similarity.similarity_result": "pass",
              "outputs.similarity.similarity_threshold": 3.0,
              "line_number": 0
            },
            {
              "inputs.query": "Second query?",
              "inputs.ground_truth": "Second ground truth",
              "inputs.response": "Second response",
              "inputs.context": "Second context",
              "inputs.latency": 7.2,
              "inputs.response_length": 150,
              "outputs.groundedness.groundedness": 2.0,
              "outputs.groundedness.gpt_groundedness": 2.0,
              "outputs.groundedness.groundedness_reason": "Failed reason",
              "outputs.groundedness.groundedness_result": "fail",
              "outputs.groundedness.groundedness_threshold": 3.0,
              "outputs.similarity.similarity": 3.5,
              "outputs.similarity.gpt_similarity": 3.5,
              "outputs.similarity.similarity_result": "pass",
              "outputs.similarity.similarity_threshold": 3.0,
              "line_number": 1
            }
          ]
        }
        """;

        File.WriteAllText(tempFile, json);
        return tempFile;
    }

    private static EvaluationResultDocument CreateTestDocument()
    {
        var passedResult = new EvaluationResult(
            new EvaluationInput("Query1", "GT1", "Resp1", "Ctx1", 8.5, 100),
            new EvaluationOutput(
                new GroundednessOutput(5.0, 5.0, "Good", "pass", 3.0),
                new SimilarityOutput(4.0, 4.0, "pass", 3.0)
            ),
            0
        );

        var failedResult = new EvaluationResult(
            new EvaluationInput("Query2", "GT2", "Resp2", "Ctx2", 7.2, 150),
            new EvaluationOutput(
                new GroundednessOutput(2.0, 2.0, "Bad", "fail", 3.0),
                new SimilarityOutput(3.5, 3.5, "pass", 3.0)
            ),
            1
        );

        return new EvaluationResultDocument(new[] { passedResult, failedResult });
    }
}
