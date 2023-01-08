import { Line } from "react-chartjs-2";
import { randNumber } from "@ngneat/falso";

import { CHART_COLORS } from "../styles/colors";
import { Chart as ChartJS, LineController, LineElement, PointElement, LinearScale, Title, CategoryScale } from 'chart.js';




export function LineChart(){
    ChartJS.register(LineController, LineElement, PointElement, LinearScale, CategoryScale, Title);    

    const labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July'];

    const data = {
    labels,
    datasets: [
        {
        label: 'Dataset 1',
        data: labels.map(() => randNumber({ min: -1000, max: 1000 })),
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
        },
        {
        label: 'Dataset 2',
        data: labels.map(() => randNumber({ min: -1000, max: 1000 })),
        borderColor: 'rgb(53, 162, 235)',
        backgroundColor: 'rgba(53, 162, 235, 0.5)',
    },
],
    };


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
    },
    };
    return(
        <Line 
            data={data}
            options={options}
        />
    )

}