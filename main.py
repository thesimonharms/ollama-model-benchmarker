import json
import argparse
from ollama_client import OllamaClient
from evaluators.regex_evaluator import RegexEvaluator
from evaluators.json_schema_evaluator import JsonSchemaEvaluator
from evaluators.unit_test_evaluator import UnitTestEvaluator

def main():
    parser = argparse.ArgumentParser(description="Ollama Code Benchmarker")
    parser.add_argument("--model", required=True, help="Model name to benchmark (e.g., llama3)")
    args = parser.parse_args()

    client = OllamaClient()
    
    with open("suite/tests.json", "r") as f:
        tests = json.load(f)

    evaluators = {
        "regex": RegexEvaluator(),
        "json_schema": JsonSchemaEvaluator(),
        "unit_test": UnitTestEvaluator()
    }

    total_score = 0
    max_points = sum(t["points"] for t in tests)
    results = []

    print(f"\n🚀 Benchmarking model: {args.model}")
    print("-" * 60)

    for test in tests:
        print(f"Running {test['id']} ({test['category']})...", end=" ", flush=True)
        
        response = client.chat(
            model=args.model,
            messages=[
                {"role": "system", "content": test.get("system_prompt", "")},
                {"role": "user", "content": test["prompt"]}
            ],
            options={"num_predict": 1024}
        )

        evaluator = evaluators.get(test["evaluator"])
        success = False
        if evaluator:
            try:
                success = evaluator.evaluate(response, test["expected"])
            except Exception as e:
                print(f"\nEvaluation error for {test['id']}: {e}")
                success = False
        
        points_earned = test["points"] if success else 0
        total_score += points_earned
        
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status} | {points_earned}/{test['points']} pts")
        
        results.append({
            "id": test["id"],
            "category": test["category"],
            "success": success,
            "points": points_earned
        })

        # PERSIST AFTER EVERY TEST
        with open(f"tests_output/results_{args.model}.json", "w") as f:
            json.dump({
                "model": args.model, 
                "total_score": total_score, 
                "max_points": max_points, 
                "details": results
            }, f, indent=2)

    # Category breakdown
    categories = {}
    for res in results:
        cat = next(t["category"] for t in tests if t["id"] == res["id"])
        pts = res["points"]
        max_p = next(t["points"] for t in tests if t["id"] == res["id"])
        categories.setdefault(cat, {"earned": 0, "max": 0})
        categories[cat]["earned"] += pts
        categories[cat]["max"] += max_p

    print("-" * 60)
    print("\n📊 CATEGORY BREAKDOWN")
    for cat, scores in categories.items():
        percentage = (scores["earned"] / scores["max"]) * 100 if scores["max"] > 0 else 0
        print(f"{cat:25} | {scores['earned']}/{scores['max']} pts ({percentage:.1f}%)")

    final_score = total_score 
    print("-" * 60)
    print(f"\n🏆 FINAL SCORE: {final_score} / {max_points}")
    print("-" * 60)

if __name__ == "__main__":
    main()
