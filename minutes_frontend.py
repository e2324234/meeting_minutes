import streamlit as st
import modal
from docx import Document

def main():
    st.title("Meeting Minutes Generator")

    # Upload the .vtt, .txt, or .docx file for the transcript
    uploaded_file = st.file_uploader("Choose a .vtt, .txt, or .docx file for the transcript", type=["vtt", "txt", "docx"])
    if uploaded_file:
        if uploaded_file.type in ["text/vtt", "text/plain"]:
            transcript = uploaded_file.read().decode()
        else:
            doc = Document(uploaded_file)
            transcript = "\n".join([p.text for p in doc.paragraphs if p.text.strip() != ""])
    else:
        transcript = ""

    # Optional field for the meeting agenda
    meeting_agenda = st.text_area("Meeting Agenda (optional): Enter each agenda item on a new line.")


    if st.button("Generate Meeting Minutes"):
        if not transcript:
            st.error("Please upload a .vtt, .txt, or .docx file for the transcript before generating the minutes.")
            return

        # Base prompt structure
        basePrompt = """
        Given the provided meeting transcript, generate meeting minutes that are informative, capturing essential details, key points, decisions, and action items. Ensure the minutes:

        - Exclude attendees' names.
        - Do not have a separate section for Action Items.
        - Consider any schedule or time associated with each action item or decision.
        - Assign the person or company responsible for each action or decision, if mentioned in the transcript.
        - Exclude the date and time mentioned at the beginning of the transcript.

        ---

        Note: The minutes should be clear, and organized.
        """

        # If there's an agenda, prepend the specific instructions related to the agenda
        if meeting_agenda:
            agendaPrompt = f"""
        Given the provided meeting agenda and transcript, ensure the minutes:

        - Are structured based on the meeting agenda.
        - Integrate highlights, decisions, or action items directly under the relevant agenda points.

        Agenda:
        {meeting_agenda}

        ---

        """
            instructPrompt = agendaPrompt + basePrompt
        else:
            instructPrompt = basePrompt

        request = instructPrompt + "\n\nTranscript:\n" + transcript

        # Call the Modal function to generate the minutes
        f = modal.Function.lookup("minutes-project", "generate_minutes")
        minutes = f.call(request)
        st.subheader("Generated Meeting Minutes:")
        st.write(minutes)

if __name__ == '__main__':
    main()
