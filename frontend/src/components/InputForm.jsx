// InputForm.jsx — The campaign context and audience input form.
// Collects: brand name, category, campaign goal, target audience description,
// primary motivation, secondary audience, and output mode selection.

import React from 'react'

// The five motivation options that map to the research framework
const MOTIVATION_OPTIONS = [
  { value: 'Achievement', label: 'Achievement & Mastery', description: 'Driven by performance, progress, winning' },
  { value: 'Belonging',   label: 'Belonging & Social Validation', description: 'Driven by acceptance, community, connection' },
  { value: 'Security',    label: 'Security & Reliability', description: 'Driven by trust, consistency, reduced risk' },
  { value: 'Status',      label: 'Status & Aspiration', description: 'Driven by exclusivity, elevation, being admired' },
  { value: 'Value',       label: 'Value & Fairness', description: 'Driven by getting a good deal, not being exploited' },
]

const OUTPUT_MODES = [
  { value: 'quick', label: 'Quick Summary', description: 'Single card overview — ideal for fast decisions' },
  { value: 'full',  label: 'Full Analysis', description: 'Tabbed breakdown with all dimension scores' },
  { value: 'both',  label: 'Both + PDF', description: 'Complete analysis with downloadable PDF report' },
]

export default function InputForm({ formData, onChange, outputMode, onOutputModeChange }) {
  // Generic handler — updates a specific field in the parent formData
  const handleChange = (field) => (e) => {
    onChange({ ...formData, [field]: e.target.value })
  }

  return (
    <div className="space-y-8">

      {/* ---- SECTION: Campaign Context ---- */}
      <div className="space-y-4">
        <SectionLabel label="Campaign Context" />

        {/* Brand Name + Category row */}
        <div className="grid grid-cols-2 gap-4">
          <FormField
            label="Brand Name"
            required
            placeholder="e.g. Nike"
            value={formData.brand_name}
            onChange={handleChange('brand_name')}
          />
          <FormField
            label="Industry / Category"
            required
            placeholder="e.g. Sportswear"
            value={formData.category}
            onChange={handleChange('category')}
          />
        </div>

        {/* Campaign Goal */}
        <FormField
          label="Campaign Goal"
          required
          placeholder="e.g. Drive brand association with athletic achievement and competition"
          value={formData.campaign_goal}
          onChange={handleChange('campaign_goal')}
        />

        {/* Additional Context */}
        <FormField
          label="Additional Context"
          placeholder="Any relevant context about previous campaigns, brand guidelines, or specific targeting notes (optional)"
          value={formData.additional_context}
          onChange={handleChange('additional_context')}
          multiline
          rows={2}
        />
      </div>

      {/* ---- SECTION: Target Audience ---- */}
      <div className="space-y-4">
        <SectionLabel label="Target Audience" />

        {/* Audience Description */}
        <FormField
          label="Describe Your Target Audience"
          required
          placeholder="e.g. Young adult sports enthusiasts aged 18 to 34 who identify as athletic and competitive, primarily male, engaged with football and fitness content"
          value={formData.target_audience}
          onChange={handleChange('target_audience')}
          multiline
          rows={3}
        />

        {/* Primary Motivation dropdown */}
        <div className="space-y-1.5">
          <label className="block text-xs font-medium text-broadlab-grey uppercase tracking-wider">
            Primary Motivation <span className="text-broadlab-red">*</span>
          </label>
          <select
            value={formData.primary_motivation}
            onChange={handleChange('primary_motivation')}
            className="
              w-full bg-broadlab-card border border-broadlab-border rounded-md
              px-3 py-2.5 text-sm text-white
              focus:outline-none focus:border-broadlab-red
              transition-colors appearance-none cursor-pointer
            "
          >
            <option value="" disabled>Select the primary motivation</option>
            {MOTIVATION_OPTIONS.map(opt => (
              <option key={opt.value} value={opt.value}>
                {opt.label} — {opt.description}
              </option>
            ))}
          </select>
        </div>

        {/* Secondary Audience */}
        <FormField
          label="Secondary Audience"
          placeholder="Optional — describe a secondary audience if you want a second resonance score"
          value={formData.secondary_audience}
          onChange={handleChange('secondary_audience')}
          multiline
          rows={2}
        />
      </div>

      {/* ---- SECTION: Output Mode ---- */}
      <div className="space-y-3">
        <SectionLabel label="Output Format" />
        <div className="grid grid-cols-3 gap-3">
          {OUTPUT_MODES.map(mode => (
            <button
              key={mode.value}
              type="button"
              onClick={() => onOutputModeChange(mode.value)}
              className={`
                relative p-4 rounded-lg border text-left transition-all duration-150
                ${outputMode === mode.value
                  ? 'border-broadlab-red bg-broadlab-red/5 text-white'
                  : 'border-broadlab-border bg-broadlab-card text-broadlab-grey hover:border-broadlab-grey/40'
                }
              `}
            >
              {/* Selected indicator dot */}
              {outputMode === mode.value && (
                <span className="absolute top-3 right-3 w-2 h-2 rounded-full bg-broadlab-red" />
              )}
              <p className="text-sm font-semibold mb-1">{mode.label}</p>
              <p className="text-xs opacity-70 leading-relaxed">{mode.description}</p>
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}

// ---- SUB-COMPONENTS ----

// SectionLabel — small uppercase section divider label
function SectionLabel({ label }) {
  return (
    <div className="flex items-center gap-3">
      <span className="text-xs font-semibold tracking-widest text-broadlab-grey uppercase">
        {label}
      </span>
      <div className="flex-1 h-px bg-broadlab-border" />
    </div>
  )
}

// FormField — reusable text input or textarea with consistent styling
function FormField({ label, required, placeholder, value, onChange, multiline, rows = 1 }) {
  const baseClasses = `
    w-full bg-broadlab-card border border-broadlab-border rounded-md
    px-3 py-2.5 text-sm text-white placeholder-broadlab-grey/40
    focus:outline-none focus:border-broadlab-red
    transition-colors resize-none
  `

  return (
    <div className="space-y-1.5">
      <label className="block text-xs font-medium text-broadlab-grey uppercase tracking-wider">
        {label}
        {required && <span className="text-broadlab-red ml-1">*</span>}
      </label>
      {multiline ? (
        <textarea
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          rows={rows}
          className={baseClasses}
        />
      ) : (
        <input
          type="text"
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          className={baseClasses}
        />
      )}
    </div>
  )
}
