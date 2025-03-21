const modal1 = document.getElementById('myModal');  //입력 모달
const openModalBtn = document.getElementById('openModalBtn'); //모달 들어가는 버튼
const closeModalBtn = document.getElementById('closeModalBtn'); //모달 나오는 버튼
const closeModalBtn2 = document.getElementById('closeModalBtn2'); //모달 나오는 버튼
const modal2 = document.getElementById('disModal');
openModalBtn.addEventListener('click', () => {
  modal1.style.display = 'flex'; // 모달을 보이게 설정
});

closeModalBtn.addEventListener('click', () => {
  modal1.style.display = 'none'; // 모달을 숨김
});

// 모달 바깥을 클릭하면 닫히도록 처리
modal1.addEventListener('click', (event) => {
  if (event.target === modal1) {
    modal1.style.display = 'none';
  }
});


// 달력
document.addEventListener('DOMContentLoaded', function () {
  var calendarEl = document.getElementById('calendar');
  var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    headerToolbar: {
      start: 'prev next today',
      center: 'title',
      end: 'dayGridMonth,dayGridWeek,dayGridDay',
    },
    locale: 'ko',
    nowIndicator: true,
    selectable: true,
    editable: true,
    events: '/calendar1/son/',

    // // 이벤트 렌더링 시 색상 적용
    // eventRender: function(info) {
    //   var event = info.event;
    //   var color = event.extendedProps.color;  // 색상 가져오기
    //   info.el.style.backgroundColor = color;  // 배경 색상 변경
    // },

    // 이벤트 클릭 시 처리
    eventClick: function(info) {
      const modal2 = document.getElementById('disModal');
      const event = info.event;
      modal2.style.display = 'flex';  // 모달 보이기

      // 이벤트 ID를 모달에 저장
      document.getElementById("eventNo").dataset.eventId = event.id;
      // 이벤트 데이터 모달 폼에 채우기
      document.getElementById("eventNo").value = event.id; // 고유번호
      document.getElementById("eventTitle1").value = event.title; // 제목
      document.getElementById("eventColor1").value = event.extendedProps.color ;  // 색상
      document.getElementById("startTime1").value = event.start.toISOString().slice(0, 16);  // 시작 시간
      document.getElementById("endTime1").value = event.end ? event.end.toISOString().slice(0, 16) : event.start.toISOString().slice(0, 16);  // 끝 시간
      document.getElementById("eventlocation1").value = event.extendedProps.location ;  // 위치
      document.getElementById("repeat1").value = event.extendedProps.repeat ;  // 반복 여부
      document.getElementById("notes1").value = event.memo ;  // 메모


        // 메모 부분을 빈 값으로 초기화하거나 기존 값으로 설정
      const notesInput = document.getElementById("notes1");
      if (event.extendedProps.memo !== undefined && event.extendedProps.memo !== null) {
        notesInput.value = event.extendedProps.memo;  // 메모 값이 있으면 설정
      } else {
        notesInput.value = '';  // 메모가 없으면 빈 값으로 설정
      }

    },
    

    // 토요일 날짜 글자 색을 파란색으로 변경
    dayCellDidMount: function(info) {
      // 토요일일 경우 글자 색을 파란색으로 설정
      if (info.date.getDay() === 6) {  // 6은 토요일을 나타냄
        info.el.style.color = 'blue';  // 글자 색을 파란색으로 변경
      }
      if(info.date.getDay() === 0){
        info.el.style.color = 'red';
      }

    }



  });
  calendar.render();
});

// 수정 버튼 클릭 시 처리
document.getElementById('updateEventBtn').addEventListener('click', function() {
  const eventId = document.getElementById("eventNo").dataset.eventId;
  const updatedTitle = document.getElementById("eventTitle1").value;
  const updatedColor = document.getElementById("eventColor1").value;  // 색상 정보
  const updatedStartTime = document.getElementById("startTime1").value;
  const updatedEndTime = document.getElementById("endTime1").value;
  const updatedLocation = document.getElementById("eventlocation1").value;
  const updatedRepeat = document.getElementById("repeat1").value;
  const updatedNotes = document.getElementById("notes1").value;

  $.ajax({
    url: '/calendar1/update_event/',  // Django 뷰 URL
    type: 'POST',
    data: {
      'event_id': eventId,
      'title': updatedTitle,
      'color': updatedColor,  // 색상 정보 추가
      'start_date': updatedStartTime,
      'end_date': updatedEndTime,
      'location': updatedLocation,
      'repeat': updatedRepeat,
      'memo': updatedNotes,
      'csrfmiddlewaretoken': document.querySelector('[name=csrfmiddlewaretoken]').value
    },
    success: function(response) {
      modal2.style.display = 'none';
      location.reload();  // 수정 완료 후 페이지 새로고침
      calendar.refetchEvents(); // 달력 갱신
    },
    error: function(xhr, errmsg, err) {
      alert("이벤트 수정 오류: " + errmsg);
    }
  });
});



// 삭제 버튼 클릭 시 처리
document.getElementById('deleteEventBtn').addEventListener('click', function() {
  const eventId = document.getElementById("eventNo").dataset.eventId;

  $.ajax({
    url: '/calendar1/delete_event/',  // Django 뷰 URL
    type: 'POST',
    data: {
      'event_id': eventId,
      'csrfmiddlewaretoken': document.querySelector('[name=csrfmiddlewaretoken]').value
    },
    success: function(response) {
      modal2.style.display = 'none';
      location.reload();  // 수정 완료 후 페이지 새로고침
      calendar.refetchEvents(); // 달력 갱신
    },
    error: function(xhr, errmsg, err) {
      alert("이벤트 삭제 오류: " + errmsg);
    }
  });
});

closeModalBtn2.addEventListener('click', () => {
  modal2.style.display = 'none'; // 모달을 숨김
});

// 모달 바깥을 클릭하면 닫히도록 처리
modal2.addEventListener('click', (event) => {
  if (event.target === modal2) {
    modal2.style.display = 'none';
  }
});
