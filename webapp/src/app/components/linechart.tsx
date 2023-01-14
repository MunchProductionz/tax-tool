import { Line } from "react-chartjs-2";
import { randNumber } from "@ngneat/falso";

import { CHART_COLORS } from "../styles/colors";
import { Chart as ChartJS, LineController, LineElement, PointElement, LinearScale, Title, CategoryScale } from 'chart.js';
import { useEffect, useState } from "react";





ChartJS.register(LineController, LineElement, PointElement, LinearScale, CategoryScale, Title);    

const options = {
    responsive: true,
    plugins: {
        legend: {
            position: 'top' as const,
        },
        title: {
            display: true,
            text: 'Chart.js Line Chart',
        },
    }
}

interface LineChartProps {
  labels: any[],
  values: number[]
}

export function LineChart(props: LineChartProps) {
  const [chartData, setChartData] = useState<any>()

  useEffect(() => {
    setChartData({
      labels: props.labels,
      datasets: [
        {
          label: '',
          data: props.values,
          backgroundColor: 'rgba(255, 99, 132, 0.5)',
        },
      ],
    })

  }, [props])

  if (chartData)  return <Line options={options} data={chartData} />;
  else return null
}