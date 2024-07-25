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
        // firstDay: 1, // Lunes
        events: dataEvents,
        initialView: "multiMonthYear",
        // initialView: "dayGridMonth",
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
            // timeGridDay: {
            //     // titleFormat: { year: "numeric", month: "long", day: "numeric" },
            // },
            // timeGridWeek: {
            //     // titleFormat: { year: "numeric", month: "long", day: "numeric" },
            // },
            dayGridMonth: {
                displayEventTime: false,
            },
            multiMonthYear: {
                // dayMaxEventRows: 6,
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

            document.getElementById("eventLoc").innerText = eventObj.extendedProps.location || "Campus UTC";

            var myModal = new mdb.Modal(document.getElementById("eventModal"));
            myModal.show();

            info.jsEvent.preventDefault();
        },
    });
    calendar.render();

    $(document).on("click", ".fc-multimonth-month", function () {
        var dataDate = $(this).attr("data-date");
        calendar.changeView("dayGridMonth", dataDate);
    });

    // var monthLabels = document.querySelectorAll(".fc-multimonth-month");
    // monthLabels.forEach(function (monthLabel) {
    //     monthLabel.addEventListener("click", function () {
    //         var dataDate = monthLabel.getAttribute("data-date");
    //         calendar.changeView("dayGridMonth", dataDate);
    //     });
    // });

    // $('[data-date]').click(() => {
    //     // var thisDate = $(this).data("date");
    //     var thisDate = $(this).attr("class");
    //     console.log('date: '+ thisDate);
    // });

    // document.addEventListener("click", function (event) {
    //     if (calendar.view.type === "multiMonthYear") {
    //         var target = event.target;
    //         if (target.classList.contains("fc-multimonth-title")) {
    //             // var monthYearText = target.innerText.split(" ");
    //             // var month = monthYearText[0];
    //             // var year = monthYearText[1];

    //             // // Convertir el nombre del mes al índice del mes
    //             // var monthIndex = new Date(Date.parse(month + " 1, 2024")).getMonth();

    //             // // Cambiar la vista al mes correspondiente
    //             // var clickedDate = new Date(year, monthIndex, 1);
    //             console.table(target);
    //             calendar.changeView("dayGridMonth", "2025-11");
    //         }
    //     }
    // });
});
