import { useState, useEffect } from "react";
import MixChart from "./charts/MixChart";
import Menu from "./components/Menu";
import Wiki from "./components/Wiki";
import LeaderBoard from "./components/LeaderBoard";
import { Route, BrowserRouter as Router, Switch } from "react-router-dom";
import {
  FaChartBar,
  FaQuestion,
  FaRegTimesCircle,
  FaUndo,
} from "react-icons/fa";
import ReactSearchBox from "react-search-box";
import MixChart2 from "./charts/MixChart2";
import food from "./components/images/about_food.jpg";

function App() {
  const [type, setType] = useState("cityData");
  const [type1, setType1] = useState(0);
  const [type2, setType2] = useState(0);
  const [cityData, setCityData] = useState({});
  const [foodMask, setFoodMask] = useState({});
  const [display, setDisplay] = useState([]);
  const [data, setData] = useState({
    labels: [],
    datasets: [
      { label: "adelaide", backgroundColor: "#003f5c" },
      { label: "brisbane", backgroundColor: "#58508d" },
      { label: "melborne", backgroundColor: "#bc5090" },
      { label: "perth", backgroundColor: "#ff6361" },
      { label: "sydney", backgroundColor: "#ffa600" },
    ],
  });
  const [data2, setData2] = useState({
    labels: [],
    datasets: [
      { label: "adelaide", backgroundColor: "#003f5c" },
      { label: "brisbane", backgroundColor: "#58508d" },
      { label: "melborne", backgroundColor: "#bc5090" },
      { label: "perth", backgroundColor: "#ff6361" },
      { label: "sydney", backgroundColor: "#ffa600" },
    ],
  });
  const [maskedData, setMaskedData] = useState({
    labels: [],
    datasets: [{}, {}, {}, {}, {}],
  });
  const [maskedData2, setMaskedData2] = useState({
    labels: [],
    datasets: [{}, {}, {}, {}, {}],
  });
  const [polarData, setPolarData] = useState({
    labels: [],
    datasets: [...Array(20)].map((item) => ({
      data: [],
    })),
  });
  const [dailyData, setDailyData] = useState({
    labels: [],
    datasets: [...Array(15)].map((item) => ({
      data: [],
    })),
  });
  const [maskedPolarData, setMaskedPolarData] = useState({
    labels: [],
    datasets: [...Array(20)].map((item) => ({
      data: [],
    })),
  });
  const [startDateIndex, setStartDateIndex] = useState(0);
  const [endDateIndex, setEndDateIndex] = useState(510);
  const startDateDefault = new Date("2020-01-01");
  const endDateDefault = new Date();
  const [startDate, setStartDate] = useState(startDateDefault);
  const [endDate, setEndDate] = useState(endDateDefault);

  const REFRESH_TIME = 300000;
  const PER_TWEET = 10000;
  const HEADER = {
    method: "get",
    headers: new Headers({
      Authorization: "Basic " + btoa("admin:admin"),
    }),
  };

  useEffect(() => {
    initializeFood();
    fetchCityData();
    fetchTimeData();
    fetchDailyData();
    const interval = setInterval(() => {
      fetchCityData();
      fetchTimeData();
    }, REFRESH_TIME);
    return () => clearInterval(interval);
  }, []);

  // update cuisine data in each city
  useEffect(() => {
    //refresh masked data
    setMaskedData({
      labels: sliceByArray(data.labels, Object.values(foodMask)),
      datasets: data["datasets"].map((cityData) => ({
        ...cityData,
        data: sliceByArray(cityData["data"], Object.values(foodMask)),
      })),
    });
    setMaskedData2({
      labels: sliceByArray(data2.labels, Object.values(foodMask)),
      datasets: data2["datasets"].map((cityData) => ({
        ...cityData,
        data: sliceByArray(cityData["data"], Object.values(foodMask)),
      })),
    });
  }, [foodMask]);

  const [time, setTime] = useState(0);
  useEffect(() => {
    let refresh = 500;
    if (maskedPolarData.labels.length > 0) {
      refresh = REFRESH_TIME;
    }
    setMaskedPolarData({
      labels: polarData.labels.slice(startDateIndex, endDateIndex),
      datasets: polarData.datasets.map((item) => ({
        ...item,
        data: item.data.slice(startDateIndex, endDateIndex),
      })),
    });
    const timer = setTimeout(() => {
      setTime(time + 1);
    }, refresh);
    return () => {
      clearTimeout(timer);
    };
  }, [time]);

  useEffect(() => {
    if (maskedPolarData.datasets.length !== 0) {
      setMaskedPolarData({
        labels: polarData.labels.slice(startDateIndex, endDateIndex),
        datasets: polarData.datasets.map((item) => ({
          ...item,
          data: item.data.slice(startDateIndex, endDateIndex),
        })),
      });
    }
  }, [startDateIndex, endDateIndex]);

  const fetchTimeData = async () => {
    Promise.all([
      await fetch(
        "http://172.26.128.24:5984/twitter/_design/scenario2/_view/combine?group_level=2",
        HEADER
      ).then((res) => res.json()),
      await fetch("http://172.26.128.24:5984/stats/covid", HEADER).then((res) =>
        res.json()
      ),
      await fetch("http://172.26.128.24:5984/stats/temp", HEADER).then((res) =>
        res.json()
      ),
    ])
      .then((response) => {
        const city_polar = {};
        const dates = new Set();
        const colors = {
          adelaide: "#003f5c",
          brisbane: "#58508d",
          melbourne: "#bc5090",
          perth: "#ff6361",
          sydney: "#ffa600",
        };

        const polar_dataSets = [];
        for (const day of response[0]["rows"]) {
          if (day["key"][0] + " average polarity" in city_polar) {
            city_polar[day["key"][0] + " average polarity"].push(
              (day["value"]["total_polarity"] / day["value"]["total"]) *
                PER_TWEET
            );
            dates.add(day["key"][1]);
          } else {
            city_polar[day["key"][0] + " average polarity"] = [];
            city_polar[day["key"][0] + " average polarity"].push(
              (day["value"]["total_polarity"] / day["value"]["total"]) *
                PER_TWEET
            );
            dates.add(day["key"][1]);
          }

          if (day["key"][0] + " food average" in city_polar) {
            city_polar[day["key"][0] + " food average"].push(
              (day["value"]["food"] / day["value"]["total"]) * PER_TWEET * 10
            );
            dates.add(day["key"][1]);
          } else {
            city_polar[day["key"][0] + " food average"] = [];
            city_polar[day["key"][0] + " food average"].push(
              (day["value"]["food"] / day["value"]["total"]) * PER_TWEET * 10
            );
            dates.add(day["key"][1]);
          }
        }
        for (const city of Object.keys(colors)) {
          city_polar[city + " covid cases"] = Object.values(response[1][city]);
        }
        for (const city of Object.keys(colors)) {
          city_polar[city + " temperature"] = Object.values(response[2][city]);
        }

        for (const city of Object.keys(city_polar)) {
          const dash = [];
          let axis = "A";
          let hide = true;
          let label = city + ` per ${PER_TWEET} tweets`;
          if (city.split(" ")[0] === "melbourne") {
            hide = false;
          }
          if (city.split(" ")[1] === "food") {
            dash.push(2);
            label = city + ` per ${PER_TWEET * 10} tweets`;
          } else if (city.split(" ")[1] === "covid") {
            dash.push(15, 3, 3, 3);
            axis = "B";
            label = city;
          } else if (city.split(" ")[1] === "temperature") {
            dash.push(20, 3, 3, 3, 3, 3, 3, 3);
            axis = "B";
            label = city;
            hide = true;
          }

          polar_dataSets.push({
            label: label,
            data: city_polar[city],
            backgroundColor: colors[city.split(" ")[0]],
            borderColor: colors[city.split(" ")[0]],
            borderDash: dash,
            yAxisID: axis,
            hidden: hide,
          });
        }
        setPolarData({
          labels: Array.from(dates),
          datasets: polar_dataSets,
        });
      })
      .catch((err) => console.error(err));
  };

  const fetchDailyData = async () => {
    await fetch(
      "http://172.26.128.24:5984/twitter/_design/scenario3/_view/combine?group_level=3",
      HEADER
    )
      .then((res) => res.json())
      .then((res) => {
        const city = {};
        for (const row of res["rows"]) {
          city[row["key"][0]] = {};
        }
        for (const row of res["rows"]) {
          city[row["key"][0]][row["key"][1]] = [];
        }
        for (const row of res["rows"]) {
          city[row["key"][0]][row["key"][1]].push(
            (row["value"]["food"] / row["value"]["total"]) * PER_TWEET
          );
        }

        const dataSets = [];
        const colors = {
          adelaide: "#003f5c",
          brisbane: "#58508d",
          melbourne: "#bc5090",
          perth: "#ff6361",
          sydney: "#ffa600",
        };
        const dash = {
          2019: [],
          2020: [2],
          2021: [15, 3, 3, 3],
        };

        for (const c of Object.keys(city)) {
          let hide = true;
          if (c === "melbourne") {
            hide = false;
          }
          for (const year of Object.keys(city[c])) {
            dataSets.push({
              label: `${c} ${year}`,
              data: city[c][year],
              backgroundColor: colors[c],
              borderColor: colors[c],
              borderDash: dash[year],
              hidden: hide,
            });
          }
        }
        setDailyData({
          labels: [...Array(23).keys()],
          datasets: dataSets,
        });
      })
      .catch((err) => console.error(err));
  };

  const initializeFood = async () => {
    await fetch(
      "http://172.26.128.24:5984/twitter/_design/scenario1/_view/count?group_level=2",
      {
        method: "get",
        headers: new Headers({
          Authorization: "Basic " + btoa("admin:admin"),
        }),
      }
    )
      .then((response) => response.json())
      .then((res) => {
        const foods = {};
        for (const dataObj of res["rows"]) {
          foods[dataObj["key"][0]] = 0;
        }
        setFoodMask(foods);
      });
  };

  const fetchCityData = async () => {
    // get total tweets for each city
    const city_total = {};
    const city_food_average = {};
    await fetch(
      "http://172.26.128.24:5984/twitter/_design/scenario1/_view/total?group_level=2",
      {
        method: "get",
        headers: new Headers({
          Authorization: "Basic " + btoa("admin:admin"),
        }),
      }
    )
      .then((response) => response.json())
      .then((response) => {
        for (const city of response["rows"]) {
          city_total[city["key"]] = city["value"]["total"];
          city_food_average[city["key"]] =
            (city["value"]["food"] / city["value"]["total"]) * PER_TWEET;
        }
        setCityData(city_food_average);
      })
      .catch((err) => console.error(err));

    await fetch(
      "http://172.26.128.24:5984/twitter/_design/scenario1/_view/count?group_level=2",
      {
        method: "get",
        headers: new Headers({
          Authorization: "Basic " + btoa("admin:admin"),
        }),
      }
    )
      .then((response) => response.json())
      .then((res) => {
        const foods = {};
        const foods2 = {}; // for polarity
        const cities = {};
        const cities2 = {}; // for polarity
        // add all unique food and unique cities
        for (const dataObj of res["rows"]) {
          cities[dataObj["key"][1]] = [];
          cities2[dataObj["key"][1]] = [];
          foods[dataObj["key"][0]] = 0;
          foods2[dataObj["key"][0]] = 0;
        }

        for (const city of Object.keys(cities)) {
          for (const dataObj of res["rows"]) {
            if (dataObj["key"][1] === city) {
              foods[dataObj["key"][0]] =
                (dataObj["value"]["count"] * PER_TWEET) / city_total[city];
              foods2[dataObj["key"][0]] =
                dataObj["value"]["polarity"] / dataObj["value"]["count"];
            }
          }
          cities[city] = Object.values(foods);
          cities2[city] = Object.values(foods2);

          // refresh foods
          for (const key of Object.keys(foods)) {
            foods[key] = 0;
            foods2[key] = 0;
          }
        }
        const datasets = [];
        const datasets2 = [];
        const colors = {
          adelaide: "#003f5c",
          brisbane: "#58508d",
          melbourne: "#bc5090",
          perth: "#ff6361",
          sydney: "#ffa600",
        };

        for (const city of Object.keys(cities)) {
          datasets.push({
            label: city,
            data: cities[city],
            backgroundColor: colors[city],
          });
        }

        for (const city of Object.keys(cities2)) {
          datasets2.push({
            label: city,
            data: cities2[city],
            backgroundColor: colors[city],
          });
        }
        setData({
          labels: Object.keys(foods),
          datasets: datasets,
        });
        setData2({
          labels: Object.keys(foods2),
          datasets: datasets2,
        });
      })
      .catch((err) => console.error(err));
  };

  const dateDiff = (day1, day2) => {
    const result = Math.ceil(day2 - day1) / (1000 * 60 * 60 * 24);
    if (result > 0) {
      return Math.ceil(day2 - day1) / (1000 * 60 * 60 * 24) + 1;
    }
    return 0;
  };

  const sliceByArray = (array, sliceIndexArray) => {
    const result = [];
    for (const [i, add] of sliceIndexArray.entries()) {
      if (add) {
        result.push(array[i]);
      }
    }
    return result;
  };

  const addFood = (food) => {
    setFoodMask((oldFoodMask) => ({ ...oldFoodMask, [food]: 1 }));
    if (!display.includes(food)) {
      setDisplay((old) => [...old, food]);
    }
  };

  const deleteFood = (food) => {
    setFoodMask((oldFoodMask) => ({ ...oldFoodMask, [food]: 0 }));
    setDisplay((old) => old.filter((item) => item !== food));
  };

  const clearBar = () => {
    setFoodMask((old) => {
      const s = {};
      for (const key of Object.keys(old)) {
        s[key] = 0;
      }
      return s;
    });
    setDisplay([]);
  };

  return (
    <>
      <Router>
        <Switch>
          <Route path="/wiki">
            <Wiki />
          </Route>
          <Route path="/foodchart">
            <div className="grid-container3">
              <Menu />
              <div className="chart2">
                <div className="chart">
                  <MixChart
                    cityData={cityData}
                    data={maskedData}
                    data2={maskedData2}
                    type={type}
                    type2={type2}
                  />
                  <button className="myButton" onClick={() => setType("city")}>
                    <FaChartBar /> By City
                  </button>
                  <button className="myButton" onClick={() => setType("data")}>
                    <FaChartBar /> By Cuisine
                  </button>
                  <button
                    className="myButton"
                    onClick={() => setType2((old) => Math.abs(old - 1))}
                  >
                    <FaUndo /> {!type2 ? "Polarity" : "Count"}
                  </button>
                </div>
                <div className="bar">
                  <ReactSearchBox
                    placeholder="Search dish to add"
                    data={Object.keys(foodMask).map((food) => {
                      return { key: food, value: food };
                    })}
                    onSelect={(record) => {
                      addFood(record["key"]);
                    }}
                    fuseConfigs={{
                      threshold: 0.05,
                    }}
                  />
                  <button className="myButton2" onClick={clearBar}>
                    Clear
                  </button>
                  {display.map((item, index) => {
                    return (
                      <pre key={index}>
                        {item.padEnd(13)}
                        <FaRegTimesCircle
                          style={{ color: "red", cursor: "pointer" }}
                          onClick={() => deleteFood(item)}
                        />
                      </pre>
                    );
                  })}
                </div>
              </div>
            </div>
          </Route>
          <Route path="/timeseries">
            <div className="grid-container2">
              <Menu />
              <MixChart2
                type1={type1}
                dailyData={dailyData}
                maskedPolarData={maskedPolarData}
                startDate={startDate}
                endDate={endDate}
                onChange1={(value) => {
                  setStartDate(value);
                  setStartDateIndex(dateDiff(startDateDefault, value));
                }}
                onChange2={(value) => {
                  setEndDate(value);
                  setEndDateIndex(dateDiff(startDateDefault, value) + 1);
                }}
                onClick1={() => {
                  setType1(0);
                }}
                onClick2={() => {
                  setType1(1);
                }}
              />
            </div>
          </Route>
          <Route path="/home">
            <div className="grid-container">
              <div className="grid-header">
                <Menu />
              </div>
              <MixChart2
                type1={type1}
                dailyData={dailyData}
                maskedPolarData={maskedPolarData}
                startDate={startDate}
                endDate={endDate}
                onChange1={(value) => {
                  setStartDate(value);
                  setStartDateIndex(dateDiff(startDateDefault, value));
                }}
                onChange2={(value) => {
                  setEndDate(value);
                  setEndDateIndex(dateDiff(startDateDefault, value) + 1);
                }}
                onClick1={() => {
                  setType1(0);
                }}
                onClick2={() => {
                  setType1(1);
                }}
              />
              <div className="chart2">
                <div className="chart">
                  <MixChart
                    cityData={cityData}
                    data={maskedData}
                    data2={maskedData2}
                    type={type}
                    type2={type2}
                  />
                  <button className="myButton" onClick={() => setType("city")}>
                    <FaChartBar /> By City
                  </button>
                  <button className="myButton" onClick={() => setType("data")}>
                    <FaChartBar /> By Cuisine
                  </button>
                  <button
                    className="myButton"
                    onClick={() => setType2((old) => Math.abs(old - 1))}
                  >
                    <FaUndo /> {!type2 ? "Polarity" : "Count"}
                  </button>
                </div>
                <div className="bar">
                  <ReactSearchBox
                    placeholder="Search dish to add"
                    data={Object.keys(foodMask).map((food) => {
                      return { key: food, value: food };
                    })}
                    onSelect={(record) => {
                      addFood(record["key"]);
                    }}
                    fuseConfigs={{
                      threshold: 0.05,
                    }}
                  />
                  <button className="myButton2" onClick={clearBar}>
                    Clear
                  </button>
                  {display.map((item, index) => {
                    return (
                      <pre key={index}>
                        {item.padEnd(13)}
                        <FaRegTimesCircle
                          style={{ color: "red", cursor: "pointer" }}
                          onClick={() => deleteFood(item)}
                        />
                      </pre>
                    );
                  })}
                </div>
              </div>

              <div className="leader round-boarder">
                <div className="header">Leader Board</div>
                <LeaderBoard />
                <div className="header">
                  Curious what are these
                  <FaQuestion /> <br />
                  Head to FOOD WIKI!!!
                </div>
              </div>
            </div>
          </Route>
          <Route path="/">
            <div className="grid-container">
              <div className="grid-header">
                <Menu />
              </div>
              <div className="chart1">
                <div className="header">
                  Welcome to COMP90024 ‘Australia and Food’ project webpage!
                </div>
                <br />
                <p className="text">
                  Being an immigration country with a multicultural environment,
                  Australia welcomes people and cultures from all over the
                  world. For every culture, there is a unique food cuisine of
                  their own, which to some extent represents the culture itself.
                  Therefore, food seems to be like a symbol representing
                  Australia’s diversity and we choose to study how different
                  food are related to Australian people’s daily life.
                </p>
                <p className="text">
                  We attempts to find a large quantity of tweets relating to
                  food in Australia. This webpage provides comprehensive data
                  visualisation of these tweets and illustrates how Australia
                  people’s lifestyle and food preference pattern are closely
                  related.
                </p>
                <p className="text">
                  The food chart presents how often people mention foods on
                  Twitter and what’s people’s average emotion/sentiment towards
                  each type of food on the aggregate level. The time chart
                  demonstrades how people’s love to food changes dynamically
                  over time (each day and each hour in a day). You can choose to
                  click on the labels to decide which combinations of lines/bars
                  you want to see. We also constructed a leader board to rank
                  the favourite food for Australians.
                </p>
                <p className="text">
                  On the background, the data are continously updating and this
                  webpage is refreshed every 5 minutes. Feel free to play with
                  the charts, try different combinations and search for the food
                  you are interested in!
                </p>
                <br />
                <p className="end">——— Cluster and Cloud Computing Team 23</p>
              </div>
              <img src={food} className="leader" alt="Multicutural food" />
            </div>
          </Route>
        </Switch>
      </Router>
    </>
  );
}

export default App;
