document.addEventListener("DOMContentLoaded", function () {
    function formatDate(date) {
        const options = { year: "2-digit", month: "2-digit", day: "2-digit" };
        return date.toLocaleDateString("es-ES", options);
    }

    function formatTime(date) {
        const options = { hour: "2-digit", minute: "2-digit", hour12: true };
        return date.toLocaleTimeString("es-ES", options);
    }

    var calendarEl = document.getElementById("calendar");
    var dataEvents = calendarEl.getAttribute("data-events");
    var calendar = new FullCalendar.Calendar(calendarEl, {
        footerToolbar: {
            start: "timeGridDay,timeGridWeek,dayGridMonth,multiMonthYear",
            end: "prevYear,nextYear",
        },
        headerToolbar: {
            start: "title",
            end: "today,prev,next",
        },
        events: dataEvents,
        initialView: "dayGridMonth",
        locale: "es",
        height: "auto",
        navLinks: true,
        nowIndicator: true,
        slotLabelFormat: {
            hour: "numeric",
            minute: "2-digit",
            hour12: true,
        },
        eventTimeFormat: {
            hour: "numeric",
            minute: "2-digit",
            hour12: true,
        },
        eventClick: function (info) {
            var eventObj = info.event;

            document.getElementById("eventModalLabel").innerText = eventObj.title;
            document.getElementById("eventDesc").innerText = eventObj.extendedProps.description || "Sin descripción";
            document.getElementById("eventStartDate").innerText = formatDate(eventObj.start);
            document.getElementById("eventStartTime").innerText = formatTime(eventObj.start);

            if (eventObj.end) {
                document.getElementById("eventEndDate").innerText = formatDate(eventObj.end);
                document.getElementById("eventEndTime").innerText = formatTime(eventObj.end);
                document.getElementById("dateSeparator").classList.remove("none");
            } else {
                document.getElementById("eventEndDate").innerText = "";
                document.getElementById("eventEndTime").innerText = "";
                document.getElementById("dateSeparator").classList.add("none");
            }

            document.getElementById("eventLoc").innerText = (eventObj.extendedProps.location || "Campus UTC");

            var myModal = new mdb.Modal(document.getElementById("eventModal"));
            myModal.show();

            info.jsEvent.preventDefault();
        },
    });
    calendar.render();
});
