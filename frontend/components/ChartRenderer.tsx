"use client";

import dynamic from "next/dynamic";

const Plot = dynamic(() => import("react-plotly.js"), { ssr: false });

type ChartRendererProps = {
  chart: Record<string, unknown>;
};

export default function ChartRenderer({ chart }: ChartRendererProps) {
  return (
    <Plot
      data={chart.data as never}
      layout={{ ...(chart.layout as object), autosize: true }}
      config={{ displayModeBar: false, responsive: true }}
      style={{ width: "100%", height: "320px" }}
    />
  );
}