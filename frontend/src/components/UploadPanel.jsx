// UploadPanel.jsx — The drag-and-drop video upload area.
// Handles file selection via drag-and-drop or clicking to browse.
// Shows filename and estimated duration once a file is selected.

import React, { useState, useRef, useCallback } from 'react'

export default function UploadPanel({ onFileSelected, file }) {
  // dragging = true when user is hovering a file over the drop zone
  const [dragging, setDragging] = useState(false)
  const [error, setError] = useState('')

  // ref to the hidden file input element so we can trigger it programmatically
  const fileInputRef = useRef(null)

  // Handle when a file is dropped onto the drop zone
  const handleDrop = useCallback((e) => {
    e.preventDefault()
    setDragging(false)
    setError('')

    const droppedFile = e.dataTransfer.files[0]
    validateAndSet(droppedFile)
  }, [])

  // Handle when a file is selected via the file browser
  const handleFileInput = (e) => {
    setError('')
    validateAndSet(e.target.files[0])
  }

  // Check the file is an MP4 before accepting it
  const validateAndSet = (selectedFile) => {
    if (!selectedFile) return

    if (!selectedFile.name.toLowerCase().endsWith('.mp4') && selectedFile.type !== 'video/mp4') {
      setError('Only MP4 files are accepted. Please convert your video to MP4 format.')
      return
    }

    // 500MB file size limit
    if (selectedFile.size > 500 * 1024 * 1024) {
      setError('File is too large. Maximum size is 500MB.')
      return
    }

    onFileSelected(selectedFile)
  }

  // Format file size into human-readable form (e.g. "24.3 MB")
  const formatFileSize = (bytes) => {
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
  }

  return (
    <div className="space-y-3">
      {/* Section label */}
      <label className="block text-xs font-semibold tracking-widest text-broadlab-grey uppercase">
        Ad Creative
      </label>

      {/* Drop zone — changes appearance when dragging or file is selected */}
      <div
        onDragOver={(e) => { e.preventDefault(); setDragging(true) }}
        onDragLeave={() => setDragging(false)}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        className={`
          relative cursor-pointer rounded-lg border-2 border-dashed
          transition-all duration-200 p-8 text-center
          ${dragging
            ? 'border-broadlab-red bg-broadlab-red/5'
            : file
            ? 'border-broadlab-red/40 bg-broadlab-card'
            : 'border-broadlab-muted bg-broadlab-card hover:border-broadlab-grey/50'
          }
        `}
      >
        {/* Hidden file input — triggered when user clicks the drop zone */}
        <input
          ref={fileInputRef}
          type="file"
          accept=".mp4,video/mp4"
          className="hidden"
          onChange={handleFileInput}
        />

        {file ? (
          /* File selected state */
          <div className="space-y-2">
            {/* Checkmark icon */}
            <div className="flex items-center justify-center">
              <div className="w-10 h-10 rounded-full bg-broadlab-red/10 flex items-center justify-center">
                <svg className="w-5 h-5 text-broadlab-red" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
            </div>
            <p className="text-white font-medium text-sm">{file.name}</p>
            <p className="text-broadlab-grey text-xs">{formatFileSize(file.size)}</p>
            <p className="text-broadlab-grey text-xs opacity-60">Click to change file</p>
          </div>
        ) : (
          /* Empty state */
          <div className="space-y-3">
            {/* Upload icon */}
            <div className="flex items-center justify-center">
              <div className="w-12 h-12 rounded-full bg-broadlab-muted flex items-center justify-center">
                <svg className="w-6 h-6 text-broadlab-grey" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
                    d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
              </div>
            </div>
            <div>
              <p className="text-white text-sm font-medium">
                Drop your MP4 here, or <span className="text-broadlab-red">click to browse</span>
              </p>
              <p className="text-broadlab-grey text-xs mt-1">MP4 format only · Maximum 500MB</p>
            </div>
          </div>
        )}
      </div>

      {/* Error message */}
      {error && (
        <p className="text-broadlab-red text-xs flex items-center gap-1.5">
          <svg className="w-3.5 h-3.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd"
              d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z"
              clipRule="evenodd" />
          </svg>
          {error}
        </p>
      )}
    </div>
  )
}
