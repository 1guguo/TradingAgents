"""Financial situation memory using BM25 for lexical similarity matching.

Uses BM25 (Best Matching 25) algorithm for retrieval - no API calls,
no token limits, works offline with any LLM provider.
"""

from rank_bm25 import BM25Okapi
from typing import List, Tuple
import re


class FinancialSituationMemory:
    """Memory system for storing and retrieving financial situations using BM25."""

    def __init__(self, name: str, config: dict = None):
        """Initialize the memory system.

        Args:
            name: Name identifier for this memory instance
            config: Configuration dict (kept for API compatibility, not used for BM25)
        """
        self.name = name
        self.documents: List[str] = []
        self.recommendations: List[str] = []
        self.bm25 = None

    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text for BM25 indexing.

        Simple whitespace + punctuation tokenization with lowercasing.
        """
        # Lowercase and split on non-alphanumeric characters
        tokens = re.findall(r"\b\w+\b", text.lower())
        return tokens

    def _rebuild_index(self):
        """Rebuild the BM25 index after adding documents."""
        if self.documents:
            tokenized_docs = [self._tokenize(doc) for doc in self.documents]
            self.bm25 = BM25Okapi(tokenized_docs)
        else:
            self.bm25 = None

    def add_situations(self, situations_and_advice: List[Tuple[str, str]]):
        """Add financial situations and their corresponding advice.

        Args:
            situations_and_advice: List of tuples (situation, recommendation)
        """
        for situation, recommendation in situations_and_advice:
            self.documents.append(situation)
            self.recommendations.append(recommendation)

        # Rebuild BM25 index with new documents
        self._rebuild_index()

    def get_memories(self, current_situation: str, n_matches: int = 1) -> List[dict]:
        """Find matching recommendations using BM25 similarity.

        Args:
            current_situation: The current financial situation to match against
            n_matches: Number of top matches to return

        Returns:
            List of dicts with matched_situation, recommendation, and similarity_score
        """
        if not self.documents or self.bm25 is None:
            return []

        # Tokenize query
        query_tokens = self._tokenize(current_situation)

        # Get BM25 scores for all documents
        scores = self.bm25.get_scores(query_tokens)

        # Get top-n indices sorted by score (descending)
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[
            :n_matches
        ]

        # Build results
        results = []
        max_score = max(scores) if max(scores) > 0 else 1  # Normalize scores

        for idx in top_indices:
            # Normalize score to 0-1 range for consistency
            normalized_score = scores[idx] / max_score if max_score > 0 else 0
            results.append(
                {
                    "matched_situation": self.documents[idx],
                    "recommendation": self.recommendations[idx],
                    "similarity_score": normalized_score,
                }
            )

        return results

    def clear(self):
        """Clear all stored memories."""
        self.documents = []
        self.recommendations = []
        self.bm25 = None

    def save(self, filepath: str = None):
        """Save memory to a JSON file.

        Args:
            filepath: Path to save the memory. If None, uses default path.
        """
        import json
        from pathlib import Path

        if filepath is None:
            # Default: save to ~/.tradingagents/memories/{name}.json
            home_dir = Path.home() / ".tradingagents" / "memories"
            home_dir.mkdir(parents=True, exist_ok=True)
            filepath = str(home_dir / f"{self.name}.json")

        data = {
            "name": self.name,
            "documents": self.documents,
            "recommendations": self.recommendations,
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"Memory saved to: {filepath}")

    @classmethod
    def load(cls, name: str, filepath: str = None):
        """Load memory from a JSON file.

        Args:
            name: Name identifier for this memory instance
            filepath: Path to load the memory from. If None, uses default path.

        Returns:
            FinancialSituationMemory instance with loaded data
        """
        import json
        from pathlib import Path

        if filepath is None:
            home_dir = Path.home() / ".tradingagents" / "memories"
            filepath = str(home_dir / f"{name}.json")

        memory = cls(name, {})

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            memory.documents = data.get("documents", [])
            memory.recommendations = data.get("recommendations", [])
            memory._rebuild_index()

            print(
                f"Memory loaded from: {filepath} ({len(memory.documents)} situations)"
            )
        except FileNotFoundError:
            print(f"No existing memory found at: {filepath}, starting fresh")

        return memory


if __name__ == "__main__":
    # Example usage
    matcher = FinancialSituationMemory("test_memory")

    # Example data
    example_data = [
        (
            "High inflation rate with rising interest rates and declining consumer spending",
            "Consider defensive sectors like consumer staples and utilities. Review fixed-income portfolio duration.",
        ),
        (
            "Tech sector showing high volatility with increasing institutional selling pressure",
            "Reduce exposure to high-growth tech stocks. Look for value opportunities in established tech companies with strong cash flows.",
        ),
        (
            "Strong dollar affecting emerging markets with increasing forex volatility",
            "Hedge currency exposure in international positions. Consider reducing allocation to emerging market debt.",
        ),
        (
            "Market showing signs of sector rotation with rising yields",
            "Rebalance portfolio to maintain target allocations. Consider increasing exposure to sectors benefiting from higher rates.",
        ),
    ]
    """
    example_data = [
    (
        "高通胀率叠加利率上升与消费支出下降",
        "考虑配置必需消费品、公用事业等防御性板块。调整固定收益投资组合久期。",
    ),
    (
        "科技板块波动性高企，机构抛售压力加剧",
        "减持高成长科技股。在现金流强劲的成熟科技企业中寻找价值投资机会。",
    ),
    (
        "美元走强影响新兴市场，外汇波动性上升",
        "对跨境投资头寸进行汇率对冲。考虑降低对新兴市场债券的配置。",
    ),
    (
        "市场显现板块轮动迹象，收益率持续上行",
        "对投资组合进行再平衡以维持目标配置比例。考虑增配受益于高利率的板块。",
    ),
]
    
    """
    # Add the example situations and recommendations
    matcher.add_situations(example_data)

    # Example query
    current_situation = """
    Market showing increased volatility in tech sector, with institutional investors
    reducing positions and rising interest rates affecting growth stock valuations
    """

    try:
        recommendations = matcher.get_memories(current_situation, n_matches=2)

        for i, rec in enumerate(recommendations, 1):
            print(f"\nMatch {i}:")
            print(f"Similarity Score: {rec['similarity_score']:.2f}")
            print(f"Matched Situation: {rec['matched_situation']}")
            print(f"Recommendation: {rec['recommendation']}")

    except Exception as e:
        print(f"Error during recommendation: {str(e)}")
