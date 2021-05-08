import Doughnut from "./Doughnut";
import BarChart from "./BarChart";

const MixChart = ({ type, label, value }) => {
  if (type === "bar") {
    return <BarChart label={label} value={value} />;
  } else {
    return (
      <Doughnut
        label={label}
        value={value}
        colors={[
          "#a8e0ff",
          "#8ee3f5",
          "#70cad1",
          "#3e517a",
          "#b08ea2",
          "#BBB6DF",
        ]}
      />
    );
  }
};

export default MixChart;
