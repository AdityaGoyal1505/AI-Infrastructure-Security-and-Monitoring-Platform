import React from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import "./PatternDistributionChart.css";

interface Props {
  distribution: { pattern: string; count: number }[];
}

const PatternDistributionChart = ({ distribution }: Props) => {
  if (!distribution || distribution.length === 0) return null;

  return (
    <div className="pattern-chart-card">
      <div className="pattern-chart-header">
        <h2>Pattern Distribution</h2>
        <p>Dynamic analysis of recurring AI patterns</p>
      </div>

      <div className="chart-wrapper">
        <ResponsiveContainer width="100%" height={350}>
          <BarChart data={distribution}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1E293B" />
            <XAxis
              dataKey="pattern"
              stroke="#94A3B8"
              tick={{ fontSize: 12 }}
            />
            <YAxis stroke="#94A3B8" />
            <Tooltip
              contentStyle={{
                background: "#0F172A",
                border: "1px solid rgba(139,92,246,0.2)",
                borderRadius: "16px",
                color: "#F8FAFC",
              }}
              itemStyle={{ color: "#F8FAFC" }}
            />
            <defs>
              <linearGradient id="patternGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#8B5CF6" />
                <stop offset="100%" stopColor="#3B82F6" />
              </linearGradient>
            </defs>
            <Bar
              dataKey="count"
              name="Occurrences"
              radius={[12, 12, 0, 0]}
              fill="url(#patternGradient)"
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default PatternDistributionChart;
