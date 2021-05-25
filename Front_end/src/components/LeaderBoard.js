import Table from "react-bootstrap/Table";
import { FaQuestion, FaFire } from "react-icons/fa";
import { useState, useEffect } from "react";

const LeaderBoard = () => {
  const [data, setData] = useState([]);

  const fetchData = async () => {
    await fetch(
      "http://172.26.128.24:5984/twitter/_design/scenario1/_view/count?group_level=1",
      {
        method: "get",
        headers: new Headers({
          Authorization: "Basic " + btoa("admin:admin"),
        }),
      }
    )
      .then((response) => response.json())
      .then((response) =>
        setData(
          response["rows"]
            .map((row) => ({ ...row, value: row["value"]["count"] }))
            .sort((a, b) => (a["value"] < b["value"] ? 1 : -1))
        )
      )
      .catch((err) => console.error(err));
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(() => {
      fetchData();
    }, 100000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="scroll">
      <Table striped bordered hover>
        <thead>
          <tr>
            <th className="a">Rank</th>
            <th className="a">Food Name</th>
            <th className="a">Trending Index</th>
          </tr>
        </thead>
        <tbody>
          {data.map((val, index) => {
            return (
              <tr key={index}>
                <td>{index + 1}</td>
                <td>{val["key"]}</td>
                <td>
                  {val["value"]} <FaFire />
                </td>
              </tr>
            );
          })}
        </tbody>
      </Table>
    </div>
  );
};

export default LeaderBoard;
