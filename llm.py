import streamlit as st
from datetime import datetime

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="LLM Quality Enhancement Demo",
    layout="wide"
)

st.title("🚀 LLM Quality Enhancement using Content Taxonomy")

st.caption(
    "Demonstrating how structured taxonomy + prompt design improves output quality "
    "irrespective of the LLM model used."
)

# ---------------- USER PROFILE (MOCK) ---------------- #
st.sidebar.header("👤 User Profile")

user_profile = {
    "name": "John",
    "role": st.sidebar.selectbox(
        "Role",
        ["Backend Engineer", "Data Engineer", "Student"]
    ),
    "skills": st.sidebar.multiselect(
        "Skills",
        ["Kafka", "Java", "Spring Boot", "Python", "SQL"],
        default=["Kafka"]
    ),
    "experience": st.sidebar.selectbox(
        "Experience Level",
        ["Beginner", "Intermediate", "Advanced"],
        index=1
    ),
    "content_type_selection": st.sidebar.selectbox(
        "Content Type",
        ["Training", "Assessment", "Explanation"],
        index=0
    )
}

# ---------------- USER QUERY ---------------- #
st.header("🧠 User Query")

user_query = st.text_input(
    "Ask for training / assessment / explanation",
    value="Kafka training"
)

# ---------------- TAXONOMY ENGINE ---------------- #
def build_taxonomy(query, profile):
    # Use content type from user selection
    content_type = profile.get("content_type_selection", "Training")
    
    learning_goal = {
        "Training": "Hands-on learning",
        "Assessment": "Evaluate understanding",
        "Explanation": "Conceptual clarity"
    }.get(content_type, "Hands-on learning")
    
    # Decide skill focus (if multiple selected, pick first, else General)
    skill_focus = profile["skills"][0] if profile["skills"] else "General"
    
    # Adjust difficulty based on experience
    difficulty = profile["experience"]
    
    taxonomy = {
        "skill": skill_focus,
        "content_type": content_type,
        "difficulty": difficulty,
        "user_role": profile["role"],
        "learning_goal": learning_goal,
        "output_format": "Structured",
        "context_depth": "High",
        "model_dependency": "None (Model-Agnostic)",
        "query": query
    }
    
    return taxonomy

# ---------------- PROMPT GENERATOR ---------------- #
def generate_prompt(taxonomy):
    if taxonomy["content_type"] == "Training":
        prompt = f"""
You are an expert technical instructor.

Create a {taxonomy['difficulty']} level TRAINING module for:
Skill: {taxonomy['skill']}
User Role: {taxonomy['user_role']}

Requirements:
- Clear learning objectives
- Concept explanation with real-world examples
- Hands-on exercises
- Common mistakes to avoid
- Quick self-check questions

Avoid generic explanations.
Focus on applied understanding.
"""
    elif taxonomy["content_type"] == "Assessment":
        prompt = f"""
You are a senior technical evaluator.

Create a {taxonomy['difficulty']} level ASSESSMENT for:
Skill: {taxonomy['skill']}

Requirements:
- 2 conceptual questions
- 1 scenario-based question
- Expected answer points
- Evaluation rubric (0–5 scale)

Ensure questions test real understanding, not memorization.
"""
    else:
        prompt = f"""
You are a senior technical mentor.

Explain the following topic clearly:
Skill: {taxonomy['skill']}

Requirements:
- Simple explanation
- Architecture overview
- Real-world use cases
- Career relevance

Keep it structured and concise.
"""

    return prompt.strip()

# ---------------- MOCK LLM OUTPUT (QUALITY FOCUSED) ---------------- #
def mock_llm_response(taxonomy):
    skill = taxonomy["skill"]
    difficulty = taxonomy["difficulty"]

    if taxonomy["content_type"] == "Training":
        return f"""
### Learning Objectives
- Understand {skill} core concepts
- Learn practical workflows
- Handle common issues

### Core Concepts
{skill} is a widely-used platform/technology for real-world applications.

### Hands-on Exercise
- Beginner: Simple exercises to understand basics
- Intermediate: Create projects and mini pipelines
- Advanced: Optimize performance, design scalable solutions

### Common Pitfalls
- Incorrect configurations
- Ignoring best practices

### Self-Check
1. Explain the core idea of {skill}.
2. Apply {skill} to a sample scenario.
"""
    elif taxonomy["content_type"] == "Assessment":
        return f"""
### Assessment

1. What is the main purpose of {skill}?
2. Explain a common use case.

### Scenario
Design a solution using {skill} for a practical problem.

### Evaluation Rubric
- Concept clarity (0–5)
- Design correctness (0–5)
- Scalability thinking (0–5)
"""
    else:
        return f"""
### {skill} Explained

{skill} enables efficient and reliable execution of tasks in practical scenarios.

### Architecture
- Key components
- How they interact
- Example workflows

### Real-World Usage
- Industry applications
- Best practices
"""

# ---------------- RUN PIPELINE ---------------- #
if st.button("▶ Generate using Taxonomy"):

    taxonomy = build_taxonomy(user_query, user_profile)
    prompt = generate_prompt(taxonomy)
    output = mock_llm_response(taxonomy)

    st.divider()

    col1, col2 = st.columns(2)

    # ---------------- TAXONOMY VIEW ---------------- #
    with col1:
        st.subheader("📚 Derived Content Taxonomy")
        st.json(taxonomy)

        st.subheader("🧩 Generated Prompt")
        st.code(prompt, language="text")

    # ---------------- OUTPUT VIEW ---------------- #
    with col2:
        st.subheader("✨ LLM Output (Quality Driven)")
        st.markdown(output)

    st.success(
        "This output quality is driven by taxonomy + prompt structure, "
        "not by a specific LLM model."
    )

# ---------------- FOOTER ---------------- #
st.divider()
st.caption(
    "Demo Purpose: Showcasing how taxonomy-driven prompting improves LLM output quality "
    "independent of the underlying model."
)
