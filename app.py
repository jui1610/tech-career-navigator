import streamlit as st
from domain_info import domain_info
from recommendation_engine import calculate_scores, calculate_percentages
from questions import questions
from data.ai_ml import ai_ml
from data.data_science import data_science
from data.software_engineering import software_engineering
from data.cloud_devops import cloud_devops
from data.cybersecurity import cybersecurity

st.set_page_config(
    page_title="Tech Career Navigator",
    page_icon="🚀",
    layout="wide"
)

st.markdown("""
<style>

.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
    padding-left:8rem;
    padding-right:8rem;
}

div.stButton > button{
    width:100%;
    border-radius:10px;
    height:3rem;
    font-size:17px;
    font-weight:600;
}

div.stProgress > div > div > div > div{
    border-radius:10px;
}

h1,h2,h3{
    color:#1F3A5F;
}

</style>
""", unsafe_allow_html=True)

domain_data = {
    "AI": ai_ml,
    "DS": data_science,
    "SE": software_engineering,
    "CLD": cloud_devops,
    "CYB": cybersecurity
}

# Initialize session state

if "show_results" not in st.session_state:
    st.session_state.show_results = False

if "started" not in st.session_state:
    st.session_state.started = False

if "current_question" not in st.session_state:
    st.session_state.current_question = 0

if "answers" not in st.session_state:
    st.session_state.answers = {}


# ---------------- WELCOME PAGE ----------------
if not st.session_state.started:

    st.title("🚀 Tech Career Navigator")

    st.caption("Helping students discover the right technology career path.")

    st.markdown("""
    ### Discover the tech domain that truly matches your interests and strengths.

    Choosing between various tech domains in this fast-paced world can be overwhelming. Tech Career Navigator helps you make an informed decision
    through a personalized assessment designed specifically for students and early-career learners.

    ### What you'll receive:

    ✅ Percentage-based compatibility scores for all domains

    ✅ Curated learning roadmaps tailored to your recommended paths

    ✅ Beginner-friendly courses, tools, programming languages, and project ideas

    ✅ Practical guidance for building your skills, portfolio, and career direction

    ### Domains covered:

    🤖 AI & Machine Learning  
    ☁️ Cloud Computing & DevOps  
    🔐 Cybersecurity  
    📊 Data Science & Big Data  
    💻 Software Engineering & Architecture
    """)

    st.success(
    "Complete a short 10-question assessment to receive personalized career recommendations."
    )

    if st.button("Start Quiz 🚀"):
        st.session_state.started = True
        st.rerun()


# ---------------- QUIZ PAGE ----------------
elif not st.session_state.show_results:

    q_index = st.session_state.current_question
    q = questions[q_index]

    st.progress((q_index + 1) / len(questions))

    st.markdown(f"## Question {q_index + 1} / {len(questions)}")
    st.write(q["question"])

    radio_key = f"question_{q_index}"

    # Initialize the value only once
    if radio_key not in st.session_state:
      if q_index in st.session_state.answers:
        st.session_state[radio_key] = st.session_state.answers[q_index]
      else:
        st.session_state[radio_key] = q["options"][0]


    selected_option = st.radio(
    "Choose one option:",
    q["options"],
    format_func=lambda option: option["text"],
    key=radio_key
    )

    # Save the selected answer
    st.session_state.answers[q_index] = selected_option

    col1, col2 = st.columns(2)

    with col1:
      if q_index > 0:
        if st.button("⬅ Previous"):
            st.session_state.current_question -= 1
            st.rerun()

    with col2:

      if q_index < len(questions) - 1:

        if st.button("Next ➡"):

            st.session_state.current_question += 1
            st.rerun()

      else:

        if st.button("Finish Quiz 🎉"):

          scores = calculate_scores(st.session_state.answers)
          percentages = calculate_percentages(scores)

          st.session_state.results = percentages
          st.session_state.show_results = True

          st.rerun()

# ---------------- RESULTS PAGE ----------------
else:

    percentages = st.session_state.results

    sorted_domains = sorted(
        percentages.items(),
        key=lambda x: x[1],
        reverse=True
    )

    st.balloons()

    top_domain = sorted_domains[0][0]
    selected_domain = domain_data[top_domain]
    top_percentage = sorted_domains[0][1]

    st.title("🎯 Your Results")

    st.success(
        f"🏆 Your Best Match: "
        f"{domain_info[top_domain]['emoji']} "
        f"{domain_info[top_domain]['name']} "
        f"({top_percentage}%)"
    )

    st.markdown("---")
    st.subheader("📊 Your Domain Compatibility")

    for domain, percentage in sorted_domains:

        info = domain_info[domain]

        st.write(
            f"{info['emoji']} **{info['name']}** — {percentage}%"
        )

        st.progress(percentage / 100)

        st.caption(info["description"])

        st.markdown("<br>", unsafe_allow_html=True) 

    st.markdown("---")
    st.header(
    f"{domain_info[top_domain]['emoji']} Complete Roadmap for {domain_info[top_domain]['name']}"
    )

    st.write(selected_domain["overview"])

    st.subheader("🗺️ Learning Roadmap")
    for i, step in enumerate(selected_domain["roadmap"], start=1):
      st.write(f"**Step {i}:** {step}")

    st.subheader("💻 Programming Languages")
    for language in selected_domain["languages"]:
      st.markdown(f"### {language['name']}")
      st.caption(language["purpose"])

    st.subheader("🛠️ Essential Tools")
    for tool in selected_domain["tools"]:
      st.markdown(f"### {tool['name']}")
      st.caption(tool["purpose"])

    st.subheader("🎓 Recommended Free Courses")
    for course in selected_domain["courses"]:
      st.markdown(f"### {course['title']}")
      st.caption(course["purpose"])

    st.subheader("🚀 Recommended Projects")
    for project in selected_domain["projects"]:
      st.markdown(f"### {project['title']}")
      st.caption(project["level"])

    st.markdown("---")

    st.info(
    """
    ### 🎉 Your roadmap is just the beginning.

    Remember, no assessment can perfectly define your career.

    Use these recommendations as a starting point, stay curious, build projects, and keep exploring.

    The best tech career is the one you genuinely enjoy learning.
    """
    )

    st.markdown("---")

    if st.button("🔄 Retake Quiz"):
      st.session_state.started = True
      st.session_state.show_results = False
      st.session_state.current_question = 0
      st.session_state.answers = {}
      st.session_state.results = {}
      st.rerun()              