import streamlit as st

st.balloons()
st.title("🎉 Final Page: Project Wrap-up")

st.markdown("""
### 🏫 Zewail City of Science and Technology  
**University of Science and Technology**  
**Computational Sciences and Artificial Intelligence (CSAI) Program**  
**Course:** DSAI 103 – *Data Acquisition in Data Science*  
**Instructor:** Dr. Mohamed Maher Ata  
**Teaching Assistants:**  
- Rasha Mostafa  
- Bassem Adel Naguib  
""")

st.markdown("""
## 🙏 Special Thanks
A heartfelt thank you to our doctor and TAs for teaching us this course and guiding us through this project.  
We truly learned a lot and had fun doing it! 😊
""")

st.markdown("## 👥 Team Members & LinkedIn Profiles")

team = {
    "Zeyad Mohamed Fathy": "https://www.linkedin.com/in/zeyad-nafea-314354357/",
    "Radwa Abd El Sadek Salah": "https://www.linkedin.com/in/radwa-salah-84b752357?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app"
}

for name, link in team.items():
    st.markdown(f"- [{name}]({link})")

st.markdown("""
## 🙂 Feedback

- Loved working as a team 🤝  
- Learned a lot about web scraping, visualization, and Streamlit 📊  
- Excited to keep learning more! 🚀
""")

sentiment_mapping = ["one", "two", "three", "four", "five"]
selected = st.feedback("faces")
if selected is not None:
    st.markdown(f"You selected {sentiment_mapping[selected]} star(s).")

st.success("Thanks again for exploring our project and hope you liked it! 😄")