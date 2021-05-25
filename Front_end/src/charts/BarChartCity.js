import React from "react";
import { Chart } from "react-chartjs-2";

class BarChartCity extends React.Component {
  constructor(props) {
    super(props);
    this.chartRef = React.createRef();
  }

  componentDidUpdate() {
    this.myChart.data.labels = this.props.label;
    this.myChart.data.datasets[3].data = this.props.value;
    this.myChart.update();
  }

  componentDidMount() {
    this.myChart = new Chart(this.chartRef.current, {
      data: {
        labels: this.props.label,
        datasets: [
          {
            type: "line",
            label: "Diabetes per 10k population",
            backgroundColor: "#003f5c",
            yAxisID: "B",
            data: [12.91, 15.4, 6.42, 20.29, 9.53],
          },
          {
            type: "line",
            label: "Obisity (%) among adults",
            backgroundColor: "#ff6361",
            yAxisID: "B",
            data: [20.71, 18.64, 19.52, 18.37, 16.85],
          },
          {
            type: "line",
            label: "average income (10k)",
            backgroundColor: "#ffa600",
            yAxisID: "B",
            data: [7.7078, 7.0556, 6.9864, 8.2981, 8.1767],
          },
          {
            type: "bar",
            label: "Average food mentioned per 10000 tweets",
            backgroundColor: "rgba(75,192,192,1)",
            yAxisID: "A",
            data: this.props.value,
          },
        ],
      },
      options: {
        maintainAspectRatio: false,
        responsive: true,
        scales: {
          A: {
            type: "linear",
            position: "left",
            title: "# tweets",
            gridLines: {
              color: "rgba(0, 0, 0, 0)",
            },
          },
          B: {
            type: "linear",
            position: "right",
            grid: {
              display: false,
            },
          },
        },
        plugins: {
          title: {
            display: true,
            text: "Average food mentioned per 10000 tweets for each city",
            fontSize: 20,
          },
          legend: {
            display: true,
            position: "top",
          },
        },
      },
    });
  }

  render() {
    return <canvas ref={this.chartRef} />;
  }
}

export default BarChartCity;
