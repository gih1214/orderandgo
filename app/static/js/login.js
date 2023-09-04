// 전화번호 입력 시
const changeInputTel = (event) => {
  const _target = event.currentTarget;
  const targetIndex = Number(_target.dataset.index);
  const textLength = _target.value.length;
  const _inputNextTel = document.querySelector(`.tel_box input[data-index="${targetIndex+1}"]`)
  if(targetIndex == 0 && textLength >= 3 || targetIndex == 1 && textLength >= 4){
    _inputNextTel.focus();
  }
}

// 패스워드 눈알 클릭 시
const clickToggleShowPassword = (event) => {
  event.preventDefault();
  const _target = event.currentTarget;
  const _passwordBox = document.querySelector('.password_box')
  const isActive = _passwordBox.classList.contains('active');
  const _inputPassword = document.querySelector('.password_box input');
  if(isActive) {
    _inputPassword.setAttribute('type', 'password')
  }else{
    _inputPassword.setAttribute('type', 'text')
  }
  _passwordBox.classList.toggle('active')
}


