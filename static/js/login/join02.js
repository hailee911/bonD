// 비밀번호 텍스트 -> 비밀번호 변경 (토글)
const passwordFields = document.querySelectorAll('.join2_input[type="password"]');
const toggleButtons = document.querySelectorAll('.toggleButton');

toggleButtons.forEach((button, index) => {
  const toggleImage = button.querySelector('img'); // 버튼 내부의 이미지
  const passwordField = passwordFields[index]; // 해당 버튼에 맞는 입력 필드

  button.addEventListener('click', () => {
    // 현재 필드 타입 확인 및 토글
    if (passwordField.type === 'password') {
      passwordField.type = 'text'; // 텍스트로 변경
      toggleImage.src = eyeOpenImage; // 눈 열림 이미지
      toggleImage.alt = '비밀번호 숨기기';
    } else {
      passwordField.type = 'password'; // 비밀번호로 변경
      toggleImage.src = eyeClosedImage; // 눈 닫힘 이미지
      toggleImage.alt = '비밀번호 보기';
    }
  });
});

// 비밀번호 유효성 검사 함수
function validatePassword(password) {
  const regex = /^(?=.*[a-zA-Z])(?=.*\d)(?=.*[!@#$%^&*()\-_=+{};:'",.<>?]).{8,12}$/;
  return regex.test(password);
}

// 모든 입력 필드와 오류 메시지를 처리하는 함수
const join2submitButton = document.getElementById('join2_button');
const inputs = document.querySelectorAll('.join2_input');
const join21errorMessage = document.querySelectorAll('.join2_error-message');

// 입력 필드 비었을 때 에러 메시지 처리
function checkEmptyFields() {
  let isValid = true;
  inputs.forEach((input, index) => {
    if (input.value.trim() === '') {
      join21errorMessage[index].style.display = 'block'; // 에러 메시지 표시
      if (isValid) input.focus(); // 첫 번째 비어 있는 필드에 포커스
      isValid = false;
    } else {
      join21errorMessage[index].style.display = 'none'; // 에러 메시지 숨김
    }
  });
  return isValid;
}

// 비밀번호 확인 기능
function checkPasswordMatch() {
  const pwpw = document.getElementById('join02_password');
  const pwpw2 = document.getElementById('join02_password2');
  if (pwpw.value !== pwpw2.value) {
    alert('비밀번호가 일치하지 않습니다.');
    return false;
  }
  return true;
}

// 비밀번호 유효성 검사 및 다른 검증
join2submitButton.addEventListener('click', () => {
  const pwpw = document.getElementById('join02_password').value;

  // 1. 빈 필드 체크
  if (!checkEmptyFields()) {
    return; // 빈 필드가 있으면 처리 중지
  }

  // 2. 비밀번호 유효성 검사
  if (!validatePassword(pwpw)) {
    alert('8자 이상 12자리 이하의 숫자, 영문자, 특수문자를 포함해주세요.');
    return;
  }

  // 3. 비밀번호 일치 확인
  if (!checkPasswordMatch()) {
    return;
  }

  
  // 모든 검증을 통과한 경우
  // location.href="/loginpage/join03/"
  join02Frm.submit()
  // 여기서 폼 제출 혹은 추가 작업을 처리합니다.
});

// 입력 필드에 포커스를 잃었을 때 에러 메시지 처리
inputs.forEach((input, index) => {
  input.addEventListener('blur', () => {
    if (input.value.trim() === '') {
      join21errorMessage[index].style.display = 'block';
    } else {
      join21errorMessage[index].style.display = 'none';
    }
  });
});
