// 모든 버튼 및 입력 필드를 가져옵니다.
const passwordFields = document.querySelectorAll('.pw3_id_input');
const toggleButtons = document.querySelectorAll('.toggleButton');
const validateButton = document.getElementById('validateButton');
const pwpw = document.getElementById('pwpw');
const pwpw2 = document.getElementById('pwpw2');
const errorMessage1 = document.getElementById('errorMessage1');
const errorMessage2 = document.getElementById('errorMessage2');

// 비밀번호 필드 타입 토글
toggleButtons.forEach((button, index) => {
  const toggleImage = button.querySelector('img');
  const passwordField = passwordFields[index];

  button.addEventListener('click', () => {
    if (passwordField.type === 'password') {
      passwordField.type = 'text';
      toggleImage.src = eyeOpenImage;
      toggleImage.alt = '비밀번호 숨기기';
    } else {
      passwordField.type = 'password';
      toggleImage.src = eyeClosedImage;
      toggleImage.alt = '비밀번호 보기';
    }
  });
});

// 비밀번호 유효성 검사 함수
function validatePassword(password) {
  const regex = /^(?=.*[a-zA-Z])(?=.*\d)(?=.*[!@#$%^&*()\-_=+{};:'",.<>?]).{8,12}$/;
  return regex.test(password);
}

// 입력 필드 확인 함수
function validateInputs() {
  let isValid = true;

  // 첫 번째 입력 필드 확인
  if (pwpw.value.trim() === '') {
    errorMessage1.style.display = 'block';
    if (isValid) pwpw.focus();
    isValid = false;
  } else {
    errorMessage1.style.display = 'none';
  }

  // 두 번째 입력 필드 확인
  if (pwpw2.value.trim() === '') {
    errorMessage2.style.display = 'block';
    if (isValid) pwpw2.focus();
    isValid = false;
  } else {
    errorMessage2.style.display = 'none';
  }

  return isValid;
}

// 버튼 클릭 이벤트
validateButton.addEventListener('click', () => {
  const password = pwpw.value;

  if (!validateInputs()) {
    // 필드가 비어 있는 경우 경고를 표시하고 종료
    return;
  }

  if (!validatePassword(password)) {
    alert('비밀번호는 8자 이상 12자리 이하, 숫자, 영문자, 특수문자를 포함해야 합니다.');
    return;
  }

  if (pwpw.value !== pwpw2.value) {
    alert('비밀번호가 일치하지 않습니다.');
    return;
  }

  // 모든 조건을 통과한 경우
  pw3Frm.submit()
  alert('비밀번호 변경을 완료했습니다!');
  // 여기서 form을 제출하거나 다른 작업 수행 가능
});

// 입력 필드에 포커스를 잃었을 때 에러 메시지 확인
[pwpw, pwpw2].forEach((field, index) => {
  const errorMessage = index === 0 ? errorMessage1 : errorMessage2;
  field.addEventListener('blur', () => {
    if (field.value.trim() === '') {
      errorMessage.style.display = 'block';
    } else {
      errorMessage.style.display = 'none';
    }
  });
});
