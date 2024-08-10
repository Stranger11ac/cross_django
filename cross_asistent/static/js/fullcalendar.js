document.addEventListener("DOMContentLoaded", function () {
    function formatDate(date) {
        const options = { year: "2-digit", month: "2-digit", day: "2-digit" };
        return date.toLocaleDateString("es-ES", options);
    }
    function formatTime(date) {
        const options = { hour: "2-digit", minute: "2-digit", hour12: true };
        return date.toLocaleTimeString("es-ES", options);
    }
    function formatDateInput(date) {
        return date.toISOString().slice(0, 10);
    }
    function formatTimeInput(date) {
        return date.toTimeString().slice(0, 5);
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
            timeGridWeek: {
                hiddenDays: [0, 6],
            },
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
            const imgJson = eventObj.extendedProps.imagen;
            var myModal = new mdb.Modal(document.getElementById("eventModal"));
            const valEnd = eventObj.end;
            const valStart = eventObj.start;
            const valTitulo = eventObj.title;
            const valallDay = eventObj.allDay;
            const valclassNames = eventObj.classNames;
            const valBtn = eventObj.extendedProps.button;
            const valPleace = eventObj.extendedProps.location;
            const valDescription = eventObj.extendedProps.description;

            if ($("#eventModal").hasClass("calendar_update")) {
                $(".idUpdate").val(eventObj.id);

                $("#tituloUpdate").addClass("active").val(valTitulo);
                $(".eventTitle").text(valTitulo);

                $("#informacionUpdate").addClass("active").val(valDescription);
                $("#redirigirUpdate").addClass("active").val(valBtn);
                $("#ePleaceUpdate").addClass("active").val(valPleace);
                $("#eStartUpdate")
                    .addClass("active")
                    .val(`${formatDateInput(valStart)}T${formatTimeInput(valStart)}`);
                if (valEnd) {
                    $("#eEndUpdate")
                        .addClass("active")
                        .val(`${formatDateInput(valEnd)}T${formatTimeInput(valEnd)}`);
                } else {
                    $("#eEndUpdate")
                        .addClass("active")
                        .val(`${formatDateInput(valStart)}T${formatTimeInput(valStart)}`);
                }
                if (valallDay) {
                    $("#eAllDayUpdate").attr("checked", true);
                } else {
                    $("#eAllDayUpdate").attr("checked", false);
                }
                $("#eColorUpdate option#eColorSelected").attr("selected", false);
                $(`#eColorUpdate option[value="${valclassNames}"]`).attr("selected", true);
                $("[data-select_addClass]").attr("class", `form-select change_bg ${valclassNames}`);

                if (imgJson == "") {
                    $("[for='imagenUpdate']").html('Subir Imagen <i class="fa-regular fa-images ms-1"></i>');
                } else {
                    $("[for='imagenUpdate']").html('Cambiar Imagen <i class="fa-regular fa-images ms-1"></i>');
                }
            } else {
                $("#eventModalLabel").text(valTitulo);
                $("#eventStartDate").text(formatDate(valStart));
                $("#eventStartTime").text(formatTime(valStart));
                $("#eventLoc").text(valPleace || "Campus UTC");
                if (valDescription) {
                    $("#eventDesc").text(valDescription);
                } else {
                    $("#eventDesc").addClass("none");
                }
                if (valEnd) {
                    $("#eventEndDate").text(formatDate(valEnd));
                    $("#eventEndTime").text(formatTime(valEnd));
                    $("#dateSeparator").removeClass("none");
                } else {
                    $("#eventEndDate").text("");
                    $("#eventEndTime").text("");
                    $("#dateSeparator").addClass("none");
                }
                if (valBtn == "") {
                    $("#eventBtnDiv").addClass("none");
                    $("#eventBtn").attr("href", "");
                } else {
                    $("#eventBtnDiv").removeClass("none");
                    $("#eventBtn").attr("href", valBtn);
                }
            }

            if (imgJson == "") {
                $("#eventImg").addClass("none");

                if ($("#eventModal").hasClass("calendar_update")) {
                    $("#eventImg").removeClass("none");
                }
            } else {
                $("#eventImg").removeClass("none");
                let imgSrc = imgJson.replace("cross_asistent/", "");
                $("#eventImg").attr("src", imgSrc);
            }

            setTimeout(() => {
                myModal.show();
            }, 300);

            info.jsEvent.preventDefault();
        },
    });
    calendar.render();

    $(document).on("click", ".fc-multimonth-month", function () {
        var dataDate = $(this).attr("data-date");
        calendar.changeView("dayGridMonth", dataDate);
    });
});
