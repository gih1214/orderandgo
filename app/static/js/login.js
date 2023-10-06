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

// 매장 로그인 클릭 시
const clickAsStoreLogin = (event) => {
  event.preventDefault();
  const _formEl = document.querySelector('form');
  _formEl.classList.remove('admin');
  _formEl.classList.add('store');
}

// 관리자 로그인 클릭 시
const clickAsAdminLogin = (event) => {
  event.preventDefault();
  const _formEl = document.querySelector('form');
  _formEl.classList.remove('store');
  _formEl.classList.add('admin');

}

// 로그인
const onSubmitLogin = (event) => {
  event.preventDefault();
  const _form = event.target;
  const isAdmin = _form.classList.contains('admin');
  const password = _form.querySelector('#password').value;
  const formData = new FormData();
  formData.append('password', password); 
  if(isAdmin){ // 관리자 로그인
    const _tel = event.target.querySelectorAll('input[type="tel"]');
    const tel = [..._tel].map(data=>data.value).join('')
    formData.append('admin_tel', tel); 
  }else{ // 스토어 로그인
    const isManager = _form.classList.contains('has_manager_section');
    let storeId
    if(isManager) {
      // 셀렉트 박스로 선택한 매장 로그인
      storeId = _form.querySelector('select').value;
    }else{
      storeId = _form.querySelector('#store_id').value;
    }
    console.log(storeId)
    formData.append('store_id', storeId); 

    
    
  }
  
  fetch(`/login`, {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    // 받은 데이터 처리
    if(data.code == 200){
      if(isAdmin){
        const _form = document.querySelector('form');
        _form.className = '';
        _form.classList.add('has_manager_section');
        _form.classList.add('store');
        const jsonData = data.json_data;
        const stores = jsonData['store_list'];
        const _select = document.querySelector('form.has_manager_section.store select');
        _select.innerHTML = stores.map(({store_id, name},index)=> `
          <option value="${store_id}" ${index == 0 ? 'selected' : ''}>${name}</option>
        `).join('')
      }else{
        console.log('스토어 로그인 성공')
        window.location.href = '/'
      }
    }else{
      alert(data.message)
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });
  
}

// 관리자 회원가입 
const onSubmitRegister = (event) => {
  event.preventDefault();
  const _form = event.target
  const _tel = event.target.querySelectorAll('input[type="tel"]');
  const tel = [..._tel].map(data=>data.value).join('')
  const password = _form.querySelector('#password').value;
  const codeNumber = _form.querySelector('#code_number').value;
  console.log(tel, password, codeNumber)
  // 테이블 주문 내역 가져오기

  const formData = new FormData();
  formData.append('tel', tel);
  formData.append('password', password); 
  formData.append('code_number', codeNumber); 
  fetch(`/register_admin`, {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    // 받은 데이터 처리
    console.log(data);
    if(data.code == 200){
      alert('관리자 로그인 후 스토어를 생성해 주세요')
      window.location.href = '/login'
    }else{
      alert(data.message);
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });
}

// 스토어 생성
const onSubmitCreateStore = (event) => {
  event.preventDefault();
  const _form = event.target;
  const name = _form.querySelector('#name').value;
  const password = _form.querySelector('.password_box input').value;
  const store_id = _form.querySelector('#store_id').value;
  const store_image = _form.querySelector('#input_logo_img').files[0];
  
  const formData = new FormData();
  formData.append('store_id', store_id);
  formData.append('name', name);
  formData.append('password', password);
  formData.append('store_image', store_image);

  fetch(`/register_store`, {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    if(data.code == 200) {
      alert('매장을 생성하였습니다. 스토어 로그인을 진행해 주세요')
      window.location.href = '/login'
    }else{
      alert(data.message);
    }
    
  })
  .catch(error => {
    console.error('Error:', error);
  });
}