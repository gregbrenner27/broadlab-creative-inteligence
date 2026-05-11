// FullAnalysis.jsx — Tabbed layout for the Full Analysis output mode.
// Four tabs: Overview, Creative Genome, Resonance Scores, Targeting.

import React, { useState, useEffect } from 'react'

const TABS = [
  { key: 'overview',  label: 'Overview' },
  { key: 'genome',    label: 'Creative Genome' },
  { key: 'resonance', label: 'Resonance Scores' },
  { key: 'targeting', label: 'Targeting' },
]

export default function FullAnalysis({ data }) {
  const [activeTab, setActiveTab] = useState('overview')

  // data = report.report.full_analysis
  if (!data) return null

  return (
    <div className="space-y-4 animate-fade-in">

      {/* ---- TABS ---- */}
      <div className="flex items-center gap-1 border-b border-broadlab-border">
        {TABS.map(tab => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key)}
            className={`
              px-4 py-2.5 text-sm font-medium transition-all duration-150 border-b-2 -mb-px
              ${activeTab === tab.key
                ? 'text-white border-broadlab-red'
                : 'text-broadlab-grey border-transparent hover:text-white hover:border-broadlab-border'
              }
            `}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* ---- TAB CONTENT ---- */}
      <div>
        {activeTab === 'overview'  && <OverviewTab data={data} />}
        {activeTab === 'genome'    && <GenomeTab data={data} />}
        {activeTab === 'resonance' && <ResonanceTab data={data} />}
        {activeTab === 'targeting' && <TargetingTab data={data} />}
      </div>
    </div>
  )
}

// ---- OVERVIEW TAB ----
function OverviewTab({ data }) {
  const scoreColor = data.overall_score >= 8 ? 'text-green-400' :
                     data.overall_score >= 6 ? 'text-broadlab-red' :
                     data.overall_score >= 4 ? 'text-yellow-500' : 'text-red-500'

  return (
    <div className="space-y-4">
      {/* Verdict + score */}
      <Card>
        <div className="flex items-start justify-between gap-6">
          <div className="flex-1">
            <Label>Overall Verdict</Label>
            <p className="text-white text-base leading-relaxed mt-2">{data.overall_verdict}</p>
          </div>
          <div className="text-right flex-shrink-0">
            <Label>Overall Score</Label>
            <div className="flex items-baseline gap-1 mt-1">
              <span className={`text-5xl font-bold tabular-nums ${scoreColor}`}>
                {typeof data.overall_score === 'number' ? data.overall_score.toFixed(1) : data.overall_score}
              </span>
              <span className="text-broadlab-grey text-lg">/10</span>
            </div>
            <TierBadge score={data.overall_score} />
          </div>
        </div>
      </Card>

      {/* DAIVID cohort */}
      {data.daivid_cohort_analysis && (
        <Card>
          <Label>Dominant DAIVID Cohort</Label>
          <div className="mt-2 flex items-center gap-3">
            <span className="inline-block bg-broadlab-red/10 border border-broadlab-red/20 text-broadlab-red text-sm font-semibold px-3 py-1 rounded-md">
              {data.daivid_cohort_analysis.dominant_cohort}
            </span>
          </div>
          {data.daivid_cohort_analysis.cohort_meaning && (
            <p className="text-broadlab-grey text-sm mt-3 leading-relaxed">
              {data.daivid_cohort_analysis.cohort_meaning}
            </p>
          )}
          {data.daivid_cohort_analysis.secondary_signals && (
            <p className="text-broadlab-grey/60 text-xs mt-2">
              {data.daivid_cohort_analysis.secondary_signals}
            </p>
          )}
        </Card>
      )}

      {/* Creative flags summary */}
      {data.creative_flags && (
        <div className="grid grid-cols-2 gap-4">
          <Card title="Working Well">
            <ul className="space-y-2 mt-2">
              {(data.creative_flags.working_well || []).map((item, i) => (
                <li key={i} className="text-sm text-broadlab-grey flex items-start gap-2">
                  <span className="text-broadlab-red mt-0.5">+</span> {item}
                </li>
              ))}
            </ul>
          </Card>
          <Card title="Not Working">
            <ul className="space-y-2 mt-2">
              {(data.creative_flags.not_working || []).map((item, i) => (
                <li key={i} className="text-sm text-broadlab-grey flex items-start gap-2">
                  <span className="text-broadlab-red mt-0.5">!</span> {item}
                </li>
              ))}
            </ul>
          </Card>
        </div>
      )}
    </div>
  )
}

// ---- GENOME TAB ----
function GenomeTab({ data }) {
  return (
    <div className="space-y-4">
      {data.creative_genome_narrative && (
        <Card title="Creative Genome Narrative">
          <p className="text-broadlab-grey text-sm leading-relaxed whitespace-pre-line mt-2">
            {data.creative_genome_narrative}
          </p>
        </Card>
      )}
      {data.future_integration_note && (
        <Card>
          <Label>Future Integration Note</Label>
          <p className="text-broadlab-grey/60 text-xs leading-relaxed mt-2 italic">
            {data.future_integration_note}
          </p>
        </Card>
      )}
    </div>
  )
}

// ---- RESONANCE SCORES TAB ----
function ResonanceTab({ data }) {
  const personas = data.persona_scorecards || []

  if (!personas.length) {
    return <p className="text-broadlab-grey text-sm">No persona scores available.</p>
  }

  return (
    <div className="space-y-6">
      {personas.map((persona, i) => (
        <PersonaScorecard key={i} persona={persona} />
      ))}
    </div>
  )
}

function PersonaScorecard({ persona }) {
  const [mounted, setMounted] = useState(false)
  useEffect(() => {
    const t = setTimeout(() => setMounted(true), 50)
    return () => clearTimeout(t)
  }, [])

  const dimensions = [
    { key: 'emotional_power',        label: 'Emotional Power',         weight: '30%' },
    { key: 'emotional_register_match', label: 'Emotional Register Match', weight: '25%' },
    { key: 'identity_signal_fit',    label: 'Identity Signal Fit',     weight: '20%' },
    { key: 'motivational_alignment', label: 'Motivational Alignment',  weight: '15%' },
    { key: 'attention_architecture_fit', label: 'Attention Architecture', weight: '10%' },
  ]

  const scores = persona.dimension_scores || {}
  const reasoning = persona.dimension_reasoning || {}

  const budgetColor = persona.budget_concentration === 'High' ? 'text-green-400 bg-green-400/10 border-green-400/20' :
                      persona.budget_concentration === 'Medium' ? 'text-yellow-400 bg-yellow-400/10 border-yellow-400/20' :
                      persona.budget_concentration === 'Low' ? 'text-orange-400 bg-orange-400/10 border-orange-400/20' :
                      'text-red-400 bg-red-400/10 border-red-400/20'

  return (
    <div className="bg-broadlab-card border border-broadlab-border rounded-xl overflow-hidden">
      {/* Persona header */}
      <div className="px-5 py-4 border-b border-broadlab-border flex items-center justify-between">
        <div>
          <h3 className="text-white font-semibold">{persona.persona_name}</h3>
          <p className="text-broadlab-grey text-xs mt-0.5">Resonance Scorecard</p>
        </div>
        <div className="flex items-center gap-3">
          <div className={`text-xs font-semibold px-2.5 py-1 rounded border ${budgetColor}`}>
            {persona.budget_concentration} Concentration
          </div>
          <div className="text-right">
            <p className="text-xs text-broadlab-grey">Overall</p>
            <p className="text-2xl font-bold text-broadlab-red tabular-nums">
              {typeof persona.overall_score === 'number'
                ? persona.overall_score.toFixed(1)
                : persona.overall_score}
            </p>
            <TierBadge score={persona.overall_score} />
          </div>
        </div>
      </div>

      {/* Dimension scores */}
      <div className="divide-y divide-broadlab-border">
        {dimensions.map(dim => {
          const score = scores[dim.key]
          const reason = reasoning[dim.key]
          const pct = score != null ? (score / 10) * 100 : 0

          return (
            <div key={dim.key} className="px-5 py-3">
              <div className="flex items-center justify-between mb-1.5">
                <div className="flex items-center gap-2">
                  <span className="text-sm text-white font-medium">{dim.label}</span>
                  <span className="text-xs text-broadlab-grey/50">({dim.weight})</span>
                </div>
                <span className="text-sm font-bold text-broadlab-red tabular-nums">
                  {score != null ? score : '–'}/10
                </span>
              </div>
              {/* Score bar — animates from 0 on mount, staggered by index */}
              <div className="w-full bg-broadlab-muted rounded-full h-1.5 mb-2">
                <div
                  className="h-1.5 rounded-full bg-broadlab-red"
                  style={{
                    width: mounted ? `${pct}%` : '0%',
                    transition: `width 700ms cubic-bezier(0.4, 0, 0.2, 1) ${i * 80}ms`,
                  }}
                />
              </div>
              {reason && (
                <p className="text-xs text-broadlab-grey/70 leading-relaxed">{reason}</p>
              )}
            </div>
          )
        })}
      </div>

      {/* Strengths + Gaps */}
      <div className="grid grid-cols-2 divide-x divide-broadlab-border border-t border-broadlab-border">
        <div className="px-5 py-4">
          <Label>Strengths</Label>
          <ul className="space-y-1.5 mt-2">
            {(persona.strengths || []).map((s, i) => (
              <li key={i} className="text-xs text-broadlab-grey flex gap-2">
                <span className="text-broadlab-red flex-shrink-0">+</span>{s}
              </li>
            ))}
          </ul>
        </div>
        <div className="px-5 py-4">
          <Label>Gaps</Label>
          <ul className="space-y-1.5 mt-2">
            {(persona.gaps || []).map((g, i) => (
              <li key={i} className="text-xs text-broadlab-grey flex gap-2">
                <span className="text-broadlab-red flex-shrink-0">!</span>{g}
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Budget concentration rationale */}
      {persona.budget_concentration_rationale && (
        <div className="px-5 py-3 bg-broadlab-dark/40 border-t border-broadlab-border">
          <p className="text-xs text-broadlab-grey/70 italic">
            {persona.budget_concentration_rationale}
          </p>
        </div>
      )}
    </div>
  )
}

// ---- TARGETING TAB ----
function TargetingTab({ data }) {
  const targeting = data.targeting_recommendation || {}
  const flags = data.creative_flags || {}

  return (
    <div className="space-y-4">
      {targeting.reasoning && (
        <Card title="Targeting Recommendation">
          {targeting.primary_target && (
            <div className="mt-3">
              <Label>Concentrate Primary Budget</Label>
              <p className="text-white text-sm mt-1">{targeting.primary_target}</p>
            </div>
          )}
          {targeting.secondary_target && (
            <div className="mt-3">
              <Label>Secondary Budget</Label>
              <p className="text-broadlab-grey text-sm mt-1">{targeting.secondary_target}</p>
            </div>
          )}
          {targeting.deprioritise && (
            <div className="mt-3">
              <Label>Deprioritise</Label>
              <p className="text-broadlab-grey/60 text-sm mt-1">{targeting.deprioritise}</p>
            </div>
          )}
          <div className="mt-4 pt-4 border-t border-broadlab-border">
            <p className="text-broadlab-grey text-sm leading-relaxed">{targeting.reasoning}</p>
          </div>
          {targeting.postcode_note && (
            <div className="mt-3 p-3 bg-broadlab-muted/40 rounded-lg">
              <p className="text-broadlab-grey/60 text-xs italic">{targeting.postcode_note}</p>
            </div>
          )}
        </Card>
      )}

      {flags.improvement_recommendations?.length > 0 && (
        <Card title="Creative Improvement Recommendations">
          <ul className="space-y-3 mt-2">
            {flags.improvement_recommendations.map((rec, i) => (
              <li key={i} className="flex items-start gap-3">
                <span className="flex-shrink-0 w-5 h-5 rounded-full bg-broadlab-red/10 flex items-center justify-center mt-0.5">
                  <span className="text-broadlab-red text-xs font-bold">{i + 1}</span>
                </span>
                <p className="text-sm text-broadlab-grey leading-snug">{rec}</p>
              </li>
            ))}
          </ul>
        </Card>
      )}
    </div>
  )
}

// ---- SHARED UI ATOMS ----

function TierBadge({ score }) {
  const tier = score >= 8   ? { label: 'HIGH',         cls: 'text-green-400 bg-green-400/10 border-green-400/20' }
             : score >= 6   ? { label: 'MEDIUM',        cls: 'text-yellow-400 bg-yellow-400/10 border-yellow-400/20' }
             : score >= 4   ? { label: 'LOW',           cls: 'text-orange-400 bg-orange-400/10 border-orange-400/20' }
             :                { label: 'DEPRIORITISE',  cls: 'text-red-400 bg-red-400/10 border-red-400/20' }
  return (
    <span className={`inline-block mt-1.5 text-xs font-semibold tracking-wider px-2 py-0.5 rounded border ${tier.cls}`}>
      {tier.label}
    </span>
  )
}

function Card({ children, title }) {
  return (
    <div className="bg-broadlab-card border border-broadlab-border rounded-xl p-5">
      {title && <Label>{title}</Label>}
      {children}
    </div>
  )
}

function Label({ children }) {
  return (
    <p className="text-xs font-semibold tracking-widest text-broadlab-grey uppercase">
      {children}
    </p>
  )
}
