import { useMemo } from "react";
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

interface CustomTooltipProps {
  active?: boolean;
  payload?: Array<{ value: number }>;
  label?: string | number;
  total: number;
}

const PatternDistributionChart = ({ distribution }: Props) => {
  // Compute total count for percentage calculations
  const total = useMemo(() => distribution.reduce((sum, d) => sum + d.count, 0), [distribution]);
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
              content={<CustomTooltip total={total} />}
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

const CustomTooltip = ({ active, payload, label, total }: CustomTooltipProps) => {
  if (active && payload && payload.length) {
    const count = payload[0].value;
    const percentage = total ? ((count / total) * 100).toFixed(1) : null;
    return (
      <div className="custom-tooltip" style={{ background: "#0F172A", padding: "8px 12px", borderRadius: "8px", color: "#F8FAFC" }}>
        <p style={{ margin: 0 }}><strong>{label}</strong></p>
        <p style={{ margin: 0 }}>{count} occurrences{percentage ? ` (${percentage}%)` : ""}</p>
      </div>
    );
  }
  return null;
};

export default PatternDistributionChart;
