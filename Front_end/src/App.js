import { useState, useEffect } from "react";
import MixChart from "./charts/MixChart";
// import Map from "./googleMap/Map";

let labelData = ["Jan", "Feb", "Mar", "Apr", "May"];
let valueData = [45, 67, 44, 78, 82];

function App() {
  const [type, setType] = useState("bar");
  const [label, setLabel] = useState(labelData);
  const [value, setValue] = useState(valueData);

  function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  async function test() {
    for (var i = 0; i < 100; i++) {
      valueData = value.map((value) =>
        Math.random() < 0.5
          ? value + Math.floor(Math.random() * 10)
          : value - Math.floor(Math.random() * 10)
      );
      setLabel(labelData);
      setValue(valueData);
      await sleep(1000);
    }
  }

  const getData = () => {
    let lab = [];
    let val = [];

    fetch("http://localhost:5984/rain/_design/all_data/_view/id", {
      method: "get",
      headers: new Headers({
        Authorization: "Basic " + btoa("admin:admin"),
      }),
    })
      .then((response) => response.json())
      .catch((err) => console.error(err))
      .then((data) => {
        for (const dataObj of data["rows"]) {
          lab.push(dataObj["key"]);
          val.push(dataObj["value"]);
        }
        setValue(val);
        setLabel(lab);
      });
  };

  useEffect(() => {
    getData();
  }, []);

  // ///hide month
  // const hide = (id) => {
  //   setRainData(rain.filter((month) => month.id !== id));
  // };

  const change = () => {
    setType((previous) => (previous === "bar" ? "doughnut" : "bar"));
  };

  // const BarButton = () => {
  //   return (
  //     <div>
  //       <button onClick={() => setRainData(rain)}>All</button>
  //       <button onClick={() => hide(1)}>Jan</button>
  //       <button onClick={() => hide(2)}>Feb</button>
  //     </div>
  //   );
  // };

  return (
    <>
      <div id="element1" className="navigator">
        <button onClick={change}>Change chart</button>
        <button onClick={test}>change data</button>
        <button onClick={getData}>Get data test</button>
      </div>
      <div id="element2" className="container">
        <div className="chart-container">
          <MixChart type={type} label={label} value={value} />
        </div>
        {/* <BarButton /> */}
        {/* <Map /> */}
      </div>
    </>
  );
}

export default App;
