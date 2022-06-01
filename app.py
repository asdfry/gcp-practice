import random
import re

import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="GCP(PCA) Exam Dump",
    page_icon="star2",
    layout="wide",
)

placeholder = st.empty()
if not "nickname" in st.session_state:
    with placeholder:
        nickname = st.text_input("Please enter your nickname")
    if nickname:
        st.session_state["nickname"] = nickname
        placeholder.empty()


def increment_number():
    st.session_state.number += 1


if "nickname" in st.session_state:
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
        for i in exercises[idx]["C"]:
            # 주석을 빨간색으로 처리
            fa = re.findall(r"\[[a-z]+\]", i)
            for j in fa:
                i = i.replace(j, f"<span style='color:red;'>{j}</span>")
            # 선택지마다 맨 앞에 있는 알파벳 대문자를 볼드 처리
            f = re.search(r"[A-Z]\.", i)
            if f:
                i = i.replace(f.group(), f"<b>{f.group()}</b>")
            st.markdown("<p class='choice'>" + i + "</p>", unsafe_allow_html=True)
            qa += i

        # Answer
        if st.button("Answer"):
            for i in exercises[idx]["A"]:
                if i[:5] == "공식 문서":
                    f = re.search(r"http.*\)", i)
                    i = f"<a href={f.group()[:-1]}>공식 문서</a>" + i[f.span()[1]:]
                elif i[:6] == "공식 블로그":
                    f = re.search(r"http.*\)", i)
                    i = f"<a href={f.group()[:-1]}>공식 블로그</a>" + i[f.span()[1]:]
                st.markdown("<p class='answer'>" + i + "</p>", unsafe_allow_html=True)

        st.button("Next", on_click=increment_number)

        fa = re.findall(r"\[[a-z]+\]", qa)
        for i in fa:  # footnote
            st.markdown(f"<p><span style='color:red;'>{i}</span> {dict_footnote[i]}</p>", unsafe_allow_html=True)
