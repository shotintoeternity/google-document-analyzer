# Interactive Document Analyzer (Gemini 1.5 Flash)

This Streamlit application provides an interactive document analysis experience using Google's Gemini 1.5 Flash model. Users can upload documents (PDF, DOCX, TXT) and receive a summarized analysis, including praise and constructive criticism. The application also allows for follow-up questions to further explore the document's content.

## Features

*   **Document Upload:** Supports uploading PDF, DOCX, and TXT files.
*   **Automatic Summarization:** Uses Gemini 1.5 Flash to generate a concise summary of the uploaded document.
*   **Initial Analysis:** Provides an initial analysis of the document summary, including praise and constructive criticism.
*   **Interactive Follow-Up Questions:** Allows users to ask follow-up questions about the document's content and receive answers based on the summary.
*   **Chat History Display:** Displays a history of the conversation, showing the user's questions and the AI's responses.

## Technologies Used

*   **Streamlit:** For building the interactive web application.
*   **Google Gemini API (via `google-generativeai`):** For document summarization and analysis.
*   **`pdfminer.six`:** For extracting text from PDF files.
*   **`python-docx`:** For extracting text from DOCX files.

## Prerequisites

Before running the application, you'll need the following:

*   **Python 3.7 or higher:**  Ensure you have a compatible Python version installed.
*   **Google Cloud Project and API Key:** You'll need a Google Cloud project and API key to access the Gemini API. Get an API key from the Google AI Studio: [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
*   **Streamlit Account (Optional):** For deploying the application to Streamlit Cloud.

## Setup

1.  **Clone the Repository:**

    ```bash
    git clone https://www.github.com/shotintoeternity/google-document-analyzer.git
    cd google-document-analyzer
    ```

2.  **Create a Virtual Environment (Recommended):**

    ```bash
    python3 -m venv venv  # Create a virtual environment (Python 3.3+)
    # virtualenv venv       # If you have virtualenv installed
    ```

3.  **Activate the Virtual Environment:**

    ```bash
    source venv/bin/activate  # Linux/macOS
    # venv\Scripts\activate   # Windows
    ```

4.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    The `requirements.txt` file contains the list of required Python packages.

5.  **Configure API Key:**

    Store your Google Gemini API key securely using one of the following methods:

    *   **Streamlit Secrets Management (Recommended for Streamlit Cloud):**
        *   Go to your Streamlit Cloud app's settings.
        *   Add a new secret named `GOOGLE_API_KEY` and set its value to your API key.
    *   **Environment Variables:**
        *   Set an environment variable named `GOOGLE_API_KEY` on your system:

            ```bash
            export GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"  # Linux/macOS
            # set GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"   # Windows
            ```

    *   **`secrets.toml` file (for local development):**
        * Create a file named `.streamlit/secrets.toml` in your project directory. Note that the file path is important.
        * Add the following line to the file, replacing `YOUR_GOOGLE_API_KEY` with your actual API key:

            ```toml
            GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY"
            ```

        *   **Important:** Add `.streamlit/secrets.toml` to your `.gitignore` file to prevent committing your API key to version control.

## Running the Application

1.  **Start the Streamlit App:**

    ```bash
    streamlit run app.py
    ```

    Replace `app.py` with the name of your main Streamlit script.

2.  **Access the App:**

    Streamlit will automatically open the app in your web browser. If it doesn't, you can access it by navigating to the URL displayed in the terminal (usually `http://localhost:8501`).

## Usage

1.  **Upload a Document:**  Use the file uploader to select a PDF, DOCX, or TXT file.
2.  **View the Summary:** The application will generate a summary of the document using Gemini 1.5 Flash and display it.
3.  **Review the Initial Analysis:**  The application will provide an initial analysis of the document summary, including praise and constructive criticism.
4.  **Ask Follow-Up Questions:**  Enter your questions in the text input field at the bottom and press Enter to submit them. The AI's response will be displayed below the input field.
5.  **View Conversation History:** All interactions will be shown in the chat history.

## Deployment (Streamlit Cloud)

1.  **Create a GitHub Repository:**  Upload your code (including `requirements.txt`, `.streamlit/secrets.toml` (make sure this is NOT tracked in Git), and `app.py`) to a new GitHub repository.
2.  **Create a Streamlit Cloud Account:**  Go to [https://streamlit.io/cloud](https://streamlit.io/cloud) and sign up for a free account.
3.  **Connect to GitHub:**  In the Streamlit Cloud dashboard, click "New app" and connect to your GitHub repository.
4.  **Configure Secrets:** Add your `GOOGLE_API_KEY` as a secret in the Streamlit Cloud app settings.
5.  **Deploy:**  Click "Deploy!" and Streamlit Cloud will automatically build and deploy your application.

## Contributing

Contributions are welcome! If you find a bug, have a suggestion, or want to contribute code, please open an issue or submit a pull request.

---

**Disclaimer:** This application uses AI to analyze documents. The accuracy and completeness of the analysis may vary. Use this tool as a starting point for your own research and analysis, and always consult with relevant experts for critical decisions.
