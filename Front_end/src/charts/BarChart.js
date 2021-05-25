import React from "react";
import { Chart } from "react-chartjs-2";

class BarChart extends React.Component {
  constructor(props) {
    super(props);
    this.chartRef = React.createRef();
  }

  componentDidUpdate() {
    this.myChart.data.labels = this.props.data.labels;
    for (const [i, city] of this.props.data.datasets.entries()) {
      this.myChart.data.datasets[i].label = city.label;
      this.myChart.data.datasets[i].data = city.data;
      this.myChart.data.datasets[i].backgroundColor = city.backgroundColor;
    }
    this.myChart.options.plugins.title.text = this.props.text;
    this.myChart.update();
  }

  componentDidMount() {
    this.myChart = new Chart(this.chartRef.current, {
      type: "bar",
      data: this.props.data,
      options: {
        maintainAspectRatio: false,
        responsive: true,
        plugins: {
          title: {
            display: true,
            text: this.props.text,
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

export default BarChart;
