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
            var {end: valEnd,start: valStart,title: valTitulo,allDay: valallDay,classNames: valclassNames,} = eventObj;
            var {imagen: imgJson,button: valBtn,location: valPleace,description: valDescription,} = eventObj.extendedProps;
            var myModal = new mdb.Modal(document.getElementById("eventModal"));
            const updateModal = $("#eventModal").hasClass("calendar_update");

            if (updateModal) {
                $(".idUpdate").val(eventObj.id);

                $("#tituloUpdate, #informacionUpdate, #redirigirUpdate, #ePleaceUpdate").each(function () {
                    $(this)
                        .addClass("active")
                        .val(eval(this.id.replace("Update", "")));
                });

                $(".eventTitle").text(valTitulo);

                $("#eStartUpdate")
                    .addClass("active")
                    .val(`${formatDateInput(valStart)}T${formatTimeInput(valStart)}`);
                $("#eEndUpdate")
                    .addClass("active")
                    .val(`${formatDateInput(valEnd || valStart)}T${formatTimeInput(valEnd || valStart)}`);
                $("#eAllDayUpdate").prop("checked", valallDay);

                $("#eColorUpdate option").prop("selected", false);
                $(`#eColorUpdate option[value="${valclassNames}"]`).prop("selected", true);
                $("[data-select_addClass]").attr("class", `form-select change_bg ${valclassNames}`);

                const imgLabel = imgJson === "" ? "Subir Imagen" : "Cambiar Imagen";
                $("[for='imagenUpdate']").html(`${imgLabel} <i class="fa-regular fa-images ms-1"></i>`);
                
            } else {
                $("#eventModalLabel").text(valTitulo);
                $("#eventStartDate").text(formatDate(valStart));
                $("#eventStartTime").text(formatTime(valStart));
                $("#eventLoc").text(valPleace || "Campus UTC");

                if (valDescription) {
                    $("#eventDesc").text(valDescription).removeClass("none");
                } else {
                    $("#eventDesc").addClass("none");
                }

                if (valEnd) {
                    $("#eventEndDate").text(formatDate(valEnd));
                    $("#eventEndTime").text(formatTime(valEnd));
                    $("#dateSeparator").removeClass("none");
                } else {
                    $("#eventEndDate, #eventEndTime").text("");
                    $("#dateSeparator").addClass("none");
                }

                const btnState = valBtn === "" ? "add" : "remove";
                $("#eventBtnDiv").toggleClass("none", btnState === "add");
                $("#eventBtn").attr("href", valBtn || "");
            }

            $("#eventImg").toggleClass("none", imgJson === "" && !updateModal);
            if (imgJson !== "") {
                $("#eventImg").attr("src", imgJson.replace("cross_asistent/", ""));
            }

            setTimeout(myModal.show.bind(myModal), 300);

            info.jsEvent.preventDefault();
        },
    });
    calendar.render();

    $(document).on("click", ".fc-multimonth-month", function () {
        var dataDate = $(this).attr("data-date");
        calendar.changeView("dayGridMonth", dataDate);
    });
});
