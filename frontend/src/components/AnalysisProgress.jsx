// AnalysisProgress.jsx — The 8-step progress indicator shown while the pipeline runs.
// Each step lights up (complete/running/error) as the backend sends Server-Sent Events.
// Steps that haven't started yet appear greyed out and waiting.

import React from 'react'

// The eight pipeline steps in display order
// "key" must match the step names sent by the backend in progress events
const PIPELINE_STEPS = [
  { key: 'extract_audio',  label: 'Extract Audio',    description: 'Pulling audio track from video' },
  { key: 'analyse_audio',  label: 'Analyse Audio',    description: 'Detecting tempo, energy, spectral features' },
  { key: 'transcribe',     label: 'Transcribe Speech', description: 'Converting speech to text with Whisper' },
  { key: 'extract_frames', label: 'Extract Frames',   description: 'Sampling visual frames every 6 seconds' },
  { key: 'rekognition',    label: 'Visual Analysis',  description: 'Running AWS Rekognition AI detection' },
  { key: 'genome',         label: 'Creative Genome',  description: 'Synthesising inputs with Claude AI' },
  { key: 'resonance',      label: 'Resonance Scoring', description: 'Scoring against your target audience' },
  { key: 'synthesis',      label: 'Final Report',     description: 'Generating complete analysis output' },
]

export default function AnalysisProgress({ progressEvents, isComplete, hasError }) {
  // Build a lookup of step key → status from the progress events array
  // Each event has: { step, status, message }
  const stepStatus = {}
  const stepMessages = {}

  progressEvents.forEach(event => {
    if (event.step && event.step !== 'error') {
      stepStatus[event.step] = event.status    // 'running' | 'complete' | 'error'
      stepMessages[event.step] = event.message
    }
  })

  // Find the currently running step (there should only be one at a time)
  const currentRunningStep = Object.entries(stepStatus)
    .find(([, status]) => status === 'running')?.[0]

  return (
    <div className="space-y-1">
      {PIPELINE_STEPS.map((step, index) => {
        const status = stepStatus[step.key] || 'pending'
        const message = stepMessages[step.key]

        return (
          <StepRow
            key={step.key}
            step={step}
            index={index}
            status={status}
            message={message}
          />
        )
      })}

      {/* Error message if the pipeline failed */}
      {hasError && (
        <div className="mt-4 p-4 bg-red-950/30 border border-broadlab-red/30 rounded-lg">
          <p className="text-broadlab-red text-sm font-medium">Analysis failed</p>
          <p className="text-broadlab-grey text-xs mt-1">
            {progressEvents.find(e => e.step === 'error')?.message ||
             'An unexpected error occurred. Check that all API keys are configured in your .env file.'}
          </p>
        </div>
      )}

      {/* Success message */}
      {isComplete && !hasError && (
        <div className="mt-4 p-4 bg-broadlab-red/5 border border-broadlab-red/20 rounded-lg animate-fade-in">
          <p className="text-white text-sm font-medium">Analysis complete</p>
          <p className="text-broadlab-grey text-xs mt-1">Loading your results...</p>
        </div>
      )}
    </div>
  )
}

// ---- STEP ROW SUB-COMPONENT ----

function StepRow({ step, index, status, message }) {
  return (
    <div className={`
      flex items-start gap-4 px-4 py-3 rounded-lg transition-all duration-300
      ${status === 'complete' ? 'bg-broadlab-card/60' : ''}
      ${status === 'running' ? 'bg-broadlab-card border border-broadlab-border step-enter' : ''}
      ${status === 'error' ? 'bg-red-950/20' : ''}
      ${status === 'pending' ? 'opacity-40' : ''}
    `}>
      {/* Step number / status icon */}
      <div className="flex-shrink-0 mt-0.5">
        {status === 'complete' && (
          <div className="w-6 h-6 rounded-full bg-broadlab-red/10 flex items-center justify-center">
            <svg className="w-3.5 h-3.5 text-broadlab-red" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
            </svg>
          </div>
        )}
        {status === 'running' && (
          <div className="w-6 h-6 rounded-full border-2 border-broadlab-red border-t-transparent animate-spin" />
        )}
        {status === 'error' && (
          <div className="w-6 h-6 rounded-full bg-red-950 flex items-center justify-center">
            <svg className="w-3.5 h-3.5 text-broadlab-red" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </div>
        )}
        {status === 'pending' && (
          <div className="w-6 h-6 rounded-full border border-broadlab-border flex items-center justify-center">
            <span className="text-broadlab-grey text-xs">{index + 1}</span>
          </div>
        )}
      </div>

      {/* Step label and message */}
      <div className="flex-1 min-w-0">
        <p className={`text-sm font-medium ${
          status === 'complete' ? 'text-white' :
          status === 'running' ? 'text-white' :
          status === 'error' ? 'text-broadlab-red' :
          'text-broadlab-grey'
        }`}>
          {step.label}
        </p>
        <p className="text-xs text-broadlab-grey mt-0.5 truncate">
          {message || step.description}
        </p>
      </div>

      {/* Timing indicator for running step */}
      {status === 'running' && (
        <div className="flex-shrink-0 flex items-center gap-1">
          <span className="w-1.5 h-1.5 rounded-full bg-broadlab-red animate-pulse" />
          <span className="w-1.5 h-1.5 rounded-full bg-broadlab-red animate-pulse delay-75" />
          <span className="w-1.5 h-1.5 rounded-full bg-broadlab-red animate-pulse delay-150" />
        </div>
      )}
    </div>
  )
}
