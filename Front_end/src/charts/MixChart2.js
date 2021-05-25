import React from "react";
import Line1 from "./Line1";
import Line2 from "./Line2";
import DatePicker from "react-date-picker";
import { FaChartLine } from "react-icons/fa";
function MixChart2({
  type1,
  dailyData,
  maskedPolarData,
  startDate,
  endDate,
  onChange1,
  onChange2,
  onClick1,
  onClick2,
}) {
  if (type1 === 0) {
    return (
      <div className="chart1 round-boarder">
        <Line1 data={maskedPolarData} />
        Start Date: <DatePicker value={startDate} onChange={onChange1} /> End
        Date: <DatePicker value={endDate} onChange={onChange2} />
        <button onClick={onClick1} className="myButton3">
          <FaChartLine /> Daily
        </button>
        <button onClick={onClick2} className="myButton3">
          <FaChartLine /> Hourly
        </button>
      </div>
    );
  } else if (type1 === 1) {
    return (
      <div className="chart1">
        <Line2 data={dailyData} />
        <button onClick={onClick1} className="myButton3">
          <FaChartLine /> Daily
        </button>
        <button onClick={onClick2} className="myButton3">
          <FaChartLine /> Hourly
        </button>
      </div>
    );
  }
}

export default MixChart2;
