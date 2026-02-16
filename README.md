# KaamChalau - AI Resume Optimizer

An AI-powered resume optimization tool that tailors your resume for specific job descriptions using multiple AI models.

## Features

- 🤖 **Multiple AI Models**: Choose between Groq (Llama 3.3 70B) or Claude (Anthropic)
- 📄 **PDF Preview**: Real-time PDF preview with zoom controls
- 📝 **LaTeX Output**: Professional LaTeX resume generation
- 🎯 **Job-Specific Optimization**: Keyword matching and tailoring
- 📋 **Custom Templates**: Upload your own LaTeX templates
- 🚀 **Modern UI**: React frontend with responsive design
- ⚡ **Fast Inference**: Quick resume generation

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 18+** - [Download Node.js](https://nodejs.org/)
- **pip** - Python package manager (comes with Python)
- **npm** - Node package manager (comes with Node.js)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd kaamchalau
```

### 2. Set Up Python Backend

Install Python dependencies:

```bash
pip install -r requirements.txt
```

### 3. Set Up Frontend

Navigate to the frontend directory and install dependencies:

```bash
cd frontend
npm install
cd ..
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```bash
# Copy the example file
cp .env.example .env
```

Edit `.env` and add your API keys:

```
# Required for Groq (Llama models)
GROQ_API_KEY=your_groq_api_key_here

# Optional - Required only if using Claude
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

**Get API Keys:**
- **Groq (Free):** [https://console.groq.com/](https://console.groq.com/)
- **Claude (Paid):** [https://console.anthropic.com/](https://console.anthropic.com/)

## Running the Application

You need to run both the backend and frontend servers simultaneously.

### Terminal 1: Start the Backend (Flask)

```bash
python app.py
```

The backend server will start on `http://localhost:5000`

You should see:
```
Starting Flask server...
GROQ_API_KEY configured: True
 * Running on http://127.0.0.1:5000
```

### Terminal 2: Start the Frontend (Vite + React)

```bash
cd frontend
npm run dev
```

The frontend will start on `http://localhost:5173`

Open your browser and navigate to `http://localhost:5173`

## Project Structure

```
kaamchalau/
├── app.py                  # Flask backend server
├── main.py                 # CLI script for direct API calls
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
├── .env.example           # Environment variables template
├── txt_files/
│   ├── template.txt       # LaTeX resume template
│   ├── master.txt         # Your master resume
│   └── job.txt            # Job description
└── frontend/
    ├── package.json       # Node.js dependencies
    ├── vite.config.js     # Vite configuration
    ├── index.html
    └── src/
        ├── App.jsx        # Main React component
        ├── App.css
        └── main.jsx
```

## Usage

### Web Interface

1. Start both backend and frontend servers (see above)
2. Open `http://localhost:5173` in your browser
3. Enter your job description
4. Enter your resume content
5. (Optional) Upload a custom LaTeX template
6. **Select AI Model**: Choose between Groq or Claude from the dropdown
7. Click "Generate Optimized Resume"
8. View the generated LaTeX code and PDF preview
9. Use zoom controls (+/-) to adjust PDF view
10. Download LaTeX file or PDF

### CLI (Alternative)

You can also use the command-line interface:

```bash
python main.py -r txt_files/master.txt -j txt_files/job.txt
```

This will output the LaTeX resume to `resume.tex`

## Dependencies

### Python (Backend)

- `flask` - Web framework
- `flask-cors` - CORS support
- `groq` - Groq API client (for Llama models)
- `anthropic` - Anthropic API client (for Claude models)
- `python-dotenv` - Environment variable management

### Node.js (Frontend)

- `react` - UI framework
- `vite` - Build tool and dev server

## Configuration

### Selecting AI Model

You can choose between two AI providers directly from the web interface:

1. **Groq (Llama 3.3 70B)** - Fast, free tier available
   - Model: `llama-3.3-70b-versatile`
   - 8K context window
   - Requires: `GROQ_API_KEY`

2. **Claude (Anthropic)** - High quality, paid
   - Model: `claude-3-5-sonnet-20241022`
   - 200K context window
   - Requires: `ANTHROPIC_API_KEY`

Simply select your preferred model from the dropdown in the web interface before generating.

### Customizing the Resume Template

Edit `txt_files/template.txt` to modify the LaTeX resume structure.

## Troubleshooting

### "Failed to generate resume" Error

1. **Check if backend is running:** Make sure `python app.py` is running in a separate terminal
2. **Check API key:** Ensure the appropriate API key is set in your `.env` file
   - For Groq: `GROQ_API_KEY`
   - For Claude: `ANTHROPIC_API_KEY`
3. **Check console:** Open browser DevTools (F12) to see detailed error messages
4. **Check backend logs:** Look at the terminal running `app.py` for error messages

### "PDF compilation failed" Error

Make sure you have LaTeX installed:

```bash
# Ubuntu/Debian
sudo apt-get install texlive-latex-base texlive-latex-extra

# macOS
brew install mactex-no-gui
```

### Import Errors

If you see import errors, reinstall dependencies:

```bash
pip install -r requirements.txt --force-reinstall
```

### Port Already in Use

If port 5000 or 5173 is already in use:

- **Backend:** Change the port in `app.py`: `app.run(debug=True, port=5001)`
- **Frontend:** Change the port in `vite.config.js` or use: `npm run dev -- --port 5174`

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## Security Note

⚠️ **Never commit your `.env` file to version control!**

The `.env` file contains your API key and should be kept private. It's already in `.gitignore`.

## License

See [LICENSE](LICENSE) file for details.

## Support

For issues and questions, please open an issue on GitHub.
