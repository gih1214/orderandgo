let mainCategoryData;
let subCategoryData;
let allMenuData;

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
  // createHtml(data);
})
.catch(error => {
  console.error('Error:', error);
});

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
