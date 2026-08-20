const symptoms = sessionStorage.getItem("symptoms");
const location = sessionStorage.getItem("location");

const steps = [

"step1",
"step2",
"step3",
"step4",
"step5"

];

let current = 0;

function runStep(){

    if(current>0){

        const prev=document.getElementById(steps[current-1]);

        prev.innerHTML="✅ "+prev.innerHTML.replace("⏳ ","");

        prev.style.background="#16a34a";

    }

    if(current<steps.length){

        const now=document.getElementById(steps[current]);

        now.style.background="#2563eb";

        now.style.color="white";

        current++;

        setTimeout(runStep,1500);

    }

}

runStep();

async function callAI(){

    const response=await fetch("/analyze",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({

            symptoms:symptoms,

            location:location

        })

    });

    const result=await response.json();

    sessionStorage.setItem(

        "result",

        JSON.stringify(result)

    );

    setTimeout(()=>{

        window.location.href="/results";

    },1500);

}

callAI();