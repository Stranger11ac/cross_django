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
            },
        },
        eventClick: function (info) {
            var eventObj = info.event;
            var $eventDesc = $("#eventDesc");
            var $eventEndDate = $("#eventEndDate");
            var $eventEndTime = $("#eventEndTime");
            var $dateSeparator = $("#dateSeparator");
            var $eventBtnDiv = $("#eventBtnDiv");
            var $eventBtn = $("#eventBtn");
            var $eventImg = $("#eventImg");

            // Actualizar texto de los elementos
            $("#eventModalLabel").text(`TITULO:${eventObj.title}`);
            $("#eventStartDate").text(formatDate(eventObj.start));
            $("#eventStartTime").text(formatTime(eventObj.start));

            // Descripción del evento
            $eventDesc
                .text(eventObj.extendedProps.description || "")
                .toggleClass("none", !eventObj.extendedProps.description);

            // Fecha y hora de finalización del evento
            var hasEnd = !!eventObj.end;
            $eventEndDate.text(hasEnd ? formatDate(eventObj.end) : "");
            $eventEndTime.text(hasEnd ? formatTime(eventObj.end) : "");
            $dateSeparator.toggleClass("none", !hasEnd);

            // Ubicación del evento
            $("#eventLoc").text(eventObj.extendedProps.location || "Campus UTC");

            // Botón de evento
            var hasButton = eventObj.extendedProps.button !== "";
            $eventBtnDiv.toggleClass("none", !hasButton);
            $eventBtn.attr("href", hasButton ? eventObj.extendedProps.button : "");

            // Imagen del evento
            var imgJson = eventObj.extendedProps.imagen;
            $eventImg.toggleClass("none", imgJson === "false");
            if (imgJson !== "false") {
                $eventImg.attr("src", imgJson.replace("cross_asistent/", ""));
            }

            // Mostrar el modal con un retraso
            var myModal = new mdb.Modal(document.getElementById("eventModal"));
            setTimeout(() => {
                myModal.show();
            }, 200);

            info.jsEvent.preventDefault();
        },
    });
    calendar.render();

    $(document).on("click", ".fc-multimonth-month", function () {
        var dataDate = $(this).attr("data-date");
        calendar.changeView("dayGridMonth", dataDate);
    });
});
