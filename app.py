import random
import re

from google.cloud import firestore
from google.api_core.exceptions import NotFound
import streamlit as st
from PIL import Image

db = firestore.Client(project="intnow-gcp-practice")

st.set_page_config(
    page_title="GCP(PCA) Exam Dump",
    page_icon="star2",
    layout="wide",
)


def increment_number():
    st.session_state.number += 1


st.title("GCP(PCA) Exam Dump")

with open("exam_dump.txt", encoding="UTF-8") as file:
    txt = file.read()

exercises = []
splited_txt = txt.split("\n________________")

for idx, block in enumerate(splited_txt[1:]):
    splited_block = [i for i in block.split("\n\n\n") if i]
    q = "\n".join(splited_block[:-1]).strip()
    idx_a = re.search("A\. ", q).span()[0]
    if idx == len(splited_txt) - 2:
        exercises.append(
            {
                "Q": q[:idx_a],
                "A": splited_block[-2].split("\n"),
                "C": q[idx_a:].split("\n")[:-1],
            }
        )
        list_footnote = splited_block[-1].split("\n")
        dict_footnote = {}
        for i in list_footnote:
            rs = re.search(r"\[.*\]", i)
            dict_footnote[rs.group()] = i[rs.span()[1] :]
    else:
        exercises.append(
            {
                "Q": q[:idx_a],
                "A": splited_block[-1].split("\n"),
                "C": q[idx_a:].split("\n"),
            }
        )

if not "number" in st.session_state:
    st.session_state["number"] = 0

if not "ids" in st.session_state:
    ids = list(range(len(exercises)))
    random.shuffle(ids)
    st.session_state["ids"] = ids

st.markdown(
    """
<style>
.question {
    font-size:20px;
}
.choice {
    font-size:18px;
}
.answer {
    font-size:18px;
}
</style>
""",
    unsafe_allow_html=True,
)

placeholder = st.empty()

with placeholder.container():
    idx = st.session_state["ids"][st.session_state["number"]]
    st.write(f"{st.session_state['number'] + 1} / {len(exercises)}")

    # 주석 빨간색으로 처리
    fa = re.findall(r"\[[a-z]+\]", exercises[idx]["Q"])
    for i in fa:
        exercises[idx]["Q"] = exercises[idx]["Q"].replace(i, f"<span style='color:red;'>{i}</span>")

    # Question
    st.markdown(
        "<p class='question'>" + exercises[idx]["Q"] + "</p>",
        unsafe_allow_html=True,
    )

    # 문제에 이미지가 포함된 경우
    try:
        q_number = re.search(r"Q\d+", exercises[idx]["Q"]).group()
        image = Image.open(f"gcp/images/{q_number}.png")
        st.image(image, caption=q_number)
    except:
        pass

    # 주석을 빨간색으로 처리하기 위함
    qa = exercises[idx]["Q"]

    # Choices
    count = 0
    for i in exercises[idx]["C"]:
        # 주석을 빨간색으로 처리
        fa = re.findall(r"\[[a-z]+\]", i)
        for j in fa:
            i = i.replace(j, f"<span style='color:red;'>{j}</span>")
        # 선택지마다 맨 앞에 있는 알파벳 대문자를 볼드 처리
        f = re.search(r"[A-Z]\.", i)
        if f:
            i = i.replace(f.group(), f"<b>{f.group()}</b>")
            count += 1
        st.markdown("<p class='choice'>" + i + "</p>", unsafe_allow_html=True)
        qa += i

    alphas = ["A", "B", "C", "D", "E", "F"]
    checks = {i: st.checkbox(i) for i in alphas[:count]}

    # Answer
    if st.button("Answer"):
        group_string = ""
        for i in exercises[idx]["A"]:
            sh = re.search(r"➜ [A-Z].*정답", i)
            if sh:
                group_string += sh.group()
            if i[:5] == "공식 문서":
                sh = re.search(r"http.*\)", i)
                i = f"<a href={sh.group()[:-1]}>공식 문서</a>" + i[sh.span()[1] :]
            elif i[:6] == "공식 블로그":
                sh = re.search(r"http.*\)", i)
                i = f"<a href={sh.group()[:-1]}>공식 블로그</a>" + i[sh.span()[1] :]
            st.markdown("<p class='answer'>" + i + "</p>", unsafe_allow_html=True)

        correct = False
        for i in re.findall(r"[A-Z]", group_string):
            if checks[i] == True:
                correct = True

        data = {
            "total": firestore.Increment(1),
            "last_access": firestore.SERVER_TIMESTAMP,
        }

        if correct:
            st.success("Correct")
            data["correct"] = firestore.Increment(1)
            print(f"Q{idx+1} Correct")
        else:
            st.error("Wrong")
            print(f"Q{idx+1} Wrong")

        try:  # 이전 데이터가 존재하는 경우
            db.collection("questions").document(str(idx+1)).update(data)
        except NotFound:  # 이전 데이터가 존재하지 않는 경우
            data["total"] = 1
            if "correct" in data:
                data["correct"] = 1
            else:
                data["correct"] = 0
            db.collection("questions").document(str(idx+1)).set(data)

    st.button("Next", on_click=increment_number)

    fa = re.findall(r"\[[a-z]+\]", qa)
    for i in fa:  # footnote
        st.markdown(f"<p><span style='color:red;'>{i}</span> {dict_footnote[i]}</p>", unsafe_allow_html=True)
