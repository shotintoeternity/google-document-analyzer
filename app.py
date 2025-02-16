import streamlit as st
import pdfminer.high_level
import docx
import os
import google.generativeai as genai

# Securely load Gemini API Key (replace with your chosen method)
genai.configure(api_key=st.secrets.get("GOOGLE_API_KEY"))  # Streamlit Secrets

if not st.secrets.get("GOOGLE_API_KEY"):
    st.error("Google Gemini API key not found. Please configure it.")
    st.stop()

model = genai.GenerativeModel('gemini-1.5-flash')  # Specify the model

def extract_text_from_pdf(pdf_file):
    """Extracts text from a PDF file."""
    try:
        text = pdfminer.high_level.extract_text(pdf_file)
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
        return ""

def extract_text_from_docx(docx_file):
    """Extracts text from a DOCX file."""
    try:
        doc = docx.Document(docx_file)
        full_text = []
        for paragraph in doc.paragraphs:
            full_text.append(paragraph.text)
        return '\n'.join(full_text)
    except Exception as e:
        st.error(f"Error extracting text from DOCX: {e}")
        return None

def extract_text_from_txt(txt_file):
    """Extracts text from a TXT file."""
    try:
        return txt_file.read() # Directly read the file content
    except Exception as e:
        st.error(f"Error extracting text from TXT: {e}")
        return None

def read_document(file):
    """Reads a document and extracts its text content."""
    file_extension = os.path.splitext(file.name)[1].lower()

    if file_extension == ".pdf":
        return extract_text_from_pdf(file)
    elif file_extension == ".docx":
        return extract_text_from_docx(file)
    elif file_extension == ".txt":
        return txt_file.read()
    elif file_extension == ".doc":
        st.warning("DOC files are not directly supported.  Consider converting to DOCX or PDF.")
        return None
    else:
        st.error("Unsupported file format. Please upload a PDF, DOCX, or TXT file.")
        return None

def summarize_document(text):
    """Summarizes the document text using Google's Gemini API."""
    prompt = f"""
    You are an expert summarizer. Provide a detailed summary of the key points and main arguments presented in the following document. Focus on conveying the core message and essential information in a concise manner.

    Document:
    {text}

    ---
    Summary:
    """
    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                candidate_count=1,
                max_output_tokens=750,  # Reduced for testing, adjust as needed
                temperature=0.3  # Reduced for consistency, adjust as needed
            )
        )
        return response.text.strip()
    except Exception as e:
        st.error(f"Error during summarization: {e}")
        return "An error occurred during summarization."

def analyze_document(summary):
    """Analyzes the document summary and provides an initial analysis."""
    prompt = f"""
        You are a document analysis expert. Analyze the following document summary. Provide:

        1. **Praise:** 2-3 specific bullet points highlighting strengths implied by the summary. Be constructive and complimentary.
        2. **Constructive Criticism:** 2-3 bullet points suggesting areas for improvement implied by the summary. Be specific, actionable, and positive.
        3. **Actionable next steps**: What should the person do to improve the document?

        Summary:
        {summary}

        ---
        Analysis:
        """

    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                candidate_count=1,
                max_output_tokens=750,
                temperature=0.3
            )
        )
        return response.text.strip()
    except Exception as e:
        st.error(f"Error during analysis: {e}")
        return "An error occurred during analysis."

def ask_followup(summary, question):
    """Answers follow-up questions based on the document summary."""
    prompt = f"""
        You are a helpful document analysis expert. Use the following document summary to answer the user's question. Be concise, specific, and helpful.

        Summary:
        {summary}

        Question: {question}

        ---
        Answer:
        """
    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                candidate_count=1,
                max_output_tokens=750,
                temperature=0.3
            )
        )
        return response.text.strip()
    except Exception as e:
        st.error(f"Error during analysis or question answering: {e}")
        return "An error occurred during analysis."

def submit_followup():
    """Handles the submission of follow-up questions."""
    question = st.session_state.followup_input.strip()
    if question != "":
        with st.spinner("Processing your follow-up question..."):
            answer = ask_followup(st.session_state.document_summary, question)

        #Store the new conversation:
        if "followups" not in st.session_state: #create the followups var
            st.session_state.followups = []

        st.session_state.followups.append({"question": question, "answer": answer}) #Add questions and answers into the object

        st.session_state.followup_input = ""  # Clear the input box
        if hasattr(st, "experimental_rerun"):
            st.experimental_rerun()

def main():
    st.title("Interactive Document Analyzer (Gemini 1.5 Flash)")

    # Initialize session state
    if "document_text" not in st.session_state:
        st.session_state.document_text = None
    if "document_summary" not in st.session_state:
        st.session_state.document_summary = None
    if "followup_input" not in st.session_state:
        st.session_state.followup_input = ""
    #Add followups variable
    if "followups" not in st.session_state:
        st.session_state.followups = []

    uploaded_file = st.file_uploader("Upload a document (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"])

    if uploaded_file is not None:
        text = read_document(uploaded_file)

        if text:
            st.session_state.document_text = text  # Store in session state

            with st.spinner("Summarizing document..."):
                summary = summarize_document(text)
                st.session_state.document_summary = summary

            st.subheader("Document Summary:")
            st.write(st.session_state.document_summary)

            with st.spinner("Performing initial analysis..."):
                initial_analysis = analyze_document(st.session_state.document_summary)
                st.subheader("Initial Analysis:")
                st.write(initial_analysis)

    #Only display this after the document has been submitted
    if st.session_state.document_summary: #Check if the summary exists

        #Display previous follow-up interactions.
        if st.session_state.followups:
            st.markdown("### Previous Follow-Up Interactions")
            for idx, qa in enumerate(st.session_state.followups, 1):
                st.markdown(f"**Follow-Up #{idx}:**")
                st.markdown(f"**Question:** {qa['question']}")
                st.markdown(f"**Answer:** {qa['answer']}")
                st.markdown("---")

        # Render the Follow-Up Questions section at the bottom.
        st.subheader("Follow-Up Questions")
        st.write("Do you have any other questions? Is there anything else I can help you with?")
        st.text_input(
            "Enter your follow-up question here:",
            key="followup_input",
            on_change=submit_followup,
            value=""
        )


if __name__ == "__main__":
    main()
