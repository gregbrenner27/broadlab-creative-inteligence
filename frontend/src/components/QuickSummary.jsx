// QuickSummary.jsx — Displays the Quick Summary output mode.
// A single clean card showing the verdict, score, top audience,
// strengths, gaps, and targeting recommendation.

import React from 'react'

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

export default function QuickSummary({ data }) {
  // data = report.report.quick_summary
  if (!data) return null

  const {
    verdict,
    overall_score,
    top_recommended_audience,
    three_strengths = [],
    two_critical_gaps = [],
    targeting_recommendation
  } = data

  const scoreColor = overall_score >= 8 ? 'text-green-400' :
                     overall_score >= 6 ? 'text-broadlab-red' :
                     overall_score >= 4 ? 'text-yellow-500' : 'text-red-500'

  return (
    <div className="space-y-4 animate-fade-in">

      {/* ---- VERDICT + SCORE ---- */}
      <div className="bg-broadlab-card border border-broadlab-border rounded-xl p-6">
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1">
            <p className="text-xs font-semibold tracking-widest text-broadlab-grey uppercase mb-2">
              Overall Verdict
            </p>
            <p className="text-white text-lg font-medium leading-relaxed">
              {verdict}
            </p>
          </div>
          {/* Big score number */}
          <div className="flex-shrink-0 text-right">
            <p className="text-xs font-semibold tracking-widest text-broadlab-grey uppercase mb-1">
              Score
            </p>
            <div className="flex items-baseline gap-1">
              <span className={`text-5xl font-bold tabular-nums ${scoreColor}`}>
                {typeof overall_score === 'number' ? overall_score.toFixed(1) : overall_score}
              </span>
              <span className="text-broadlab-grey text-lg">/10</span>
            </div>
            <TierBadge score={overall_score} />
          </div>
        </div>

        {/* Primary recommended audience */}
        {top_recommended_audience && (
          <div className="mt-4 pt-4 border-t border-broadlab-border">
            <p className="text-xs font-semibold tracking-widest text-broadlab-grey uppercase mb-1.5">
              Primary Recommended Audience
            </p>
            <div className="inline-flex items-center gap-2 bg-broadlab-red/10 border border-broadlab-red/20 rounded-md px-3 py-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-broadlab-red" />
              <span className="text-white text-sm font-medium">{top_recommended_audience}</span>
            </div>
          </div>
        )}
      </div>

      {/* ---- STRENGTHS + GAPS ---- */}
      <div className="grid grid-cols-2 gap-4">

        {/* Strengths */}
        <div className="bg-broadlab-card border border-broadlab-border rounded-xl p-5">
          <p className="text-xs font-semibold tracking-widest text-broadlab-grey uppercase mb-3">
            Key Strengths
          </p>
          <ul className="space-y-2.5">
            {three_strengths.map((strength, i) => (
              <li key={i} className="flex items-start gap-2.5">
                <span className="flex-shrink-0 w-4 h-4 rounded-full bg-broadlab-red/10 flex items-center justify-center mt-0.5">
                  <svg className="w-2.5 h-2.5 text-broadlab-red" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                  </svg>
                </span>
                <p className="text-sm text-broadlab-grey leading-snug">{strength}</p>
              </li>
            ))}
          </ul>
        </div>

        {/* Gaps */}
        <div className="bg-broadlab-card border border-broadlab-border rounded-xl p-5">
          <p className="text-xs font-semibold tracking-widest text-broadlab-grey uppercase mb-3">
            Critical Gaps
          </p>
          <ul className="space-y-2.5">
            {two_critical_gaps.map((gap, i) => (
              <li key={i} className="flex items-start gap-2.5">
                <span className="flex-shrink-0 w-4 h-4 rounded-full bg-red-950/50 flex items-center justify-center mt-0.5">
                  <svg className="w-2.5 h-2.5 text-broadlab-red" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </span>
                <p className="text-sm text-broadlab-grey leading-snug">{gap}</p>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* ---- TARGETING RECOMMENDATION ---- */}
      {targeting_recommendation && (
        <div className="bg-broadlab-card border border-broadlab-red/20 rounded-xl p-5">
          <p className="text-xs font-semibold tracking-widest text-broadlab-red uppercase mb-3">
            Targeting Recommendation
          </p>
          <p className="text-broadlab-grey text-sm leading-relaxed">
            {targeting_recommendation}
          </p>
        </div>
      )}
    </div>
  )
}
