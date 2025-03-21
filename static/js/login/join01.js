// DOM 요소 가져오기
const all_agree = document.getElementById('all_agree');
const slaveCheckboxes = document.querySelectorAll('.slaveCheckbox');

// 마스터 체크박스 클릭 시 나머지 체크박스 상태 변경
all_agree.addEventListener('change', () => {
  const isChecked = all_agree.checked;
  slaveCheckboxes.forEach(checkbox => {
    checkbox.checked = isChecked;
  });
});

// 슬레이브 체크박스 상태에 따라 마스터 체크박스 상태 업데이트
slaveCheckboxes.forEach(checkbox => {
  checkbox.addEventListener('change', () => {
    const allChecked = Array.from(slaveCheckboxes).every(checkbox => checkbox.checked);
    const noneChecked = Array.from(slaveCheckboxes).every(checkbox => !checkbox.checked);

    if (allChecked) {
      all_agree.checked = true;
      all_agree.indeterminate = false; // 중간 상태 해제
    } else if (noneChecked) {
      all_agree.checked = false;
      all_agree.indeterminate = false; // 중간 상태 해제
    } else {
      all_agree.indeterminate = true; // 중간 상태로 표시
    }
    // 필수 항목 체크 여부 확인
    if (!checkboxA.checked || !checkboxB.checked) {
      // 필수 체크박스 중 하나라도 체크되지 않은 경우
      warningMessage.textContent = '필수 항목을 모두 선택해주세요!';
    }
  });
});

document.getElementById('join01button').addEventListener('click', () => {
  const checkboxA = document.getElementById('agree1'); // 필수 A
  const checkboxB = document.getElementById('agree2'); // 필수 B

  // 필수 항목 체크 여부 확인
  if (!checkboxA.checked || !checkboxB.checked) {
    alert('필수항목을 모두 체크해주세요')
    return;
  }
  location.href="/loginpage/join02/"
});
