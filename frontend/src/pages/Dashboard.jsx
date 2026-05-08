// Dashboard.jsx — Screen 1: the main upload and input form.
// When the user clicks "Run Analysis", this page submits the form to the
// backend API and navigates to the Results page with the session ID.

import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import UploadPanel from '../components/UploadPanel'
import InputForm from '../components/InputForm'

// The initial empty state for the campaign context form
const EMPTY_FORM = {
  brand_name: '',
  category: '',
  campaign_goal: '',
  target_audience: '',
  primary_motivation: '',
  additional_context: '',
  secondary_audience: ''
}

export default function Dashboard() {
  const navigate = useNavigate()

  // State — the uploaded file, form data, output mode, and submission status
  const [file, setFile] = useState(null)
  const [formData, setFormData] = useState(EMPTY_FORM)
  const [outputMode, setOutputMode] = useState('both')
  const [submitting, setSubmitting] = useState(false)
  const [submitError, setSubmitError] = useState('')
  const [nikeLoading, setNikeLoading] = useState(false)

  // One-click Nike test — triggers the pre-loaded test case on the backend
  const handleNikeTest = async () => {
    setNikeLoading(true)
    setSubmitError('')
    try {
      const response = await fetch('/api/test-nike', { method: 'POST' })
      if (!response.ok) {
        const err = await response.json().catch(() => ({}))
        throw new Error(err.detail || `Server error: ${response.status}`)
      }
      const { session_id } = await response.json()
      navigate(`/results/${session_id}`, {
        state: { brandName: 'Nike — Why Do It 2025', outputMode: 'both' }
      })
    } catch (err) {
      setSubmitError(err.message)
      setNikeLoading(false)
    }
  }

  // The "Run Analysis" button is only active when required fields are filled
  const isReady =
    file !== null &&
    formData.brand_name.trim() !== '' &&
    formData.category.trim() !== '' &&
    formData.campaign_goal.trim() !== '' &&
    formData.target_audience.trim() !== '' &&
    formData.primary_motivation !== ''

  const handleSubmit = async () => {
    if (!isReady || submitting) return

    setSubmitting(true)
    setSubmitError('')

    try {
      // Build a FormData object to send the file and all text fields together
      // This is the standard way to submit files via HTTP
      const data = new FormData()
      data.append('video', file)
      data.append('brand_name', formData.brand_name)
      data.append('category', formData.category)
      data.append('campaign_goal', formData.campaign_goal)
      data.append('target_audience', formData.target_audience)
      data.append('primary_motivation', formData.primary_motivation)
      data.append('additional_context', formData.additional_context || '')
      data.append('secondary_audience', formData.secondary_audience || '')
      data.append('output_mode', outputMode)

      // POST to the backend API
      const response = await fetch('/api/analyse', {
        method: 'POST',
        body: data  // FormData handles the Content-Type header automatically
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `Server error: ${response.status}`)
      }

      const { session_id } = await response.json()

      // Navigate to the results page with the session ID
      navigate(`/results/${session_id}`, {
        state: { brandName: formData.brand_name, outputMode }
      })

    } catch (err) {
      setSubmitError(err.message || 'Failed to start analysis. Is the backend server running?')
      setSubmitting(false)
    }
  }

  return (
    <div className="min-h-screen bg-broadlab-dark">
      {/* ---- TOP NAV BAR ---- */}
      <header className="border-b border-broadlab-border px-8 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          {/* Broadlab wordmark */}
          <span className="text-white font-bold text-lg tracking-tight">BROADLAB</span>
          <span className="w-px h-4 bg-broadlab-border" />
          <span className="text-broadlab-grey text-sm">Creative Intelligence</span>
        </div>
        {/* Version badge */}
        <span className="text-xs text-broadlab-grey/50 font-mono">v1.0</span>
      </header>

      {/* ---- MAIN CONTENT ---- */}
      <main className="max-w-3xl mx-auto px-6 py-10">

        {/* Page title */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white tracking-tight">
            Creative Analysis
          </h1>
          <p className="text-broadlab-grey text-sm mt-2 max-w-lg leading-relaxed">
            Upload a video ad and provide campaign context. The system will analyse
            the creative across five dimensions and produce a resonance scorecard
            for your target audience.
          </p>
        </div>

        {/* ---- NIKE TEST SHORTCUT ---- */}
        <div className="mb-8 p-4 bg-broadlab-card border border-broadlab-border rounded-xl flex items-center justify-between gap-4">
          <div>
            <p className="text-white text-sm font-semibold">Nike — Why Do It 2025</p>
            <p className="text-broadlab-grey text-xs mt-0.5">
              Pre-loaded test case · Uses existing Rekognition data · No AWS needed
            </p>
          </div>
          <button
            onClick={handleNikeTest}
            disabled={nikeLoading}
            className={`
              flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-semibold
              flex-shrink-0 transition-all duration-150
              ${nikeLoading
                ? 'bg-broadlab-muted text-broadlab-grey cursor-not-allowed'
                : 'bg-broadlab-red text-white hover:bg-broadlab-red-hover'
              }
            `}
          >
            {nikeLoading ? (
              <>
                <div className="w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                Starting...
              </>
            ) : (
              <>Run Nike Test</>
            )}
          </button>
        </div>

        {/* ---- FORM CARD ---- */}
        <div className="bg-broadlab-card border border-broadlab-border rounded-2xl overflow-hidden">

          {/* Upload section */}
          <div className="p-6 border-b border-broadlab-border">
            <UploadPanel onFileSelected={setFile} file={file} />
          </div>

          {/* Campaign inputs section */}
          <div className="p-6">
            <InputForm
              formData={formData}
              onChange={setFormData}
              outputMode={outputMode}
              onOutputModeChange={setOutputMode}
            />
          </div>

          {/* Submit bar */}
          <div className="px-6 py-5 bg-broadlab-dark/30 border-t border-broadlab-border flex items-center justify-between gap-4">

            {/* Validation hint */}
            {!isReady && (
              <p className="text-broadlab-grey/50 text-xs">
                {!file
                  ? 'Upload an MP4 to continue'
                  : 'Fill in all required fields to continue'}
              </p>
            )}
            {isReady && (
              <p className="text-broadlab-grey/50 text-xs">
                Ready — click to start analysis
              </p>
            )}

            {/* Submit error */}
            {submitError && (
              <p className="text-broadlab-red text-xs flex-1">{submitError}</p>
            )}

            {/* Run Analysis button */}
            <button
              onClick={handleSubmit}
              disabled={!isReady || submitting}
              className={`
                flex items-center gap-2.5 px-6 py-2.5 rounded-lg font-semibold text-sm
                transition-all duration-150 flex-shrink-0
                ${isReady && !submitting
                  ? 'bg-broadlab-red text-white hover:bg-broadlab-red-hover shadow-lg shadow-broadlab-red/20'
                  : 'bg-broadlab-muted text-broadlab-grey cursor-not-allowed'
                }
              `}
            >
              {submitting ? (
                <>
                  <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  Starting...
                </>
              ) : (
                <>
                  Run Analysis
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </>
              )}
            </button>
          </div>
        </div>

        {/* Methodology note */}
        <p className="text-broadlab-grey/40 text-xs text-center mt-6 leading-relaxed">
          Scores are derived from Emotional Power, Emotional Register Match, Identity Signal Fit,
          Motivational Alignment, and Attention Architecture Fit.
          Based on the DAIVID 39-emotion framework and System1 ad effectiveness research.
        </p>
      </main>
    </div>
  )
}
