# Document Q&A Application

A Streamlit-based application that enables users to interact with multiple documents through a conversational interface.

## Features

- Multiple document upload support (.txt and .pdf formats)
- Efficient document processing with chunking and retrieval mechanisms
- Context-aware responses using advanced language models
- Source attribution for answers
- Persistent chat history
- Interactive chat interface

## Setup and Installation

1. Clone the repository and create a Codespace, or use the provided template
2. Set your OpenAI API key:
   ```bash
   export OPENAI_API_KEY=your_api_key
   ```
3. Run the application:
   ```bash
   streamlit run chat_with_pdf.py
   ```

## Usage

1. Launch the application
2. Upload one or more documents (.txt or .pdf)
3. Enter questions about the documents in the chat interface
4. View responses with source attributions

## Technical Implementation

- Document Processing: Utilizes LangChain's document loaders and text splitters
- Vector Storage: Implements ChromaDB for efficient document retrieval
- Language Model: Integrates with OpenAI's models through the Cornell API endpoint
- Interface: Built with Streamlit for seamless user interaction

## Configuration

The application uses the following default settings:
- Chunk size: 500 characters
- Chunk overlap: 50 characters
- Retrieved context: 5 most relevant chunks
- Temperature: 0.2 for consistent responses

## Development Environment

Built and tested using the provided Cornell Tech Codespace template.
