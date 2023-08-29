let mainCategoryData;
let subCategoryData;
let allMenuData;
let menuImgData = [];

// 메인카테고리 데이터 가져오기
fetch(`/store/get_main_category`, {
  method: 'GET',
})
.then(response => response.json())
.then(data => {
  // 받은 데이터 처리
  console.log(data);
  mainCategoryData = data;
  createSeleteBox(data, 'clickCategory', '.seletebox_main_category');
})
.catch(error => {
  console.error('Error:', error);
});


// 서브카테고리 데이터 가져오기
fetch(`/store/get_sub_category`, {
  method: 'GET',
})
.then(response => response.json())
.then(data => {
  // 받은 데이터 처리
  console.log(data);
  subCategoryData = data;
  createSeleteBox(data, 'clickCategory', '.seletebox_sub_category');
})
.catch(error => {
  console.error('Error:', error);
});


// 메뉴 데이터 가져오기
fetch(`/store/all_menu_list`, {
  method: 'GET',
})
.then(response => response.json())
.then(data => {
  // 받은 데이터 처리
  console.log(data);
  allMenuData = data;
  createMenuTable(data);
})
.catch(error => {
  console.error('Error:', error);
});

// 메뉴 리스트 테이블 html 만들기
const createMenuTable = (data) => {
  const html = `
    <li>
      <div><input type="checkbox"></div>
      <div>메인카테고리</div>
      <div>서브카테고리</div>
      <div>메뉴명</div>
      <div>옵션</div>
      <div>가격</div>
    </li>
    ${data.map(({ id, main_category, sub_category, name, price, option })=>`
    <li data-id="${id}}">
      <div><input type="checkbox"></div>
      <div>${main_category}</div>
      <div>${sub_category}</div>
      <div>${name}</div>
      <div>${option}</div>
      <div>${price.toLocaleString()}</div>
    </li>`).join('')}
  `
  const _menuTable = document.querySelector('.set_menu_product main article .article_bottom ul');
  _menuTable.innerHTML = html;
}

// 셀렉트 박스 html 만들기
const createSeleteBox = (data, fun, target) => {
  html = `
    <button class="input_box btn-dropdown" data-id="${data[0].id}" data-name="${data[0].name}" onclick="clickDropDownBtn(event)">
      <span>${data[0].name}</span>
      <i class="ph ph-caret-down"></i>
    </button>
    <ul class="dropdown-list">
      ${data.map(({id,name})=>`
      <li onclick="${fun}(event)" data-id="${id}" data-name="${name}">${name}</li>
      `).join('')}
    </ul>
  `
  const _selectBox = document.querySelector(target);
  _selectBox.innerHTML = html;
}

// 그룹 셀렉트 드롭박스 클릭 시
const clickDropDownBtn = (event) => {
  const _dropDownBtn = event.currentTarget;
  const _dropDownList = _dropDownBtn.nextElementSibling;
  _dropDownList.classList.toggle('active');
}

// 메인 카테고리 셀릭트 박스에서 현재 메인 카테고리 변경 클릭 시
const clickCategory = (event) => {
  const _target = event.currentTarget;
  const _dropDwonList = _target.closest('.dropdown-list');
  const _dropDownBox = _target.closest('.dropdown-box');
  const categoryId = _target.dataset.id;
  const categoryName = _target.dataset.name;
  const _dropDownBtn = _dropDownBox.querySelector('.btn-dropdown')
  _dropDownBtn.querySelector('span').innerHTML = categoryName;

  _dropDownBtn.dataset.id = categoryId;
  _dropDownBtn.dataset.name = categoryName;
  _dropDwonList.classList.remove('active');
}

// 메뉴 영역 확장 버튼 클릭 시
const clickResponsiveBtn = (event) => {
  const _main = document.querySelector('main');
  _main.classList.toggle('open_aside')
}

// 이미지 프리뷰 만들기
function previewImage(event) {
  const _input = event.target;
  const _imgBox = event.target.closest('.img_box');
  const _img = _imgBox.querySelector('img');
  const _mainImgBox = document.querySelector('.main_img');
  const _mainImg = _mainImgBox.querySelector('img');
  const imgBoxIndex = Number(_imgBox.dataset.index);
  if (_input.files && _input.files[0]) {
    const reader = new FileReader();
    reader.onload = function (e) {
      _img.setAttribute('src', e.target.result);
      menuImgData[imgBoxIndex-1] = e.target.result;
      _mainImg.setAttribute('src', e.target.result);
    }
    reader.readAsDataURL(_input.files[0]);
    _imgBox.classList.add('active');
    _mainImgBox.classList.add('active');
    _mainImgBox.dataset.index = imgBoxIndex;
  }
}
// 멀티 이미지 프리뷰 만들기 
function multiPreviewImage(event) {
  event.preventDefault();
  if(_mainInput.files.length > 4) {
    alert('메뉴 이미지는 최대 4개까지 설정이 가능합니다.')
    return;
  }
  if(!_mainInput.files) return;
  for (let i = 0; i < _mainInput.files.length && i < 4; i++) {
    const _imgBox = document.querySelector(`.img_box[data-index="${i+1}"]`);
    const _img = _imgBox.querySelector('img');
    const reader = new FileReader();
    reader.onload = function (e) {
      _img.setAttribute('src', e.target.result);
      menuImgData[i] = e.target.result;
      if(i == 0) {
        _mainImg.setAttribute('src',e.target.result)
      }
      _imgBox.classList.add('active');    
    }
    reader.readAsDataURL(_mainInput.files[i]);
  }
  _mainImgBox.classList.add('active');
  _mainImgBox.dataset.index = 1;
  
}

// 이미지 클릭 시
const clickMenuImg = (event) => {
  const _img = event.currentTarget;
  const _imgBox = event.target.closest('.img_box');
  const _mainImgBox = document.querySelector('.main_img');
  const _mainImg = _mainImgBox.querySelector('img');
  const imgBoxIndex = Number(_imgBox.dataset.index);
  _mainImg.setAttribute('src', _img.src);
  _mainImgBox.classList.add('active');
  _mainImgBox.dataset.index = imgBoxIndex;
}

// 이미지 삭제 클릭 시
const clickDeleteImg = (event) => {
  const _mainImgBox = event.target.closest('.main_img');
  const _mainImg = _mainImgBox.querySelector('img');
  const imgBoxIndex = Number(_mainImgBox.dataset.index);
  const _imgBox = document.querySelector(`.img_box[data-index="${imgBoxIndex}"]`);
  const _img = _imgBox.querySelector('img');
  menuImgData[imgBoxIndex-1] = '';
  _img.setAttribute('src', '');
  _mainImg.setAttribute('src', '');
  _imgBox.classList.remove('active');
  _mainImgBox.classList.remove('active');
  _mainImgBox.dataset.index = '';
  const _activeImg = document.querySelectorAll('.img_box.active');
  if(_activeImg.length != 0) {
    _mainImg.setAttribute('src', _activeImg[0].querySelector('img').src); 
    _mainImgBox.dataset.index = _activeImg[0].dataset.index;
    _mainImgBox.classList.add('active');
  }
}