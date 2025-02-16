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
        return None

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
    Please provide a detailed summary of the key points and main arguments presented in the following document.  Focus on conveying the core message and essential information in a concise manner.

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
                max_output_tokens=1000,  # Increased summary length
                temperature=0.4
            )
        )
        return response.text.strip()
    except Exception as e:
        st.error(f"Error during summarization: {e}")
        return "An error occurred during summarization."

def analyze_document(summary, question=""):
    """Analyzes the document summary using Google's Gemini API and returns the response."""

    if not summary:
        return "No summary to analyze."

    if not question:
        prompt = f"""
        Analyze the following document summary and provide a comprehensive analysis, including:

        1.  **Praise:** 3-4 bullet points highlighting the strengths implied by the summary. Be specific, constructive, and complimentary.
        2.  **Constructive Criticism:** 3-4 bullet points suggesting areas for improvement implied by the summary. Be specific, actionable, and phrased positively.

        Summary:
        {summary}

        ---
        Analysis:
        """
    else:
        prompt = f"""
        Based on the following document summary, answer the user's question. Be concise and helpful.

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
                temperature=0.5
            )
        )
        return response.text.strip()
    except Exception as e:
        st.error(f"Error during analysis: {e}")
        return "An error occurred during analysis."

def main():
    st.title("Interactive Document Analyzer (Gemini 1.5 Flash)")

    # Initialize session state
    if "document_text" not in st.session_state:
        st.session_state.document_text = None
    if "document_summary" not in st.session_state:
        st.session_state.document_summary = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "question_count" not in st.session_state:
        st.session_state.question_count = 0

    uploaded_file = st.file_uploader("Upload a document (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"])

    if uploaded_file is not None:
        text = read_document(uploaded_file)

        if text:
            st.session_state.document_text = text  # Store in session state
            #st.subheader("Document Content:") #Removing this line
            #st.write(text) #Removing this line

            with st.spinner("Summarizing document..."):
                summary = summarize_document(text)
                st.session_state.document_summary = summary

            st.subheader("Document Summary:")
            st.write(st.session_state.document_summary)

            with st.spinner("Performing initial analysis..."):
                initial_analysis = analyze_document(st.session_state.document_summary)
                st.session_state.chat_history.append({"role": "AI", "content": initial_analysis})

            st.subheader("Initial Analysis:")
            st.write(initial_analysis)

            # Display Chat History
            st.subheader("Chat History:")
            for message in st.session_state.chat_history:
                if message["role"] == "User":
                    st.write(f"**You:** {message['content']}")
                else:
                    st.write(f"**AI:** {message['content']}")

            # Chat Interface - Always at the Bottom, New Input After Each Question
            st.subheader("Ask Follow-up Questions:")
            question_key = f"question_input_{st.session_state.question_count}"
            question = st.text_input("Your question:", key=question_key)

            if st.button("Ask"):
                if question:
                    with st.spinner("Generating response..."):
                        response = analyze_document(st.session_state.document_summary, question)
                        st.session_state.chat_history.append({"role": "User", "content": question})
                        st.session_state.chat_history.append({"role": "AI", "content": response})
                        st.session_state.question_count += 1 # Increment the question count

if __name__ == "__main__":
    main()
