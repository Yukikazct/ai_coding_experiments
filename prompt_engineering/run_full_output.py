"""Run all 6 prompt tests and save FULL model outputs."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ollama import chat
from dotenv import load_dotenv
load_dotenv()

def run_test(name, model, system_prompt, user_prompt, output_file):
    print(f"\n{'='*60}")
    print(f"Running: {name}")
    print(f"{'='*60}")

    response = chat(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        options={"temperature": 0.5},
    )

    full_output = response.message.content

    with open(output_file, "w") as f:
        f.write(f"Test: {name}\n")
        f.write(f"Model: {model}\n")
        f.write(f"System Prompt:\n{system_prompt}\n\n")
        f.write(f"User Prompt:\n{user_prompt}\n\n")
        f.write(f"Model Output:\n{full_output}\n")

    print(f"Saved to {output_file}")
    print(f"Output preview: {full_output[:200]}...")
    return full_output


# 1. K-shot
import k_shot_prompting as ksp
run_test("K-shot Prompting", "mistral-nemo:12b",
         ksp.YOUR_SYSTEM_PROMPT, ksp.USER_PROMPT, "output_k_shot.txt")

# 2. Chain of Thought
import chain_of_thought as cot
run_test("Chain of Thought", "llama3.1:8b",
         cot.YOUR_SYSTEM_PROMPT, cot.USER_PROMPT, "output_cot.txt")

# 3. Tool Calling
import tool_calling as tc
run_test("Tool Calling", "llama3.1:8b",
         tc.YOUR_SYSTEM_PROMPT, "Call the tool now.", "output_tool_calling.txt")

# 4. Self-consistency — run 5 times
import self_consistency_prompting as scp
with open("output_self_consistency.txt", "w") as f:
    f.write(f"Test: Self-Consistency Prompting\n")
    f.write(f"Model: llama3.1:8b\n")
    f.write(f"System Prompt:\n{scp.YOUR_SYSTEM_PROMPT}\n\n")
    f.write(f"User Prompt:\n{scp.USER_PROMPT}\n\n")
    f.write(f"Expected: {scp.EXPECTED_OUTPUT}\n\n")

    for i in range(5):
        response = chat(
            model="llama3.1:8b",
            messages=[
                {"role": "system", "content": scp.YOUR_SYSTEM_PROMPT},
                {"role": "user", "content": scp.USER_PROMPT},
            ],
            options={"temperature": 1},
        )
        f.write(f"--- Run {i+1} ---\n")
        f.write(f"{response.message.content}\n\n")
    f.write("(Majority vote determined by test script)\n")
print("Self-consistency saved to output_self_consistency.txt")

# 5. RAG
import rag as rag_mod
context = rag_mod.YOUR_CONTEXT_PROVIDER(rag_mod.CORPUS)
user_prompt = rag_mod.make_user_prompt(rag_mod.QUESTION, context)
run_test("RAG", "llama3.1:8b",
         rag_mod.YOUR_SYSTEM_PROMPT, user_prompt, "output_rag.txt")

# 6. Reflexion
import reflexion as refl
# Initial generation
resp1 = chat(
    model="llama3.1:8b",
    messages=[
        {"role": "system", "content": refl.SYSTEM_PROMPT},
        {"role": "user", "content": "Provide the implementation now."},
    ],
    options={"temperature": 0.2},
)
initial_code = refl.extract_code_block(resp1.message.content)

with open("output_reflexion.txt", "w") as f:
    f.write(f"Test: Reflexion\n")
    f.write(f"Model: llama3.1:8b\n\n")
    f.write(f"Initial System Prompt:\n{refl.SYSTEM_PROMPT}\n\n")
    f.write(f"=== Initial Generation ===\n")
    f.write(f"Full response:\n{resp1.message.content}\n\n")
    f.write(f"Extracted code:\n{initial_code}\n\n")

    # Evaluate
    func = refl.load_function_from_code(initial_code)
    passed, failures = refl.evaluate_function(func)
    f.write(f"Tests passed: {passed}\n")
    if failures:
        f.write(f"Failures:\n")
        for fail in failures:
            f.write(f"  - {fail}\n")

    # Reflexion step
    if not passed:
        ctx = refl.your_build_reflexion_context(initial_code, failures)
        f.write(f"\n=== Reflexion Step ===\n")
        f.write(f"Reflexion System Prompt:\n{refl.YOUR_REFLEXION_PROMPT}\n\n")
        f.write(f"Reflexion Context:\n{ctx}\n\n")

        resp2 = chat(
            model="llama3.1:8b",
            messages=[
                {"role": "system", "content": refl.YOUR_REFLEXION_PROMPT},
                {"role": "user", "content": ctx},
            ],
            options={"temperature": 0.2},
        )
        improved_code = refl.extract_code_block(resp2.message.content)
        f.write(f"Full reflexion response:\n{resp2.message.content}\n\n")
        f.write(f"Extracted improved code:\n{improved_code}\n")

print("Reflexion saved to output_reflexion.txt")
print("\nDone!")
