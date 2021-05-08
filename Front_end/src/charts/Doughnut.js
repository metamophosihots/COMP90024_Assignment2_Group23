import React from "react";
import { Chart } from "react-chartjs-2";

class DoughnutChart extends React.Component {
  constructor(props) {
    super(props);
    this.chartRef = React.createRef();
  }

  componentDidUpdate() {
    this.myChart.data.labels = this.props.data.label;
    this.myChart.data.datasets[0].data = this.props.value;
    this.myChart.update();
  }

  componentDidMount() {
    this.myChart = new Chart(this.chartRef.current, {
      type: "doughnut",
      data: {
        labels: this.props.label,
        datasets: [
          {
            data: this.props.value,
            backgroundColor: this.props.colors,
          },
        ],
      },
      options: {
        maintainAspectRatio: false,
        responsive: true,
      },
    });
  }

  render() {
    return <canvas ref={this.chartRef} />;
  }
}

export default DoughnutChart;
