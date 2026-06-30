import React from 'react';
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from 'recharts';

interface Props {
  chartType: 'health' | 'nodes' | 'risk' | 'forecast';
  data: any[];
}

const CustomTooltip = ({ active, payload, label, chartType }: any) => {
  if (active && payload && payload.length) {
    return (
      <div style={{ backgroundColor: '#1e1e2d', border: '1px solid #333', padding: '10px', color: '#fff', borderRadius: '8px' }}>
        <p style={{ margin: '0 0 5px 0', fontSize: '12px', color: '#94A3B8' }}>{new Date(label).toLocaleString()}</p>
        {payload.map((entry: any, index: number) => (
          <p key={`item-${index}`} style={{ margin: 0, fontWeight: 'bold', color: entry.color }}>
            {entry.name}: {entry.value}
          </p>
        ))}
      </div>
    );
  }
  return null;
};

const TrendAnalyticsChart = ({ chartType, data }: Props) => {
  if (!data || data.length === 0) return null;

  const getChartContent = () => {
    switch (chartType) {
      case 'health':
        return (
          <>
            <h3 style={{ marginBottom: '20px', color: '#fff', fontSize: '1.2rem', fontWeight: 600 }}>Health Score Trend</h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={data}>
                <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                <XAxis 
                  dataKey="timestamp" 
                  stroke="#aaa" 
                  tickFormatter={(tick) => new Date(tick).toLocaleDateString()} 
                />
                <YAxis stroke="#aaa" domain={[0, 100]} />
                <Tooltip content={<CustomTooltip chartType="health" />} />
                <Line type="monotone" dataKey="score" name="Health Score" stroke="#10b981" strokeWidth={2} dot={{ r: 3 }} activeDot={{ r: 5 }} />
              </LineChart>
            </ResponsiveContainer>
          </>
        );
      case 'nodes':
        // Map backend node fields if needed
        const nodeData = data.map((d: any) => ({
          name: d.node_id || d.name,
          anomalies: d.count || d.anomalies
        }));
        return (
          <>
            <h3 style={{ marginBottom: '20px', color: '#fff', fontSize: '1.2rem', fontWeight: 600 }}>Top Affected Nodes</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={nodeData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                <XAxis dataKey="name" stroke="#aaa" />
                <YAxis stroke="#aaa" />
                <Tooltip contentStyle={{ backgroundColor: '#1e1e2d', border: '1px solid #333', color: '#fff', borderRadius: '8px' }} />
                <Bar dataKey="anomalies" name="Anomalies" fill="#8884d8" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </>
        );
      default:
        return null;
    }
  };

  return (
    <div className="trend-analytics-chart" style={{ width: '100%', background: 'rgba(255,255,255,0.02)', padding: '24px', borderRadius: '12px', marginBottom: '24px', fontFamily: "'Inter', sans-serif" }}>
      {getChartContent()}
    </div>
  );
};

export default TrendAnalyticsChart;
