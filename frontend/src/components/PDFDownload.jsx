// PDFDownload.jsx — Button that triggers a PDF download from the backend.
// When clicked, it calls the /api/pdf/{sessionId} endpoint which generates
// and streams the PDF file back to the browser.

import React, { useState } from 'react'

const API_BASE = import.meta.env.VITE_API_URL || ''

export default function PDFDownload({ sessionId, brandName }) {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleDownload = async () => {
    setLoading(true)
    setError('')

    try {
      // Fetch the PDF from the backend
      const response = await fetch(`${API_BASE}/api/pdf/${sessionId}`)

      if (!response.ok) {
        throw new Error(`PDF generation failed: ${response.statusText}`)
      }

      // Convert the response to a blob (binary file data)
      const blob = await response.blob()

      // Create a temporary download link and click it programmatically
      // This is the standard browser technique for triggering file downloads
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `broadlab_${brandName?.replace(/\s+/g, '_').toLowerCase() || 'analysis'}_report.pdf`
      document.body.appendChild(a)
      a.click()

      // Clean up the temporary URL
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)

    } catch (err) {
      setError(err.message || 'Download failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-2">
      <button
        onClick={handleDownload}
        disabled={loading}
        className={`
          flex items-center gap-2.5 px-5 py-2.5 rounded-lg
          text-sm font-semibold transition-all duration-150
          ${loading
            ? 'bg-broadlab-muted text-broadlab-grey cursor-not-allowed'
            : 'bg-broadlab-card border border-broadlab-border text-white hover:border-broadlab-red hover:text-broadlab-red'
          }
        `}
      >
        {loading ? (
          <>
            <div className="w-4 h-4 border-2 border-broadlab-grey border-t-transparent rounded-full animate-spin" />
            Generating PDF...
          </>
        ) : (
          <>
            {/* Download icon */}
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            Download PDF Report
          </>
        )}
      </button>

      {error && (
        <p className="text-broadlab-red text-xs">{error}</p>
      )}
    </div>
  )
}
