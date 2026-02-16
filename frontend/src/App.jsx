import { useState } from 'react'
import './App.css'

function App() {
  const [jobDescription, setJobDescription] = useState('')
  const [resume, setResume] = useState('')
  const [template, setTemplate] = useState('')
  const [generatedResume, setGeneratedResume] = useState('')
  const [pdfUrl, setPdfUrl] = useState(null)
  const [pdfError, setPdfError] = useState(null)
  const [pdfZoom, setPdfZoom] = useState(100)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [jobDescriptionFile, setJobDescriptionFile] = useState(null)
  const [resumeFile, setResumeFile] = useState(null)
  const [templateFile, setTemplateFile] = useState(null)

  const handleGenerateResume = async () => {
    if (!jobDescription.trim() || !resume.trim()) {
      setError('Please fill in both job description and resume')
      return
    }

    setLoading(true)
    setError('')
    setGeneratedResume('')
    setPdfUrl(null)
    setPdfError(null)
    setPdfZoom(100)

    try {
      const response = await fetch('/api/generate-resume', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          jobDescription,
          resume,
          template: template || undefined
        })
      })

      const data = await response.json()
      
      if (!response.ok) {
        throw new Error(data.error || 'Failed to generate resume')
      }
      
      setGeneratedResume(data.resume)
      
      // Handle PDF if available
      if (data.pdf) {
        // Convert base64 to blob URL
        const base64toBlob = (base64) => {
          const binaryString = atob(base64)
          const bytes = new Uint8Array(binaryString.length)
          for (let i = 0; i < binaryString.length; i++) {
            bytes[i] = binaryString.charCodeAt(i)
          }
          return new Blob([bytes], { type: 'application/pdf' })
        }
        
        const blob = base64toBlob(data.pdf)
        const url = URL.createObjectURL(blob)
        setPdfUrl(url)
      } else if (data.pdf_error) {
        setPdfError(data.pdf_error)
      }
    } catch (err) {
      console.error('Error generating resume:', err)
      setError(err.message || 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  const handleDownloadResume = () => {
    const element = document.createElement('a')
    const file = new Blob([generatedResume], { type: 'text/plain' })
    element.href = URL.createObjectURL(file)
    element.download = 'optimized_resume.tex'
    document.body.appendChild(element)
    element.click()
    document.body.removeChild(element)
  }

  const handleDownloadPdf = () => {
    if (pdfUrl) {
      const element = document.createElement('a')
      element.href = pdfUrl
      element.download = 'optimized_resume.pdf'
      document.body.appendChild(element)
      element.click()
      document.body.removeChild(element)
    }
  }

  const handleZoomIn = () => {
    setPdfZoom(prev => Math.min(prev + 10, 200))
  }

  const handleZoomOut = () => {
    setPdfZoom(prev => Math.max(prev - 10, 50))
  }

  const handleResetZoom = () => {
    setPdfZoom(100)
  }

  const handleCopyResume = async () => {
    try {
      await navigator.clipboard.writeText(generatedResume)
      // Optional: Show a temporary success message
      const copyBtn = document.querySelector('.copy-btn')
      const originalText = copyBtn.textContent
      copyBtn.textContent = '✓ Copied!'
      setTimeout(() => {
        copyBtn.textContent = originalText
      }, 2000)
    } catch (err) {
      console.error('Failed to copy:', err)
      setError('Failed to copy to clipboard')
    }
  }

  const handleFileSelect = (file, setContent, setFileName) => {
    if (!file) return

    const reader = new FileReader()
    reader.onload = (e) => {
      setContent(e.target.result)
      setFileName(file.name)
    }
    reader.onerror = () => {
      setError('Failed to read file')
    }
    reader.readAsText(file)
  }

  const handleJobDescriptionFileChange = (e) => {
    const file = e.target.files?.[0]
    if (file) {
      handleFileSelect(file, setJobDescription, setJobDescriptionFile)
    }
  }

  const handleResumeFileChange = (e) => {
    const file = e.target.files?.[0]
    if (file) {
      handleFileSelect(file, setResume, setResumeFile)
    }
  }

  const handleTemplateFileChange = (e) => {
    const file = e.target.files?.[0]
    if (file) {
      handleFileSelect(file, setTemplate, setTemplateFile)
    }
  }

  return (
    <div className="app-container">
      <header className="header">
        <h1>📄 Resume Optimizer</h1>
        <p>Tailor your resume to any job description using AI</p>
      </header>

      <div className="content">
        <div className="input-section">
          <div className="form-group">
            <label htmlFor="job">Job Description</label>
            <div className="file-input-wrapper">
              <input
                type="file"
                id="job-file"
                onChange={handleJobDescriptionFileChange}
                accept=".txt,.pdf,.doc,.docx"
                className="file-input"
              />
              <label htmlFor="job-file" className="file-input-label">
                📁 Browse File
              </label>
              {jobDescriptionFile && (
                <span className="file-name">Loaded: {jobDescriptionFile.name}</span>
              )}
            </div>
            <textarea
              id="job"
              placeholder="Paste the job description here or browse for a file..."
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              rows="8"
            />
          </div>

          <div className="form-group">
            <label htmlFor="resume">Your Resume</label>
            <div className="file-input-wrapper">
              <input
                type="file"
                id="resume-file"
                onChange={handleResumeFileChange}
                accept=".txt,.pdf,.doc,.docx"
                className="file-input"
              />
              <label htmlFor="resume-file" className="file-input-label">
                📁 Browse File
              </label>
              {resumeFile && (
                <span className="file-name">Loaded: {resumeFile.name}</span>
              )}
            </div>
            <textarea
              id="resume"
              placeholder="Paste your resume content here or browse for a file..."
              value={resume}
              onChange={(e) => setResume(e.target.value)}
              rows="8"
            />
          </div>

          <div className="form-group">
            <label htmlFor="template">LaTeX Template (Optional)</label>
            <div className="file-input-wrapper">
              <input
                type="file"
                id="template-file"
                onChange={handleTemplateFileChange}
                accept=".txt,.tex"
                className="file-input"
              />
              <label htmlFor="template-file" className="file-input-label">
                📁 Browse Template
              </label>
              {templateFile && (
                <span className="file-name">Loaded: {templateFile.name}</span>
              )}
            </div>
            <textarea
              id="template"
              placeholder="Paste your LaTeX template here or browse for a file (optional)..."
              value={template}
              onChange={(e) => setTemplate(e.target.value)}
              rows="6"
            />
          </div>

          {error && <div className="error-message">{error}</div>}

          <button
            className="generate-btn"
            onClick={handleGenerateResume}
            disabled={loading}
          >
            {loading ? 'Generating...' : 'Generate Optimized Resume'}
          </button>
        </div>

        {generatedResume && (
          <>
            <div className="output-section">
              <div className="output-header">
                <h2>Generated LaTeX Resume</h2>
                <button className="copy-btn" onClick={handleCopyResume}>
                  📋 Copy
                </button>
              </div>
              <div className="resume-output">
                <pre>{generatedResume}</pre>
              </div>
              <button className="download-btn" onClick={handleDownloadResume}>
                ⬇️ Download LaTeX File
              </button>
            </div>

            {pdfUrl && (
              <div className="output-section pdf-section">
                <div className="output-header">
                  <h2>PDF Preview</h2>
                  <div className="pdf-controls">
                    <button className="zoom-btn" onClick={handleZoomOut} title="Zoom Out">
                      🔍−
                    </button>
                    <span className="zoom-level">{pdfZoom}%</span>
                    <button className="zoom-btn" onClick={handleZoomIn} title="Zoom In">
                      🔍+
                    </button>
                    <button className="zoom-btn" onClick={handleResetZoom} title="Reset Zoom">
                      ↺
                    </button>
                    <button className="copy-btn" onClick={handleDownloadPdf}>
                      ⬇️ Download
                    </button>
                  </div>
                </div>
                <div className="pdf-viewer">
                  <div className="pdf-container" style={{ transform: `scale(${pdfZoom / 100})` }}>
                    <iframe 
                      src={pdfUrl} 
                      width="100%" 
                      height="100%"
                      title="Resume Preview"
                    />
                  </div>
                </div>
              </div>
            )}

            {pdfError && (
              <div className="output-section">
                <div className="output-header">
                  <h2>PDF Preview</h2>
                </div>
                <div className="error-message">
                  {pdfError}
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  )
}

export default App
