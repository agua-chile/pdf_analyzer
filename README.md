# PDF Q&A Bot

A Python application that uses IBM Watsonx AI to analyze PDF documents and answer questions about their content using natural language processing and vector embeddings.

## Author

**Agua Chile**
- GitHub: [@aguachile](https://github.com/aguachile)
- Project: pdf_analyzer

## Acknowledgements

This project is based on the IBM Coursera course:
**[Project: Generative AI Applications with RAG and LangChain](https://www.coursera.org/learn/project-generative-ai-applications-with-rag-and-langchain/)**

Special thanks to IBM for providing comprehensive learning materials on Retrieval-Augmented Generation (RAG) and LangChain implementation with Watsonx AI.

## Features

- 📄 **PDF Document Processing**: Upload and process PDF files
- 🤖 **AI-Powered Q&A**: Ask questions about your PDF content in natural language
- 🔍 **Semantic Search**: Uses vector embeddings to find relevant document sections
- 🎯 **Context-Aware Responses**: Provides accurate answers based on document content
- 🌐 **Web Interface**: Easy-to-use Gradio interface
- 🔒 **Secure**: Environment variables for API credentials

## Technology Stack

- **AI Models**: IBM Watsonx AI (Granite 3 8B, Slate 125M)
- **Framework**: LangChain
- **Vector Database**: ChromaDB
- **Document Processing**: PyPDF
- **UI**: Gradio
- **Environment**: Python 3.12

## Setup

### Prerequisites

- Python 3.12
- IBM Watsonx AI account with API credentials

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/agua-chile/pdf_analyzer
   cd pdf_analyzer
   ```

2. **Create and activate virtual environment and install dependencies**
   ```bash
   chmod +x setup.sh && ./setup.sh
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the `env/` directory:
   ```
   APIKEY=your_ibm_watsonx_api_key
   PROJECT_ID=your_ibm_watsonx_project_id
   ```

### Getting IBM Watsonx Credentials

1. Sign up for [IBM Cloud](https://cloud.ibm.com/)
2. Create a Watsonx AI service instance
3. Get your API key from IBM Cloud IAM
4. Create a project in Watsonx and note the Project ID

## Usage

1. **Start the application**
   ```bash
   python qabot.py
   ```

2. **Upload a PDF**
   - Open the Gradio interface in your browser
   - Upload a PDF document using the file uploader

3. **Ask questions**
   - Type your question about the PDF content
   - Get AI-powered answers based on the document

## Project Structure

```
pdf_analyzer/
├── qabot.py              # Main application file
├── error_handling.py     # Error handling utilities
├── env/
│   ├── .env             # Environment variables (not tracked)
│   ├── .venv/           # Virtual environment (not tracked)
│   └── requirements.txt # Python dependencies
│   └── setup.sh         # Setup environment script
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## Configuration

### AI Models

- **Generation Model**: `ibm/granite-3-8b-instruct`
- **Embedding Model**: `ibm/slate-125m-english-rtrvr`

## Features in Detail

### Document Processing
- Loads PDF files using PyPDFLoader
- Splits documents into manageable chunks
- Creates vector embeddings for semantic search

### Q&A System
- Uses retrieval-augmented generation (RAG)
- Finds relevant document sections for each question
- Generates contextual answers using IBM Granite model

### Vector Database
- ChromaDB for storing document embeddings
- Efficient similarity search for relevant content
- Persistent storage for processed documents

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions or issues:
- Check the error logs for debugging information
- Ensure your IBM Watsonx credentials are correctly configured
- Verify that all dependencies are properly installed

## Troubleshooting

### Common Issues

1. **API Key Errors**
   - Verify your `.env` file contains valid credentials
   - Check that the API key has proper permissions

2. **PDF Loading Issues**
   - Ensure PDF files are not password-protected
   - Verify PDF files are not corrupted

3. **Memory Issues**
   - Reduce chunk size for large documents
   - Consider processing smaller documents first

---

*Built using IBM Watsonx AI and LangChain*
