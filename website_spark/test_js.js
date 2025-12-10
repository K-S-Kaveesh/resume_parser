const emojisList = ["📄","💼","📝","📊","🔍","🚀","📚","📈","📁","🗂️","🧾","📃","🏢","✏️","🧠","💡"];

function random(min, max) {
    return Math.random() * (max - min) + min;
}

for (let i = 0; i < 120; i++) {
    const em = document.createElement("div");
    em.classList.add("emoji");
    em.innerText = emojisList[Math.floor(Math.random() * emojisList.length)];
    em.style.left = random(2, 98) + "%";
    em.style.top = random(2, 95) + "%";
    em.style.fontSize = random(28, 60) + "px";
    em.style.animationDuration = random(6, 16) + "s";
    em.style.animationDelay = random(0, 5) + "s";
    em.style.opacity = random(0.15, 0.35);
    document.body.appendChild(em);
}

/* File name display */
let resume = document.getElementById("resume");
let jd = document.getElementById("jd");

resume.addEventListener("change", () => {
    let box = document.getElementById("resumeName");
    box.textContent = resume.files[0].name;
    box.style.display = "block";
});

jd.addEventListener("change", () => {
    let box = document.getElementById("jdName");
    box.textContent = jd.files[0].name;
    box.style.display = "block";
});

function goNext() {
    if (!resume.files[0] || !jd.files[0]) {
        alert("Please upload both files!");
        return;
    }
    
    // Show loading overlay
    document.getElementById('loadingOverlay').style.display = 'flex';
    document.getElementById('analyzeBtn').disabled = true;
    
    // Create FormData and send to backend
    const formData = new FormData();
    formData.append("resume", resume.files[0]);
    formData.append("job", jd.files[0]);
    
    // Send files to backend for processing using fetch
    fetch("http://127.0.0.1:5000/analyze", {
        method: "POST",
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('HTTP error! status: ' + response.status);
        }
        return response.json();
    })
    .then(data => {
        localStorage.setItem("matchData", JSON.stringify(data));
        window.location.href = "result.html";
    })
    .catch(error => {
        console.error("Error:", error);
        // Store error info and go to results page
        localStorage.setItem("matchData", JSON.stringify({
            score: 0,
            resume_skills: [],
            job_skills: [],
            matching_skills: [],
            missing_skills: [],
            summary: "Error processing files: " + error.message
        }));
        window.location.href = "result.html";
    });
}