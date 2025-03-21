// 아이디찾기 페이지1

// input이 비었을때 에러메세지

const id1submitButton = document.getElementById('id_button');
const inputs = document.querySelectorAll('.id_input');
const id1errorMessage = document.querySelectorAll('.id1_error-message');

// 버튼 클릭 시 입력 필드 확인
id_button.addEventListener('click', () => {
  let isValid = true;

  // 입력 필드 확인
  for (let i = 0; i < inputs.length; i++) {
    if (inputs[i].value.trim() === '') {
      id1errorMessage[i].style.display = 'block'; // 에러 메시지 표시
      if (isValid) {
        inputs[i].focus(); // 첫 번째 비어 있는 필드에 포커스
      }
      isValid = false;
    } else {
      id1errorMessage[i].style.display = 'none'; // 에러 메시지 숨김
    }
  }
});

// 입력 필드에 포커스를 잃었을 때도 확인
inputs.forEach((input, index) => {
  input.addEventListener('blur', () => {
    if (input.value.trim() === '') {
      id1errorMessage[index].style.display = 'block';
    } else {
      id1errorMessage[index].style.display = 'none';
    }
  });
});