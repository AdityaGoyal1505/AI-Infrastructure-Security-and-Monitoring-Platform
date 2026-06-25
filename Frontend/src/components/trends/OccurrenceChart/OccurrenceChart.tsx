import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import type { Trend } from "../../../types/trends";

import "./OccurrenceChart.css";

interface Props {
  trends: Trend[];
}

const OccurrenceChart = ({ trends }: Props) => {
  const chartData = trends.map((item) => ({
    title: item.title,

    occurrences: item.occurrence_count,
  }));

  return (
    <div className="occurrence-chart-card">
      <div className="occurrence-chart-header">
        <h2>Occurrence Overview</h2>

        <p>Most recurring AI insights</p>
      </div>

      <div className="chart-wrapper">
        <ResponsiveContainer width="100%" height={350}>
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1E293B" />

            <XAxis
              dataKey="title"
              stroke="#94A3B8"
              tick={{
                fontSize: 12,
              }}
            />

            <YAxis stroke="#94A3B8" />

            <Tooltip
              contentStyle={{
                background: "#0F172A",

                border: "1px solid rgba(139,92,246,0.2)",

                borderRadius: "16px",
              }}
              labelStyle={{
                color: "#F8FAFC",
              }}
            />

            <defs>
              <linearGradient id="barGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#A855F7" />

                <stop offset="100%" stopColor="#3B82F6" />
              </linearGradient>
            </defs>

            <Bar
              dataKey="occurrences"
              radius={[12, 12, 0, 0]}
              fill="url(#barGradient)"
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default OccurrenceChart;
