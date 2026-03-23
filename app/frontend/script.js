const API_URL = "http://127.0.0.1:8000/events";

let allEvents = [];

function formatTeam(team) {
    if (!team) return "[missing]";
    return `${team.official_name} (${team.abbreviation}) [${team.country_code}]`;
}

function formatResult(event) {
    if (!event.result) return "-";
    return `${event.result.home_goals}:${event.result.away_goals}`;
}

async function loadEvents() {
    const response = await fetch(API_URL);
    allEvents = await response.json();

    if (allEvents.length > 0) {
        const firstEventDate = new Date(allEvents[0].date);
        currentDate = new Date(firstEventDate.getFullYear(), firstEventDate.getMonth(), 1);
    }

    allEvents.sort((a, b) => {
        if (a.date === b.date) {
            return a.time.localeCompare(b.time);
        }
        return a.date.localeCompare(b.date);
    });

    const tbody = document.querySelector("#events-table tbody");
    tbody.innerHTML = "";

    allEvents.forEach(event => {
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

    renderCalendar(); // IMPORTANT: update calendar after loading events
}

function groupEventsByDate(events) {
    const map = {};

    events.forEach(event => {
        if (!map[event.date]) {
            map[event.date] = [];
        }
        map[event.date].push(event);
    });

    return map;
}

let currentDate = new Date();

function getMondayIndex(day) {
    return (day + 6) % 7;
}

function renderCalendar() {
    const calendar = document.getElementById("calendar");
    calendar.innerHTML = "";

    const title = document.getElementById("calendar-title");

    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();

    title.textContent = `${year}-${String(month + 1).padStart(2, "0")}`;

    const firstDay = new Date(year, month, 1);
    const startDay = getMondayIndex(firstDay.getDay());

    const daysInMonth = new Date(year, month + 1, 0).getDate();

    const weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

    const eventsByDate = groupEventsByDate(allEvents);

    // headers
    weekdays.forEach(day => {
        const header = document.createElement("div");
        header.className = "day-header";
        header.textContent = day;
        calendar.appendChild(header);
    });

    // empty cells before first day
    for (let i = 0; i < startDay; i++) {
        const empty = document.createElement("div");
        empty.className = "day other-month";
        calendar.appendChild(empty);
    }

    // days of month
    for (let day = 1; day <= daysInMonth; day++) {
        const cell = document.createElement("div");
        cell.className = "day";

        const dateStr = `${year}-${String(month + 1).padStart(2, "0")}-${String(day).padStart(2, "0")}`;

        let eventsHtml = "";

        if (eventsByDate[dateStr]) {
            const dayEvents = eventsByDate[dateStr]
                .sort((a, b) => a.time.localeCompare(b.time));

            eventsHtml = dayEvents.map(e => {
                const home = e.home_team ? e.home_team.official_name : "[missing]";
                const away = e.away_team ? e.away_team.official_name : "[missing]";
                const result = e.result ? ` ${e.result.home_goals}:${e.result.away_goals}` : "";

                return `<div class="event">
                    ${e.time.slice(0,5)} ${home} vs ${away}${result}
                </div>`;
            }).join("");
        }

        cell.innerHTML = `
            <div><strong>${day}</strong></div>
            ${eventsHtml}
        `;

        calendar.appendChild(cell);
    }
}

function prevMonth() {
    currentDate.setMonth(currentDate.getMonth() - 1);
    renderCalendar();
}

function nextMonth() {
    currentDate.setMonth(currentDate.getMonth() + 1);
    renderCalendar();
}

// initialize
loadEvents();