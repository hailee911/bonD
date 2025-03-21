// input이 비었을때 에러메세지

const loginsubmitButton = document.getElementById('pw_button');
const logintextInput1 = document.getElementById('pw_id_input');
const loginerrorMessage1 = document.getElementById('pw_errorMessage');

// 버튼 클릭 시 입력 필드 확인
pw_button.addEventListener('click', () => {
  let isValid = true;

  // 첫 번째 입력 필드 확인
  if (pw_id_input.value.trim() === '') {
    pw_errorMessage.style.display = 'block';
    pw_id_input.focus(); // 첫 번째 입력 필드에 포커스 이동
    isValid = false;
  } else {
    pw_errorMessage.style.display = 'none';
  }
  pwFrm.submit()
});

// 입력 필드에 포커스를 잃었을 때도 확인
pw_id_input.addEventListener('blur', () => {
  if (pw_id_input.value.trim() === '') {
    pw_errorMessage.style.display = 'block';
  } else {
    pw_errorMessage.style.display = 'none';
  }
});
