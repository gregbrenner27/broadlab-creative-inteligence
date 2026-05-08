// main.jsx — The entry point for the React application.
// React renders into the <div id="root"> in index.html.
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'  // global styles including Tailwind

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
