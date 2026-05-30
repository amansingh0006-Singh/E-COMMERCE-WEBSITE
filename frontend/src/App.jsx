import { useEffect, useState } from "react";
import "./App.css";

function App() {

  const [products, setProducts] = useState([]);
  const [cart, setCart] = useState([]);

  const [showLogin, setShowLogin] =
    useState(false);

  const [email, setEmail] =
    useState("");

  const [password, setPassword] =
    useState("");

  const [loggedInUser,
    setLoggedInUser] =
    useState("");

  const [isLoggedIn,
    setIsLoggedIn] =
    useState(false);



  // LOAD USER + CART
  useEffect(() => {

    const savedUser =
      localStorage.getItem(
        "loggedInUser"
      );

    if (savedUser) {

      setLoggedInUser(savedUser);

      setIsLoggedIn(true);

      const savedCart =
        localStorage.getItem(
          `cart-${savedUser}`
        );

      if (savedCart) {

        setCart(
          JSON.parse(savedCart)
        );

      }

    }

  }, []);



  // SAVE CART
  useEffect(() => {

    if (loggedInUser) {

      localStorage.setItem(
        `cart-${loggedInUser}`,
        JSON.stringify(cart)
      );

    }

  }, [cart, loggedInUser]);



  // FETCH PRODUCTS
  useEffect(() => {

    fetch(
      "http://127.0.0.1:8000/products/"
    )
      .then((res) => res.json())
      .then((data) => {

        setProducts(data);

      });

  }, []);




  // ADD TO CART
  const addToCart = (product) => {

    if (!isLoggedIn) {

      alert(
        "Please Login First 🔐"
      );

      return;

    }

    const existingItem = cart.find(
      (item) =>
        item.id === product.id
    );

    if (existingItem) {

      const updatedCart =
        cart.map((item) =>

          item.id === product.id

            ? {
                ...item,
                quantity:
                  item.quantity + 1
              }

            : item
        );

      setCart(updatedCart);

    } else {

      setCart([
        ...cart,
        {
          ...product,
          quantity: 1
        }
      ]);

    }

  };



  // REMOVE FROM CART
  const removeFromCart =
    (productId) => {

    const existingItem =
      cart.find(
        (item) =>
          item.id === productId
      );

    if (
      existingItem.quantity === 1
    ) {

      setCart(
        cart.filter(
          (item) =>
            item.id !== productId
        )
      );

    } else {

      const updatedCart =
        cart.map((item) =>

          item.id === productId

            ? {
                ...item,
                quantity:
                  item.quantity - 1
              }

            : item
        );

      setCart(updatedCart);

    }

  };



  // CLEAR CART
  const clearCart = () => {

    setCart([]);

  };



  // LOGIN
  const loginUser = async () => {

    const response =
      await fetch(
        "http://127.0.0.1:8000/login",
        {
          method: "POST",

          headers: {
            "Content-Type":
              "application/json",
          },

          body: JSON.stringify({
            email,
            password,
          }),
        }
      );

    const data =
      await response.json();

    if (
      data.message ===
      "Login Successful 🔥"
    ) {

      setIsLoggedIn(true);

      setLoggedInUser(email);

      localStorage.setItem(
        "loggedInUser",
        email
      );

      const savedCart =
        localStorage.getItem(
          `cart-${email}`
        );

      if (savedCart) {

        setCart(
          JSON.parse(savedCart)
        );

      } else {

        setCart([]);

      }

      setShowLogin(false);

    } else {

      alert(
        "Wrong Email Password ❌"
      );

    }

  };



  // LOGOUT
  const logoutUser = () => {

    setIsLoggedIn(false);

    setLoggedInUser("");

    setCart([]);

    localStorage.removeItem(
      "loggedInUser"
    );

  };



  return (

    <div className="container">

      <h1 className="title">
        Bhartiye Products 🔥
      </h1>


      <h2 className="cart-count">

        Cart Items: {

          cart.reduce(
            (total, item) =>
              total +
              item.quantity,
            0
          )

        }

      </h2>



      <h2 className="total-price">

        Total Price: ₹

        {

          cart.reduce(
            (total, item) =>

              total +
              item.price *
              item.quantity,

            0
          )

        }

      </h2>



      <nav className="navbar">

        <h1 className="logo">
          Bhartiye Products 🛍️
        </h1>


        <div className="nav-right">

          <h2>

            🛒 {

              cart.reduce(
                (total, item) =>
                  total +
                  item.quantity,
                0
              )

            }

          </h2>



          {

            isLoggedIn ? (

              <div className="user-section">

                <h3>
                  {loggedInUser}
                </h3>

                <button
                  className="logout-btn"
                  onClick={
                    logoutUser
                  }
                >
                  Logout
                </button>

              </div>

            ) : (

              <button
                className="login-btn"
                onClick={() =>
                  setShowLogin(true)
                }
              >
                Login
              </button>

            )

          }

        </div>

      </nav>



      <div className="products-grid">

        {

          products.map((product) => (

            <div
              className="card"
              key={product.id}
            >

              <img
                src={product.image_url}
                alt={product.name}
                className="product-image"
              />

              <h2>
                {product.name}
              </h2>

              <p>
                {product.description}
              </p>

              <h3>
                ₹ {product.price}
              </h3>

              <button
                onClick={() =>
                  addToCart(product)
                }
              >
                Add To Cart
              </button>

            </div>

          ))

        }

      </div>




      <div className="cart-section">

        <h1>
          Shopping Cart 🛒
        </h1>


        <button
          className="clear-btn"
          onClick={clearCart}
        >
          Clear Cart
        </button>



        {

          cart.map(
            (item, index) => (

              <div
                className="cart-item"
                key={index}
              >

                <img
                  src={item.image_url}
                  alt=""
                />

                <div>

                  <h3>
                    {item.name}
                  </h3>

                  <p>

                    ₹ {

                      item.price *
                      item.quantity

                    }

                  </p>

                  <p>

                    Quantity:
                    {item.quantity}

                  </p>

                  <button
                    className="remove-btn"
                    onClick={() =>
                      removeFromCart(
                        item.id
                      )
                    }
                  >
                    Remove
                  </button>

                </div>

              </div>

            )
          )

        }

      </div>





      {

        showLogin && (

          <div className="login-popup">

            <div className="login-box">

              <h2>
                Login 🔐
              </h2>


              <input
                type="email"
                placeholder="Enter Email"
                value={email}
                onChange={(e) =>
                  setEmail(
                    e.target.value
                  )
                }
              />


              <input
                type="password"
                placeholder="Enter Password"
                value={password}
                onChange={(e) =>
                  setPassword(
                    e.target.value
                  )
                }
              />


              <button
                onClick={loginUser}
              >
                Login
              </button>



              <button
                className="close-btn"
                onClick={() =>
                  setShowLogin(false)
                }
              >
                Close
              </button>

            </div>

          </div>

        )

      }

    </div>

  );

}

export default App;