import wave from './static/images/wave.png';
import './App.css';
import { React, useState, useEffect } from 'react';
// import catalog from 'gsmarena-api';

// const brands = await catalog.getBrands();


var test_questions = new Object();
var test_questions = {
  "What is your budget?": [">10,000", "10,000-15,000", "15,000-20,000", "20,000-30,000", "30,000-40,000"],
  "What is your age group?": ["13-18", "18-30", "30-60", "60+"],
  "What is your screentime?": ["<1hr", "1-2hrs", "2-6hrs", "6+hrs"],
  "Do you care about how your phone looks?": ["Yes", "No"],
  "How many photos do you click in a day?": ["Not everyday", "1-2", "2-10", "10+"],
  "Which screen size do you prefer?": ["<5.5inches", "5-6inches", "6+inches"],
  "How much storage is sufficient according to you?": ["32GB", "64GB", "128GB", "256GB"],
  "What are your basic needs?": ["Messaging and Calls", "Gaming", "Photography"],
  "How much RAM is sufficient according to your needs?": ["2GB", "4GB", "6GB", "6GB+"]
};

function App() {
  const [showElement, setShowElement] = useState(true);
  useEffect(() => {
    setTimeout(function () {
      setShowElement(false);
    }, 1000);
  }, []);

  const click = event => {
    event.currentTarget.style.display = "block";
  }

  const [showElement2, setShowElement2] = useState(false);

  const handleClick = () => {
    setShowElement2(true);
  };

  return (
    <>
    {/* <div>{brands}</div> */}
    <img class="wave" src={wave} alt="" width="100%" height="100%"></img>
    <img class="wave2" src={wave} alt="" width="100%" height="100%"></img>
    {showElement ? (
      <div> "" </div>
    ) : (
      <div class = "main" id="main" style={{opacity: showElement ? 0 : 1}}>
        <h2 class = "prevent-select">Welcome to <span class="mobihunt">MobiHunt</span></h2>
        {"\n"}
        {showElement2 ? (
          <div class="questionsContainer">
          <div class = "question">
            {Object.keys(test_questions)[0]}
          </div>

        </div>
        ) : (
          <button onClick={handleClick} class="button_">Get Started</button>
        )}
      </div>
    )}
    </>
  )
}

export default App;
