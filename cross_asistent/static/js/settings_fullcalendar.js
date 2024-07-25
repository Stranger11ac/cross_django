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
        headerToolbar: {
            start: "title",
            end: "today,prev,next",
        },
        footerToolbar: {
            start: "timeGridDay,timeGridWeek,dayGridMonth,multiMonthYear",
            end: "prevYear,nextYear",
        },
        firstDay: 0, // Domingo
        events: dataEvents,
        initialView: "dayGridMonth",
        locale: "es",
        height: "auto",
        navLinks: true,
        nowIndicator: true,
        weekNumbers: true,
        weekText: "",
        slotLabelFormat: {
            hour: "numeric",
            minute: "2-digit",
            hour12: true,
        },
        eventTimeFormat: {
            hour: "numeric",
            hour12: true,
            meridiem: "narrow",
        },
        views: {
            dayGridMonth: {
                displayEventTime: false,
            },
            multiMonthYear: {
                multiMonthMaxColumns: 4,
                multiMonthMinWidth: 250,
                dateClick: function (info) {
                    var clickedDate = new Date(info.dateStr);
                    calendar.changeView("dayGridMonth", clickedDate);
                },
            },
        },
        eventClick: function (info) {
            var eventObj = info.event;

            document.getElementById("eventModalLabel").innerText = eventObj.title;
            document.getElementById("eventStartDate").innerText = formatDate(eventObj.start);
            document.getElementById("eventStartTime").innerText = formatTime(eventObj.start);

            if (eventObj.extendedProps.description) {
                document.getElementById("eventDesc").innerText = eventObj.extendedProps.description;
            } else {
                document.getElementById("eventDesc").classList.add("none");
            }

            if (eventObj.end) {
                document.getElementById("eventEndDate").innerText = formatDate(eventObj.end);
                document.getElementById("eventEndTime").innerText = formatTime(eventObj.end);
                document.getElementById("dateSeparator").classList.remove("none");
            } else {
                document.getElementById("eventEndDate").innerText = "";
                document.getElementById("eventEndTime").innerText = "";
                document.getElementById("dateSeparator").classList.add("none");
            }

            document.getElementById("eventLoc").innerText = eventObj.extendedProps.location || "Campus UTC";

            if (eventObj.extendedProps.button == "false") {
                document.getElementById("eventBtnDiv").classList.add("none");
                document.getElementById("eventBtn").href = "";
            } else {
                document.getElementById("eventBtnDiv").classList.remove("none");
                document.getElementById("eventBtn").href = eventObj.extendedProps.button;
            }

            const imgJson = eventObj.extendedProps.imagen;
            if (imgJson == "false") {
                document.getElementById("eventImg").classList.add("none");
            } else {
                document.getElementById("eventImg").classList.remove("none");
                imgSrc = imgJson.replace("cross_asistent/", "");
                document.getElementById("eventImg").src = imgSrc;
            }

            var myModal = new mdb.Modal(document.getElementById("eventModal"));
            setTimeout(() => {
                myModal.show();
            }, 500);

            info.jsEvent.preventDefault();
        },
    });
    calendar.render();

    $(document).on("click", ".fc-multimonth-month", function () {
        var dataDate = $(this).attr("data-date");
        calendar.changeView("dayGridMonth", dataDate);
    });
});
