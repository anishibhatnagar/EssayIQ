import { useState } from "react";
import "./App.css";

function App() {
  const [title, setTitle] = useState("");
  const [essay, setEssay] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleAnalyze = async () => {
    if (!essay.trim()) {
      setError("Please enter an essay first.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(
  `${import.meta.env.VITE_API_URL}/api/analyze`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            essay: essay,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Analysis failed.");
      }

      setResult(data);
    } catch (err) {
      setError(
        "Could not connect to the EssayIQ backend. Make sure Flask is running."
      );
    } finally {
      setLoading(false);
    }
  };

  const wordCount = essay.trim()
    ? essay.trim().split(/\s+/).length
    : 0;

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="logo">EssayIQ</div>
        <div className="tagline">
          AI-Powered Essay Analysis
        </div>
      </header>

      <main className="main-container">

        {/* Hero */}
        <section className="hero">
          <h1>Improve Your Writing with EssayIQ</h1>

          <p>
            Analyze your essay for readability, vocabulary,
            structure, and overall writing quality.
          </p>
        </section>

        {/* Essay Input */}
        <section className="essay-card">

          <label htmlFor="title">
            Essay Title
          </label>

          <input
            id="title"
            type="text"
            placeholder="Enter your essay title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />

          <label htmlFor="essay">
            Your Essay
          </label>

          <textarea
            id="essay"
            placeholder="Paste or write your essay here..."
            value={essay}
            onChange={(e) => setEssay(e.target.value)}
          />

          <div className="word-count">
            Words: {wordCount}
          </div>

          {error && (
            <div className="error">
              {error}
            </div>
          )}

          <button
            onClick={handleAnalyze}
            disabled={loading}
          >
            {loading ? "Analyzing..." : "Analyze Essay"}
          </button>

        </section>

        {/* Results */}
        {result && (
          <section className="results">

            <h2>Essay Analysis</h2>

            {/* Overall Score */}
            <div className="score-card">
              <div className="score-label">
                Overall Score
              </div>

              <div className="overall-score">
                {result.overall_score}
              </div>

              <div className="score-out-of">
                / 100
              </div>
            </div>

            {/* Statistics */}
            <div className="stats-grid">

              <div className="stat-card">
                <span>Words</span>
                <strong>
                  {result.word_count}
                </strong>
              </div>

              <div className="stat-card">
                <span>Sentences</span>
                <strong>
                  {result.sentence_count}
                </strong>
              </div>

              <div className="stat-card">
                <span>Paragraphs</span>
                <strong>
                  {result.paragraph_count}
                </strong>
              </div>

              <div className="stat-card">
                <span>Avg. Sentence Length</span>
                <strong>
                  {result.average_sentence_length}
                </strong>
              </div>

            </div>

            {/* Scores */}
            <div className="analysis-card">

              <h3>Writing Scores</h3>

              <ScoreBar
                label="Readability"
                score={result.readability_score}
              />

              <ScoreBar
                label="Vocabulary"
                score={result.vocabulary_score}
              />

              <ScoreBar
                label="Sentence Quality"
                score={result.sentence_score}
              />

              <div className="vocabulary">
                <strong>
                  Vocabulary Diversity:
                </strong>{" "}
                {result.vocabulary_diversity}%
              </div>

            </div>

            {/* Strengths */}
            <div className="analysis-card">

              <h3>Strengths</h3>

              {result.strengths.length > 0 ? (
                <ul>
                  {result.strengths.map(
                    (item, index) => (
                      <li key={index}>
                        ✓ {item}
                      </li>
                    )
                  )}
                </ul>
              ) : (
                <p>
                  No major strengths detected yet.
                </p>
              )}

            </div>

            {/* Improvements */}
            <div className="analysis-card">

              <h3>Areas to Improve</h3>

              {result.improvements.length > 0 ? (
                <ul>
                  {result.improvements.map(
                    (item, index) => (
                      <li key={index}>
                        ⚠ {item}
                      </li>
                    )
                  )}
                </ul>
              ) : (
                <p>
                  Your essay looks good!
                </p>
              )}

            </div>

            {/* Repeated Words */}
            {result.repeated_words.length > 0 && (
              <div className="analysis-card">

                <h3>Frequently Used Words</h3>

                <div className="word-list">

                  {result.repeated_words.map(
                    (item, index) => (
                      <div
                        className="word-item"
                        key={index}
                      >
                        <span>
                          {item.word}
                        </span>

                        <strong>
                          {item.count}
                        </strong>
                      </div>
                    )
                  )}

                </div>

              </div>
            )}

          </section>
        )}

      </main>

      <footer>
        <p>EssayIQ © 2026</p>
      </footer>
    </div>
  );
}


/* Score Bar Component */

function ScoreBar({ label, score }) {
  return (
    <div className="score-bar-container">

      <div className="score-bar-header">
        <span>{label}</span>
        <strong>{score}/100</strong>
      </div>

      <div className="score-bar">
        <div
          className="score-fill"
          style={{ width: `${score}%` }}
        ></div>
      </div>

    </div>
  );
}


export default App;