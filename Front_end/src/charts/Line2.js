import React from "react";
import { Chart } from "react-chartjs-2";

class Line2 extends React.Component {
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
      this.myChart.data.datasets[i].borderColor = city.borderColor;
      this.myChart.data.datasets[i].borderDash = city.borderDash;
      this.myChart.data.datasets[i].hidden = city.hidden;
    }
    this.myChart.update();
  }

  componentDidMount() {
    this.myChart = new Chart(this.chartRef.current, {
      type: "line",
      data: this.props.data,
      options: {
        maintainAspectRatio: false,
        responsive: true,
        elements: {
          point: {
            radius: 0,
          },
        },
        plugins: {
          title: {
            display: true,
            text: "Average food mentioned per 10000 tweets at different time each year each city",
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

export default Line2;
