const API_URL = "http://127.0.0.1:8000/events";

function formatTeam(team) {
    if (!team) return "[missing]";
    return `${team.official_name} (${team.abbreviation}) [${team.country_code}]`;
}

function formatResult(event) {
    if (!event.result) return "-";
    return `${event.result.home_goals} : ${event.result.away_goals}`;
}

async function loadEvents() {
    const response = await fetch(API_URL);
    const events = await response.json();

    events.sort((a, b) => {
        if (a.date === b.date) {
            return a.time.localeCompare(b.time);
        }
        return a.date.localeCompare(b.date);
    });

    const tbody = document.querySelector("#events-table tbody");
    tbody.innerHTML = "";

    events.forEach(event => {
        const row = document.createElement("tr");

        row.className = event.status;

        row.innerHTML = `
            <td>${event.date}</td>
            <td>${event.time}</td>
            <td>${event.status}</td>
            <td>${formatTeam(event.home_team)}</td>
            <td>${formatTeam(event.away_team)}</td>
            <td>${formatResult(event)}</td>
        `;

        tbody.appendChild(row);
    });
}

loadEvents();