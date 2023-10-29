let mainCategoryData;
let subCategoryData;
let allMenuData;
let menuImgData = [];

// 메인카테고리 데이터 가져오기
const callMainCategoryList = () => {
  const onSuccess = (data) => {
    console.log(data);
    mainCategoryData = data;
    createSeleteBox({main: data}, 'clickCategory', '.seletebox_main_category', 'main', '메인 카테고리');
  }
  fetchData(`/store/get_main_category`, 'GET', {}, onSuccess)
}
callMainCategoryList();

// 서브카테고리 데이터 가져오기
const callSubCategoryList = (main_category_id=undefined) => {
  const submit_data = main_category_id != undefined ? { main_category_id } : '';
  const onSuccess = (data) => {
    console.log(data);
    subCategoryData = data;
    createSeleteBox({sub:data}, 'clickCategory', '.seletebox_sub_category', 'sub', '서브카테고리');
  }
  fetchData(`/store/get_sub_category`, 'GET', submit_data, onSuccess)
}
callSubCategoryList();

// 메뉴 데이터 가져오기
const callAllMenuList = () => {
  const onSuccess = (data) => {
    console.log(data);
    allMenuData = data;
    createMenuTable(data);
  }
  fetchData(`/store/all_menu_list`, 'GET', {}, onSuccess)
}
callAllMenuList();

// 메뉴 리스트 테이블 html 만들기
const createMenuTable = (data) => {
  const html = `
    <li class="table_header">
      <div><input type="checkbox" onclick="clickAllCheckBox(event)"></div>
      <div>메인카테고리</div>
      <div>서브카테고리</div>
      <div>메뉴명</div>
      <div>옵션</div>
      <div>가격</div>
    </li>
    ${data.map(({ id, main_category_id, main_category_name, sub_category_id, sub_category_name, name, price, option })=>`
    <li data-id="${id}" onclick="clickCallMenuData(event)">
      <div><input type="checkbox"></div>
      <div>${main_category_name}</div>
      <div>${sub_category_name}</div>
      <div>${name}</div>
      <div>${option.length == 0 ? `-` : `${option.map((data)=>data.option_name).join(', ')}`}</div>
      <div>${price.toLocaleString()}</div>
    </li>`).join('')}
  `
  const _menuTable = document.querySelector('.set_menu_product main article .article_bottom ul');
  _menuTable.innerHTML = html;
}

// 셀렉트 박스 html 만들기
const createSeleteBox = (category, fun, target, type, ko_category) => {

  const checkedCategorys = category[type].filter(({checked})=>checked);
  const html = `
    <button 
      class="input_box btn-dropdown" 
      data-id="${checkedCategorys.length == 0 ? `` : `${checkedCategorys[0].id}`}" 
      data-name="${checkedCategorys.length == 0 ? `${ko_category}` : `${checkedCategorys[0].name}`}" 
      onclick="clickDropDownBtn(event)"
      >
        <span>${checkedCategorys.length == 0 ? `${ko_category}` : `${checkedCategorys[0].name}`}</span>
        <i class="ph ph-caret-down"></i>
    </button>
    <ul class="dropdown-list">
    ${category[type].map(({id, name})=>`
      <li onclick="${fun}(event)" data-category="${type}" data-id="${id}" data-name="${name}">${name}</li>
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

// 드롭다운 애니메션 처리
const dropDownAnimation = (event) => {
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

// 메인 카테고리 셀릭트 박스에서 현재 메인 카테고리 변경 클릭 시
const clickCategory = (event) => {
  dropDownAnimation(event);
  const target = event.target;
  if(target.closest(".seletebox_main_category") == undefined) return;
  const category_id = target.dataset.id;
  callSubCategoryList(category_id)
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
  const _mainInput = document.querySelector('#main_menu_img');
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
        const _mainImg = _mainImgBox.querySelector('img');
        _mainImg.setAttribute('src',e.target.result)
      }
      _imgBox.classList.add('active');    
    }
    reader.readAsDataURL(_mainInput.files[i]);
  }
  const _mainImgBox = document.querySelector('.main_img');
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

const setMenuHtmlEmptyData = {
  imgList : [],
  name: '',
  price: '',
  description: '',
  category: {
    main: [],
    sub: [],
  },
  options: []
}
const setMenuHtmlDataList = {
  imgList : [
    '/static/images/user/menu/id/1',
    '/static/images/user/menu/id/2',
    '/static/images/user/menu/id/3',
    '/static/images/user/menu/id/4',
  ],
  name: '탕수육',
  price: 16000,
  description: '',
  category : {
    main: [
      {
        id: 1,
        name: '식사류',
        checked: true
      },
      {
        id: 2,
        name: '주류',
        checked: false
      }
    ],
    sub: [
      {
        id: 1,
        name: '메인',
        checked: true
      },
      {
        id: 2,
        name: '면류',
        checked: false
      },
      {
        id: 3,
        name: '밥류',
        checked: false
      }
    ]
  },
  options: [
    {
      name: '소',
      price: 0,
    },
    {
      name: '중',
      price: 5000,
    },
    {
      name: '대',
      price: 10000,
    }
  ]
}
// 메뉴데이터 수정 html 만들기
const setMenuHtml = ({imgList,name,price,description,category,options}) => {
  const imgCountArray = new Array(4).fill(false);
  const checkedMainCategory = category.main.filter(({checked})=>checked);
  const checkedSubCategory = category.sub.filter(({checked})=>checked);
  const html = `
    <button class="responsive_btn" onclick="clickResponsiveBtn(event)">
      <i class="ph ph-caret-left"></i>
      <i class="ph ph-caret-right"></i>
    </button>
    <div class="top scrollbar_hidden">
      <div class="main_img ${imgList[0] != undefined ? `active` : `` }" data-index="1">
        <label for="main_menu_img"><i class="ph ph-plus"></i></label>
        <input id="main_menu_img" hidden multiple  type="file" onchange="multiPreviewImage(event)">
        <img src="${imgList[0] != undefined ? `${imgList[0]}` : ``}" alt="">
        <button class="delete_btn" onclick="clickDeleteImg(event)">
          <i class="ph ph-trash"></i>
        </button>
      </div>
      <div class="imgs">
      ${imgCountArray.map((data, index)=>`
        <div class="img_box ${imgList[index] != undefined ? `active` : ``}" data-index="${index + 1}">
          <label for="menu_img_${index + 1}"><i class="ph ph-plus"></i></label>
          <input data-title="image" data-type="form" id="menu_img_${index + 1}" hidden type="file" onchange="previewImage(event)">
          <img src="${imgList[index] != undefined ? `${imgList[index]}` : ``}" alt="" onclick="clickMenuImg(event)">
        </div>
      `).join('')}
      </div>
    </div>
    <div class="middle scrollbar_hidden">
      <div class="left">
        <label for="">
          <span>메뉴명</span>
          <input data-title="name" data-required="true" data-type="form" type="text" value="${name}">
        </label>
        <label for="">
          <span>판매가</span>
          <input data-title="price" data-required="true" data-type="form" type="text" value="${price}">
        </label>
        <label for="">
          <span>메뉴 설명</span>
          <textarea data-title="main_description" data-type="form" value="${description}"></textarea>
        </label>
      </div>
      <div class="right">
        <label for="">
          <span>카테고리</span>
          <div class="flex_box">
            <div class="dropdown-box seletebox_menu main_category_box">
              ${createCategoryBoxHtml(category,'main','메인카테고리')}
            </div>
            <div class="dropdown-box seletebox_menu sub_category_box">
              ${createCategoryBoxHtml(category,'sub','서브카테고리')}
            </div>  
          </div>
        </label>
        <label for="" class="set_menu_options">
          <span>옵션</span>
          <div class="menu_options">
            ${options.map(({name, price})=>`
            <div class="flex_box">
              <input data-title="option_name" data-type="form" type="text" value="${name}">
              <input data-title="option_price" data-type="form" type="text" value="${price}">
              <button class="delete_btn" onclick="clickAddOptionBtn(event)">
                <i class="ph ph-trash"></i>
              </button>
            </div>
            `).join("")}
          </div>
          <button class="add_option_btn" onclick="clickAddOptionBtn(event)">
            <i class="ph ph-plus"></i>
            <span>옵션 추가</span>
          </button>
        </label>
      </div>
    </div>
    <div class="bottom">
      <button class="delete">삭제</button>
      <button class="save" onclick="clickSaveMenuData(event)">저장</button>
    </div>
  `
  return html
}

// 메뉴 설정에서 카테고리 html 만들기
const createCategoryBoxHtml = (category,type,ko_category) => {
  const checkedCategorys = category[type].filter(({checked})=>checked);
  const html = `
    <button 
      class="input_box btn-dropdown" 
      data-type="form"
      data-title="${type}_category"
      data-id="${checkedCategorys.length == 0 ? `` : `${checkedCategorys[0].id}`}" 
      data-name="${checkedCategorys.length == 0 ? `${ko_category}` : `${checkedCategorys[0].name}`}" 
      onclick="clickDropDownBtn(event)"
      >
        <span>${checkedCategorys.length == 0 ? `${ko_category}` : `${checkedCategorys[0].name}`}</span>
        <i class="ph ph-caret-down"></i>
    </button>
    <ul class="dropdown-list">
    ${category[type].map(({id, name})=>`
      <li onclick="clickSetMenuCategory(event)" data-category="${type}" data-id="${id}" data-name="${name}">${name}</li>
    `).join('')}
    </ul>
  `
  return html;
}

// 테이블에서 메뉴 클릭 시
const clickCallMenuData = (event) => {
  const target = event.currentTarget;
  const menu_id = Number(findParentTarget(target, 'li').dataset.id);
  // 메뉴 id로 메뉴 데이터 호출 후 html 리로딩
  
  
  const _asideEl = document.querySelector('.set_menu_product main aside');
  const onSuccess = (data) => {
    console.log(data)
    const html = setMenuHtml(data);
    _asideEl.innerHTML = html;
  }
  fetchData(`/store/get_menu`, 'GET', {menu_id}, onSuccess)
}

// 메뉴 추가 버튼 클릭 시
const clickAddMenuBtn = (event) => {
  setMenuHtmlEmptyData.category.main = mainCategoryData
  const html = setMenuHtml(setMenuHtmlEmptyData);
  const _asideEl = document.querySelector('.set_menu_product main aside');
  const _tableHeader = document.querySelector('.table_header');

  clickResponsiveBtn(event) // 메뉴 편집 창 열기
  _asideEl.innerHTML = html;
  const _inputName = document.querySelector('input[data-title="name"]');
  _inputName.focus();

  // // 서버에 빈 메뉴 생성 요청 후 데이터 받기
  // // 받은 데이터로 테이블 생성
  // _tableHeader.insertAdjacentHTML('afterend', `
  //   <li data-id="9" onclick="clickCallMenuData(event)">
  //     <div><input type="checkbox"></div>
  //     <div>식사류</div>
  //     <div>메인</div>
  //     <div>탕수육</div>
  //     <div>소, 중, 대</div>
  //     <div>16,000</div>
  //   </li>
  // `);
  
}

// 메뉴 옵션 추가 버튼 클릭 시
const clickAddOptionBtn = (event) => {
  const _menuOptionsEl = document.querySelector('.set_menu_options .menu_options');
  console.log(_menuOptionsEl)
  const html = createMenuOptionHtml([{name: '', price: ''}]);
  console.log(html)
  _menuOptionsEl.insertAdjacentHTML('afterbegin', html);
}

// 옵션 input html 만들기
const createMenuOptionHtml = (optionsData) => {
  return optionsData.map(({name, price})=> `
    <div class="flex_box">
      <input data-title="option_name" data-type="form" type="text" value="${name}"  placeholder="옵션명">
      <input data-title="option_price" data-type="form" type="text" value="${price}" placeholder="가격">
      <button class="delete_btn" onclick="clickDeleteOptionBtn(event)">
        <i class="ph ph-trash"></i>
      </button>
    </div>
  `).join('')
}

// 메뉴 데이터 설정에서 메뉴 카테고리 선택 시
const clickSetMenuCategory = (event) => {
  dropDownAnimation(event);
  const target = event.currentTarget;
  const categoryType = target.dataset.category;
  if(categoryType == 'main'){
    const submit_data = { 'main_category_id' : Number(target.dataset.id)};
    const onSuccess = (data) => {
      console.log(data);
      const _subCategoryEl = document.querySelector('.sub_category_box');
      _subCategoryEl.innerHTML = createCategoryBoxHtml({'sub': data},'sub','서브카테고리')
    }
    fetchData(`/store/get_sub_category`, 'GET', submit_data, onSuccess)
  }
}

// 옵션 삭제 버튼 클릭 시 
const clickDeleteOptionBtn = (event) => {
  const target = event.currentTarget;
  const optionBox = target.closest(".flex_box");
  optionBox.remove();
}

// 메뉴 데이터 저장 버튼 클릭 시
const clickSaveMenuData = (event) => {
  const elements = document.querySelectorAll('*[data-type="form"]');
  const new_data = {};
  const form_data = [];
  let optionsCount = 0;
  elements.forEach((element) => {
    const title = element.dataset.title;
    let value = element.value;
    if(title == 'image'){
      if (!new_data[title]) {
        new_data[title] = [];
      }
      const _imgBox = findParentTarget(element, '.img_box');
      const _img = _imgBox?.querySelector('img');
      const imgData = _img?.getAttribute('src');
      if(imgData == '') return
      form_data.push({
        key : element.id,
        value : getUriToBlobToFile(imgData)
      })
      new_data[title].push(element.id);
    }
    else if(title == 'main_category' || title == 'sub_category'){
      value = Number(element.dataset.id);
      new_data[title] = value;
    }
    else if(title == 'option_name'){
      if(optionsCount == 0) new_data.options = [];
      new_data.options.push({});
      new_data.options[optionsCount].name = element.value;
    }
    else if(title == 'option_price'){
      new_data.options[optionsCount].price = element.value;
      optionsCount += 1;
    }
    else{
      new_data[title] = value;
    }
  })
  const data = {
    json_data : new_data,
    form_data : form_data
  }
  console.log(data);
  fetchData(`/store/set_menu`, 'POST', data, (data)=>{
    console.log(data)
    if(data.code == 200){
      
    }
  },true)
}

// 체크박스 전체 토글
const clickAllCheckBox = (event) => {
  const isChecked = event.target.checked;
  const _checkBoxs = document.querySelectorAll('.set_menu_product main article .article_bottom ul li div:first-child input' );
  _checkBoxs.forEach((_checkBox) => _checkBox.checked = isChecked)
}

// 전체 선택 버튼 클릭 시
const clickAllSeleteBtn = (e) => {
  const _checkBoxs = document.querySelectorAll('.set_menu_product main article .article_bottom ul li div:first-child input' );
  _checkBoxs.forEach((_checkBox) => _checkBox.checked = true)
}

// 전체 취소 버튼 클릭 시
const clickAllCnacelSeleteBtn = (e) => {
  const _checkBoxs = document.querySelectorAll('.set_menu_product main article .article_bottom ul li div:first-child input' );
  _checkBoxs.forEach((_checkBox) => _checkBox.checked = false)
}

// 메뉴 삭제 버튼 클릭 시
const clickDeleteMenu = (e) => {
  const _checkBoxs = document.querySelectorAll('.set_menu_product main article .article_bottom ul li:not(.table_header) div:first-child input:checked');
  
  const menuList = [..._checkBoxs].map((checkBox) => findParentTarget(checkBox, 'li'));
  const menuIdList = menuList.map((menu) => Number(menu.dataset.id));

  // 삭제 api 연결,
  menuList.forEach((menu)=>{menu.remove()});


}