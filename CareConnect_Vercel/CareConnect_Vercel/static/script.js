async function analyze() {

    const symptoms = document.getElementById("symptoms").value.trim();

    if (!symptoms) {
        alert("Please enter your symptoms.");
        return;
    }

    if (!navigator.geolocation) {
        alert("Your browser doesn't support location.");
        return;
    }

    document.getElementById("loading").style.display = "block";
    document.getElementById("results").classList.add("hidden");

    navigator.geolocation.getCurrentPosition(

        async function (position) {

            window.userLatitude = position.coords.latitude;
            window.userLongitude = position.coords.longitude;

            try {

                const response = await fetch("/analyze", {

                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({

                        symptoms: symptoms,
                        latitude: window.userLatitude,
                        longitude: window.userLongitude

                    })

                });

                if (!response.ok) {

    const error = await response.text();

    alert(error);

    console.log(error);

    document.getElementById("loading").style.display = "none";

    return;
}

const data = await response.json();
window.analysisResult = data;
window.hospitals = data.hospitals;

                document.getElementById("loading").style.display = "none";
                document.getElementById("results").classList.remove("hidden");

                document.getElementById("doctorSection").style.display = "none";
                document.getElementById("hospitalSection").style.display = "none";

                // =========================
                // Doctor Button
                // =========================

                document.getElementById("doctorBtn").onclick = function () {

                    document.getElementById("doctorSection").style.display = "block";

                    document.getElementById("specialist").innerHTML = `
<b>Doctor:</b> ${data.specialist.name}

<b>Reason:</b>
${data.specialist.reason}

<b>Urgency:</b>
${data.specialist.urgency}
`;

                };

                // =========================
                // Hospital Button
                // =========================

                document.getElementById("hospitalBtn").onclick = showRecommendedHospitals;

            }

            catch (error) {

                document.getElementById("loading").style.display = "none";

                console.error(error);

                alert("Unable to analyze symptoms.");

            }

        },

        function () {

            document.getElementById("loading").style.display = "none";

            alert("Please allow location access.");

        }

    );

}



function showRecommendedHospitals() {

    document.getElementById("hospitalSection").style.display = "block";

    const data = window.analysisResult;

    if (!data || !data.hospitals || data.hospitals.length === 0) {

        document.getElementById("hospital").innerHTML =
            "<h3>No hospitals found nearby.</h3>";

        return;
    }

    let html = "";

    // Find the recommended hospital
    const recommended = data.hospitals.find(
        h => h.name === data.recommended_hospital.hospital
    );

    // ==========================
    // AI Recommended Hospital
    // ==========================

    html += `
    <div class="hospital-card" style="border:3px solid gold">

        <h2>⭐ AI Recommended Hospital</h2>

        <h3>${data.recommended_hospital.hospital}</h3>

        <p>${data.recommended_hospital.reason}</p>

        ${
            recommended
                ? `<button onclick="viewHospital(${recommended.id})">
                    View Details
                   </button>`
                : ""
        }

    </div>

    <br>

    <h2>🏥 Other Nearby Hospitals</h2>
    `;

    // ==========================
    // Other Hospitals
    // ==========================

    data.hospitals.forEach(hospital => {

        if (hospital.name === data.recommended_hospital.hospital)
            return;

        html += `
        <div class="hospital-card">

            <h3>${hospital.name}</h3>

            <p><b>Address:</b> ${hospital.address}</p>

            <p><b>Distance:</b> ${hospital.distance}</p>

            <button onclick="viewHospital(${hospital.id})">
                View Details
            </button>

        </div>
        `;

    });

    document.getElementById("hospital").innerHTML = html;
}

function viewHospital(id) {

    console.log("Clicked Hospital ID:", id);
    console.log("Stored Hospitals:", window.hospitals);

    const hospital = window.hospitals.find(
        h => String(h.id) === String(id)
    );

    console.log("Selected Hospital:", hospital);

    if (!hospital) {
        alert("Hospital not found.");
        return;
    }

    document.getElementById("modalName").textContent =
        hospital.name || "Unknown Hospital";

    document.getElementById("modalAddress").textContent =
        hospital.address || "Address Not Available";

    document.getElementById("modalDistance").textContent =
        hospital.distance || "Unknown";

    document.getElementById("modalPhone").textContent =
        hospital.phone || "Not Available";

    if (hospital.website && hospital.website !== "Not Available") {
        document.getElementById("modalWebsite").innerHTML =
            `<a href="${hospital.website}" target="_blank">${hospital.website}</a>`;
    } else {
        document.getElementById("modalWebsite").textContent =
            "Not Available";
    }

    document.getElementById("modalEmergency").textContent =
        hospital.emergency || "Unknown";

    document.getElementById("mapLink").href =
        `https://www.google.com/maps?q=${hospital.latitude},${hospital.longitude}`;

    document.getElementById("hospitalModal").style.display = "block";
}
function closeHospitalModal(){

    document.getElementById("hospitalModal").style.display =
        "none";

}