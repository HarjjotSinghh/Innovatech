let fake_space = String.fromCodePoint(0x00002800);
let test_questions = new Object();
test_questions = {  
    "What is your budget?": [">10,000", "10,000-20,000", "20,000-30,000", "30,000-40,000", "40,000-70,000", "70,000+"],
    "What is your screentime?": ["<4hrs", "4-8hrs", "8-12hrs", "12+hrs"],
    "Do you care about how your phone looks?": ["Yes", "No"],
    "How often do use your phone's camera?": [`Not${fake_space}that${fake_space}much`, "Sometimes", "Frequently", `All${fake_space}the${fake_space}time`],
    "What screen size do you prefer?": ["<6inches", "6-6.4inches", "6.4+inches"],
    "How much storage is sufficient for you?": ["32GB", "64GB", "128GB", "256GB", "512GB+"],
    "How much RAM is sufficient according to your needs?": ["2GB", "4GB", "6GB", "8GB+"]
};

let test_questions_index = {
    1: "What is your budget?",
    2: "What is your age group?",
    3: "What is your screentime?",
    4: "Do you care about how your phone looks?",
    5: "How often do use your phone's camera?",
    6: "What screen size do you prefer?",
    7: "How much storage is sufficient for you?",
    8: "What do you typically do on your smartphone on daily basis?",
    9: "How much RAM is sufficient according to your needs?"
};

var selectedOptions = new Object();

(function(window, document) {

    window.onload = init;
    var currentDiv = 1;
    
    function init(){

        const nextQuestionButton = document.getElementById("nextQuestion");
        const firstQuestion = document.getElementById(Object.keys(test_questions)[0].replace(/ /g, '_'));
        const labels = document.querySelectorAll("label");
        var divs = document.getElementsByClassName("questionDivs");
        var options = [];

        Object.values(test_questions).forEach(v => {
            options.push(document.getElementsByName(String.toString(v)));
        });

        // const pushSelectedOption = function() {
        //     options.forEach(option => {
        //         let selectedOption = '';
        //         for (let i = 0; i < option.length; i++) {
        //             if (option[i].checked) {
        //               selectedOption = option[i].value;
        //               selectedOptions.push(selectedOption);
        //               console.log(selectedOptions);
        //               break;
        //             };
        //         };
        //     });
        // }
        

        Object.entries(test_questions).forEach(([k, v]) => {
            const question = document.getElementById(k.replace(/ /g, '_'));
            if (firstQuestion.isEqualNode(question)) {

            }
            else {
                question.style.display = "none";
            };
            
        });

        function labelsChecked() {
            let checked = false;
            labels.forEach(function(myLabel) {
              if (myLabel.querySelector('input:checked')) {
                checked = true;
              }
            });
            return checked;
          }

        let i = 0;

        labels.forEach(function(label) {

            label.addEventListener('change', function() {
              if (labelsChecked()) {
                nextQuestionButton.disabled = false;
              } else {
                nextQuestionButton.disabled = true;
              }
            });
          });

        nextQuestionButton.disabled = true;

        nextQuestionButton.addEventListener("click", function(event) {
                
                var x = 0;
                labels.forEach(function(label) {
                    // console.log(label);
                    // const inputs = (`input[name=${String.toString(Object.values(test_questions)[i]).replace(/ /g, '_')}]`);
                    const input = label.children[0];
                    if (input.checked) {
                        // console.log([Object.keys(test_questions)])
                        // console.log(x);
                        selectedOptions[Object.keys(test_questions)[x]] = input.value;
                        x++;
                        // console.log(selectedOptions);
                    };
                     
                });
                
                if (nextQuestionButton.disabled) {
                    event.preventDefault();
                };

                // pushSelectedOption();

                divs[currentDiv - 1].style.display = "none";
                
                currentDiv++;
                
                if (currentDiv > divs.length) {
                    
                    // const req = new XMLHttpRequest();
                    // req.open("POST", `get_user_data/${JSON.stringify(selectedOptions)}`);
                    // req.send();

                    $.post("/get_user_data", {
                        javascript_data: JSON.stringify(selectedOptions)
                    });
                    // console.log(selectedOptions);
                    window.location = "http://localhost:6969/result";
                    
                };
                
                divs[currentDiv - 1].style.display = "block";

                nextQuestionButton.disabled = true;
          });

    };
  
  })(window, document);

export { selectedOptions };

