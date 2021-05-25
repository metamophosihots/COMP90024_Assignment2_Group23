import { Link } from "react-router-dom";
import {
  FaHome,
  FaInfo,
  FaWikipediaW,
  FaChartLine,
  FaChartBar,
} from "react-icons/fa";

const Menu = () => {
  return (
    <div className="menu">
      <Link to="/home">
        <button className="button">
          <FaHome /> Home
        </button>
      </Link>
      <Link to="/">
        <button className="button">
          <FaInfo /> About
        </button>
      </Link>
      <Link to="/wiki">
        <button className="button">
          <FaWikipediaW /> Food Wiki
        </button>
      </Link>
      <Link to="/timeseries">
        <button className="button">
          <FaChartLine /> Time Chart
        </button>
      </Link>
      <Link to="/foodchart">
        <button className="button">
          <FaChartBar /> Food Chart
        </button>
      </Link>
    </div>
  );
};

export default Menu;
