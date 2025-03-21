// 아이디찾기 페이지1

// input이 비었을 때 에러 메시지
const join3submitButton = document.getElementById('join03button');
const inputs = document.querySelectorAll('.join3_input');
const join31errorMessage = document.querySelectorAll('.join3_error-message');

// 버튼 클릭 시 입력 필드 확인
join3submitButton.addEventListener('click', () => {
  let isValid = true;

  // 입력 필드 확인
  for (let i = 0; i < inputs.length; i++) {
    if (inputs[i].value.trim() === '') {
      join31errorMessage[i].style.display = 'block'; // 에러 메시지 표시
      if (isValid) {
        inputs[i].focus(); // 첫 번째 비어 있는 필드에 포커스
      }
      isValid = false;
    } else {
      join31errorMessage[i].style.display = 'none'; // 에러 메시지 숨김
    }
  }

  // 라디오 버튼 선택 여부 확인
  const radios = document.querySelectorAll('input[name="gender"]');
  const join3_errorMessage3 = document.getElementById('join3_errorMessage3');
  const isChecked = Array.from(radios).some(radio => radio.checked);

  if (!isChecked) {
    join3_errorMessage3.style.display = 'block';
    isValid = false;
  } else {
    join3_errorMessage3.style.display = 'none';
  }

  // 입력 필드나 라디오 버튼에서 오류가 있으면 제출되지 않도록 함
  if (!isValid) {
    return;
  }
  // location.href="/loginpage/join04/"
  join03Frm.submit()
  // 여기에 폼 제출 등 추가 작업을 추가할 수 있습니다.
});

// 입력 필드에 포커스를 잃었을 때도 확인
inputs.forEach((input, index) => {
  input.addEventListener('blur', () => {
    if (input.value.trim() === '') {
      join31errorMessage[index].style.display = 'block';
    } else {
      join31errorMessage[index].style.display = 'none';
    }
  });
});
