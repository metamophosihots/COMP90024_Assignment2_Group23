import Menu from "./Menu";
import food1 from "./images/food1.jpeg";
import food2 from "./images/food2.jpeg";

const Wiki = ({ startStream, stopStream }) => {
  return (
    <div className="wiki-container">
      <div className="wiki-header">
        <Menu startStream={startStream} stopStream={stopStream} />
      </div>
      <ul className="b round-boarder">
        <div className="a">B</div>
        <li>
          <a
            href="https://en.wikipedia.org/wiki/Barbecue"
            target="_blank"
            rel="noreferrer"
          >
            BBQ
          </a>
        </li>
        <li>
          <a
            href="https://en.wikipedia.org/wiki/Bibimbap"
            target="_blank"
            rel="noreferrer"
          >
            Bibimbap
          </a>
        </li>
        <li>
          <a
            href="https://en.wikipedia.org/wiki/B%C3%B6rek"
            target="_blank"
            rel="noreferrer"
          >
            Borek
          </a>
        </li>
        <li>
          <a
            href="https://en.wikipedia.org/wiki/Bread"
            target="_blank"
            rel="noreferrer"
          >
            Bread
          </a>
        </li>
        <li>
          <a
            href="https://en.wikipedia.org/wiki/Hamburger"
            target="_blank"
            rel="noreferrer"
          >
            Burger
          </a>
        </li>
        <li>
          <a
            href="https://en.wikipedia.org/wiki/Burrito"
            target="_blank"
            rel="noreferrer"
          >
            Buritto
          </a>
        </li>
      </ul>
      <ul className="c round-boarder">
        <div className="a">C</div>
        <li>
          <a
            href="https://en.wikipedia.org/wiki/Cake"
            target="_blank"
            rel="noreferrer"
          >
            Cake
          </a>
        </li>
        <li>
          <a
            href="https://en.wikipedia.org/wiki/Potato_chip"
            target="_blank"
            rel="noreferrer"
          >
            Chips
          </a>
        </li>
        <li>
          <a
            href="https://en.wikipedia.org/wiki/Curry"
            target="_blank"
            rel="noreferrer"
          >
            Curry
          </a>
        </li>
      </ul>
      <ul className="d round-boarder">
        <div className="a">D</div>
        <li>
          <a
            href="https://en.wikipedia.org/wiki/Donuts"
            target="_blank"
            rel="noreferrer"
          >
            Donuts
          </a>
        </li>
        <li>
          <a
            href="https://en.wikipedia.org/wiki/Dumpling"
            target="_blank"
            rel="noreferrer"
          >
            Dumplings
          </a>
        </li>
      </ul>
      <ul className="f round-boarder">
        <div className="a">F</div>
        <li>
          <a
            href="https://en.wikipedia.org/wiki/Fried_chicken"
            target="_blank"
            rel="noreferrer"
          >
            Fried Chicken
          </a>
        </li>
      </ul>
      <ul className="h round-boarder">
        <div className="a">H</div>
        <li>
          <a
            href="https://en.wikipedia.org/wiki/Hot_dog"
            target="_blank"
            rel="noreferrer"
          >
            Hot dog
          </a>
        </li>
        <li>
          <a
            href="https://en.wikipedia.org/wiki/Hot_pot"
            target="_blank"
            rel="noreferrer"
          >
            Hot pot
          </a>
        </li>
        <li>
          <a
            href="https://en.wikipedia.org/wiki/Halal_snack_pack"
            target="_blank"
            rel="noreferrer"
          >
            HSP
          </a>
        </li>
      </ul>
      <ul className="k round-boarder">
        <div className="a">K</div>
        <li>
          <a
            href="https://en.wikipedia.org/wiki/Kebab"
            target="_blank"
            rel="noreferrer"
          >
            Kebab
          </a>
        </li>
        <li>
          <a
            href="https://en.wikipedia.org/wiki/Kimchi"
            target="_blank"
            rel="noreferrer"
          >
            Kimchi
          </a>
        </li>
      </ul>
      <ul className="l round-boarder">
        <div className="a">L</div>
        <li>
          <a
            href="https://en.wikipedia.org/wiki/Laksa"
            target="_blank"
            rel="noreferrer"
          >
            Laksa
          </a>
        </li>
        <li>
          <a
            href="https://en.wikipedia.org/wiki/Lamington"
            target="_blank"
            rel="noreferrer"
          >
            Lamington
          </a>
        </li>
        <li>
          <a
            href="https://en.wikipedia.org/wiki/Lasagne"
            target="_blank"
            rel="noreferrer"
          >
            Lasagna
          </a>
        </li>
      </ul>
      <ul className="p round-boarder">
        <div className="a">P</div>
        <li>
          <a
            href="https://en.wikipedia.org/wiki/Pasta"
            target="_blank"
            rel="noreferrer"
          >
            Pasta
          </a>
        </li>
        <li>
          <a
            href="https://en.wikipedia.org/wiki/Pho"
            target="_blank"
            rel="noreferrer"
          >
            Pho
          </a>
        </li>
        <li>
          <a
            href="https://en.wikipedia.org/wiki/Pie"
            target="_blank"
            rel="noreferrer"
          >
            Pita
          </a>
        </li>
        <li>
          <a
            href="https://en.wikipedia.org/wiki/Pita"
            target="_blank"
            rel="noreferrer"
          >
            Pita
          </a>
        </li>
        <li>
          <a
            href="https://en.wikipedia.org/wiki/Pizza"
            target="_blank"
            rel="noreferrer"
          >
            Pizza
          </a>
        </li>
      </ul>
      <ul className="r round-boarder">
        <div className="a">R & T</div>
        <li>
          <a
            href="https://en.wikipedia.org/wiki/Ramen"
            target="_blank"
            rel="noreferrer"
          >
            Ramen
          </a>
        </li>
        <li>
          <a
            href="https://en.wikipedia.org/wiki/Taco"
            target="_blank"
            rel="noreferrer"
          >
            Taco
          </a>
        </li>
        <li>
          <a
            href="https://en.wikipedia.org/wiki/Toast_(food)"
            target="_blank"
            rel="noreferrer"
          >
            Toast
          </a>
        </li>
      </ul>
      <ul className="s round-boarder">
        <div className="a">S & V</div>
        <li>
          <a
            href="https://en.wikipedia.org/wiki/Salad"
            target="_blank"
            rel="noreferrer"
          >
            Salad
          </a>
        </li>
        <li>
          <a
            href="https://en.wikipedia.org/wiki/Sausage"
            target="_blank"
            rel="noreferrer"
          >
            Sausage
          </a>
        </li>
        <li>
          <a
            href="https://en.wikipedia.org/wiki/Steak"
            target="_blank"
            rel="noreferrer"
          >
            Steak
          </a>
        </li>
        <li>
          <a
            href="https://en.wikipedia.org/wiki/Sushi"
            target="_blank"
            rel="noreferrer"
          >
            Sushi
          </a>
        </li>
        <li>
          <a
            href="https://en.wikipedia.org/wiki/Vegemite"
            target="_blank"
            rel="noreferrer"
          >
            Vegemite
          </a>
        </li>
      </ul>
      <img src={food1} className="img2" alt="Ingridiants" />
      <img src={food2} className="img1" alt="Asian cusine" />
    </div>
  );
};

export default Wiki;
