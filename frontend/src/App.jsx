// App.jsx — The root component. Sets up page routing.
// React Router handles navigation between the Dashboard (input) and Results pages.
// Think of routes like URL paths: / = Dashboard, /results = Results page.

import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import Results from './pages/Results'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* The main upload/input screen */}
        <Route path="/" element={<Dashboard />} />

        {/* The results screen — receives the session ID via URL parameter */}
        <Route path="/results/:sessionId" element={<Results />} />

        {/* Redirect any unknown URL back to the dashboard */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}
