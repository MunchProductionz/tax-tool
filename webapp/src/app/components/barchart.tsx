import React, { useEffect, useState } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';
import { randNumber } from '@ngneat/falso';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

export const options = {
  responsive: true,
  plugins: {
    legend: {
      position: 'top' as const,
    },
    title: {
      display: true,
      text: 'Chart.js Bar Chart',
    },
  },
};



interface BarChartProps {
  labels: any[],
  values: number[]
}

export function BarChart(props: BarChartProps) {
  const [chartData, setChartData] = useState<any>()

  useEffect(() => {
    console.log(props)
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

  if (chartData)  return <Bar options={options} data={chartData} />;
  else return null
}