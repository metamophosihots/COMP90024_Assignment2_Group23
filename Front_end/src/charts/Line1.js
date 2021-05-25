import React from "react";
import { Chart } from "react-chartjs-2";

class Line1 extends React.Component {
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
      this.myChart.data.datasets[i].yAxisID = city.yAxisID;
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
        scales: {
          A: {
            type: "linear",
            position: "left",
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
            text: "Statistics for each city since 01/01/2020",
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

export default Line1;
