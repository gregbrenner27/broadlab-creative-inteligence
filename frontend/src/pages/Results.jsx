// Results.jsx — Screen 2: shows the progress indicator while the pipeline runs,
// then displays the completed analysis results.
//
// Uses Server-Sent Events (SSE) — the browser maintains an open connection to
// the backend which pushes updates as each pipeline step finishes. When all
// steps complete, the results are displayed immediately without a page reload.

import React, { useState, useEffect, useRef } from 'react'
import { useParams, useNavigate, useLocation } from 'react-router-dom'
import logo from '../assets/broadlab-logo.png'
import AnalysisProgress from '../components/AnalysisProgress'
import QuickSummary from '../components/QuickSummary'
import FullAnalysis from '../components/FullAnalysis'
import PDFDownload from '../components/PDFDownload'

const API_BASE = import.meta.env.VITE_API_URL || ''

export default function Results() {
  const { sessionId } = useParams()    // the session ID from the URL
  const navigate = useNavigate()
  const location = useLocation()

  // Pull the brand name and output mode that were passed from the Dashboard
  const brandName = location.state?.brandName || 'Analysis'
  const outputMode = location.state?.outputMode || 'both'

  // State
  const [progressEvents, setProgressEvents] = useState([])
  const [isComplete, setIsComplete] = useState(false)
  const [hasError, setHasError] = useState(false)
  const [result, setResult] = useState(null)
  const [activeResultTab, setActiveResultTab] = useState('quick')

  // Keep a ref to the EventSource so we can close it on cleanup
  const eventSourceRef = useRef(null)

  useEffect(() => {
    if (!sessionId) return

    // Open an SSE connection to the backend progress endpoint
    const eventSource = new EventSource(`${API_BASE}/api/progress/${sessionId}`)
    eventSourceRef.current = eventSource

    // Called each time the backend sends a progress event
    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)

        if (data.type === 'complete') {
          // Pipeline finished successfully
          setIsComplete(true)
          setResult(data.result)
          eventSource.close()

          // Set the default tab based on what output mode was requested
          if (outputMode === 'quick') setActiveResultTab('quick')
          else if (outputMode === 'full') setActiveResultTab('full')
          else setActiveResultTab('quick')

        } else if (data.type === 'error') {
          // Pipeline failed
          setHasError(true)
          setProgressEvents(prev => [...prev, { step: 'error', status: 'error', message: data.error }])
          eventSource.close()

        } else {
          // Regular step progress event — add to the list
          setProgressEvents(prev => [...prev, data])
        }
      } catch (e) {
        console.error('Failed to parse SSE event:', e)
      }
    }

    // Called if the SSE connection itself errors out
    eventSource.onerror = (err) => {
      console.error('SSE connection error:', err)
      // Only mark as error if we didn't already complete successfully
      if (!isComplete) {
        setHasError(true)
        setProgressEvents(prev => [...prev, {
          step: 'error', status: 'error',
          message: 'Lost connection to server. Check that the backend is still running.'
        }])
      }
      eventSource.close()
    }

    // Cleanup: close the connection when this component unmounts
    return () => {
      eventSource.close()
    }
  }, [sessionId])

  // Extract the report data from the result
  const reportData = result?.report?.report || result?.report || {}
  const quickSummary = reportData.quick_summary
  const fullAnalysis = reportData.full_analysis

  return (
    <div className="min-h-screen bg-broadlab-dark">
      {/* ---- TOP NAV BAR ---- */}
      <header className="border-b border-broadlab-border px-8 py-4 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <img src={logo} alt="Broadlab" className="h-8 w-auto" />
          <span className="text-white font-bold text-lg tracking-widest">BROADLAB</span>
        </div>
        {isComplete && (
          <button
            onClick={() => navigate('/')}
            className="flex items-center gap-2 text-broadlab-grey text-sm hover:text-white transition-colors"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            New Analysis
          </button>
        )}
      </header>

      <main className="max-w-5xl mx-auto px-6 py-10">

        {/* ---- PAGE HEADER ---- */}
        <div className="mb-8 flex items-start justify-between">
          <div>
            <p className="text-broadlab-grey text-xs font-semibold tracking-widest uppercase mb-1">
              {isComplete ? 'Analysis Complete' : 'Running Analysis'}
            </p>
            <h1 className="text-3xl font-bold text-white tracking-tight">{brandName}</h1>
          </div>

          {/* PDF download button — only shown when complete and mode includes PDF */}
          {isComplete && !hasError && outputMode !== 'quick' && (
            <PDFDownload sessionId={sessionId} brandName={brandName} />
          )}
        </div>

        {/* ---- TWO COLUMN LAYOUT: Progress + Results ---- */}
        <div className="grid grid-cols-3 gap-6">

          {/* LEFT COLUMN: Progress indicator (always visible) */}
          <div className="col-span-1">
            <div className="bg-broadlab-card border border-broadlab-border rounded-xl p-4 sticky top-6">
              <p className="text-xs font-semibold tracking-widest text-broadlab-grey uppercase mb-4">
                Pipeline Status
              </p>
              <AnalysisProgress
                progressEvents={progressEvents}
                isComplete={isComplete}
                hasError={hasError}
              />
            </div>
          </div>

          {/* RIGHT COLUMN: Results (shown after completion) */}
          <div className="col-span-2">
            {!isComplete && !hasError && (
              /* Loading state — shown while pipeline runs */
              <div className="bg-broadlab-card border border-broadlab-border rounded-xl p-8 flex flex-col items-center justify-center text-center min-h-64">
                <div className="w-10 h-10 border-2 border-broadlab-red border-t-transparent rounded-full animate-spin mb-4" />
                <p className="text-white font-medium">Analysing creative...</p>
                <p className="text-broadlab-grey text-sm mt-1.5">
                  This typically takes 3–5 minutes.
                </p>
                <p className="text-broadlab-grey/50 text-xs mt-4 max-w-xs">
                  The pipeline is extracting audio, transcribing speech, running visual
                  analysis, and synthesising insights with Claude AI.
                </p>
              </div>
            )}

            {hasError && !isComplete && (
              /* Error state */
              <div className="bg-broadlab-card border border-broadlab-red/30 rounded-xl p-8 flex flex-col items-center justify-center text-center">
                <div className="w-10 h-10 rounded-full bg-red-950/50 flex items-center justify-center mb-4">
                  <svg className="w-5 h-5 text-broadlab-red" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                      d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <p className="text-white font-medium">Analysis failed</p>
                <p className="text-broadlab-grey text-sm mt-1.5 max-w-sm">
                  Check the pipeline status on the left for the specific error.
                  Make sure all API keys are set in your .env file.
                </p>
                <button
                  onClick={() => navigate('/')}
                  className="mt-6 px-5 py-2 bg-broadlab-red text-white text-sm font-semibold rounded-lg hover:bg-broadlab-red-hover transition-colors"
                >
                  Try Again
                </button>
              </div>
            )}

            {isComplete && !hasError && result && (
              /* Results display */
              <div className="space-y-4">

                {/* Output mode tabs — only show if both modes are available */}
                {outputMode === 'both' && quickSummary && fullAnalysis && (
                  <div className="flex items-center gap-1 bg-broadlab-card border border-broadlab-border rounded-lg p-1 w-fit">
                    <TabButton
                      active={activeResultTab === 'quick'}
                      onClick={() => setActiveResultTab('quick')}
                      label="Quick Summary"
                    />
                    <TabButton
                      active={activeResultTab === 'full'}
                      onClick={() => setActiveResultTab('full')}
                      label="Full Analysis"
                    />
                  </div>
                )}

                {/* Quick summary */}
                {(activeResultTab === 'quick' || outputMode === 'quick') && quickSummary && (
                  <QuickSummary data={quickSummary} />
                )}

                {/* Full analysis */}
                {(activeResultTab === 'full' || outputMode === 'full') && fullAnalysis && (
                  <FullAnalysis data={fullAnalysis} />
                )}

                {/* PDF download (shown at bottom for quick summary view too) */}
                {outputMode !== 'quick' && activeResultTab === 'quick' && (
                  <div className="pt-2">
                    <PDFDownload sessionId={sessionId} brandName={brandName} />
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}

// Simple tab button component
function TabButton({ active, onClick, label }) {
  return (
    <button
      onClick={onClick}
      className={`
        px-4 py-1.5 rounded-md text-sm font-medium transition-all duration-150
        ${active
          ? 'bg-broadlab-red text-white'
          : 'text-broadlab-grey hover:text-white'
        }
      `}
    >
      {label}
    </button>
  )
}
