import BarChartCity from "./BarChartCity";
import BarChart from "./BarChart";

const MixChart = ({ type, type2, cityData, data, data2 }) => {
  if (type === "data") {
    if (type2 === 0)
      return (
        <BarChart
          data={data}
          text={"Average food name mentioned per 10000 tweets in each city"}
        />
      );
    else
      return (
        <BarChart data={data2} text={"Average food polarity in each city"} />
      );
  } else {
    return (
      <BarChartCity
        label={Object.keys(cityData)}
        value={Object.values(cityData)}
      />
    );
  }
};

export default MixChart;
