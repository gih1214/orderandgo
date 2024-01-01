let curCategoryIndex = 0;
let curPage = 0;
let menuData;
let state = {
  has_click_item : false,
  click_item : null,
}
// 메뉴판 메뉴 리스트 가져오기
fetch(`/pos/get_menu_list/${lastPath}`, {
  method: 'GET',
})
.then(response => response.json())
.then(data => {
  // 받은 데이터 처리
  console.log(data);
  menuData = data;
  createMenuHtml(data, curCategoryIndex, curPage);
})
.catch(error => {
  console.error('Error:', error);
});

const createMenuHtml = (data, categoryNum, pageNum) => {
  const _menuCatgory = document.querySelector('main section nav ul');
  const _menu = document.querySelector('main section article .items');
  let nav_html = '';
  data.forEach(({categoryId, category, pageList}, index)=>{
    
    nav_html += `
      <li data-id="${categoryId}" data-state="${index == categoryNum ? 'active': ''}">
        <button onclick="changeMenuCategory(event, ${index})">${category}</button>
      </li>
    `
    _menuCatgory.innerHTML = nav_html;
    if(index != categoryNum) return;
    const menus = pageList[pageNum].menuList;
    const menus_html = changeMenuHtml(menus, categoryNum, pageNum);
    _menu.innerHTML = menus_html;
    _menu.setAttribute('data-page', pageNum);
    const _article = document.querySelector('main section article');
    const pageLen = menuData[categoryNum].pageList.length;

    if(0 < pageNum){
      _article.classList.add('hasPrevPage');
    }
    if(pageNum < pageLen){
      _article.classList.add('hasNextPage');
    }
  })
}

// 메뉴 html 변경
const changeMenuHtml = (menus, categoryNum, pageNum) => {
  menus.sort((a,b)=> a.position-b.position);
  const forArray = Array.from({ length: 24 }, () => false);
  menus.forEach((menu)=>forArray[menu.position-1] = menu);
  return forArray.map((menu,index)=> `
    ${menu == false ? `
      <button class="menu item hidden" data-active="false" data-page="${pageNum}" data-position="${index+1}" onclick="clickMenu(event)"></button>` 
      : `
      <button class="menu item" 
        data-active="${state.has_click_item && menu.menuId == Number(state.click_item.id) ? `true` : `false`}" 
        data-id="${menu.menuId}" 
        data-name="${menu.menu}" 
        data-price="${menu.price}" 
        data-page="${pageNum}" 
        data-position="${index+1}" 
        onclick="clickMenu(event)"
      >
        <div class="title">
          <h2 class="ellipsis">${menu.menu}</h2>
        </div>
        <span class="price">${menu.price.toLocaleString()}원</span>
        <div class="active"><i class="ph ph-arrows-out-cardinal"></i></div>
      </button>
    ` }
  `).join('');
}

// 메뉴 영역 클릭 시
const clickMenu = (event) => {
  const _target = event.currentTarget;
  const isHidden = _target.classList.contains('hidden');
  if(isHidden && !state.has_click_item) { // 빈 영역만 클릭 
    return
  }
  const name = _target.dataset.name;
  const price = Number(_target.dataset.price);
  const page = Number(_target.dataset.page);
  const position = Number(_target.dataset.position);
  if(!isHidden && !state.has_click_item){ // 유효 메뉴 클릭, active가 없음  
    _target.dataset.active = !JSON.parse(_target.dataset.active);
    state.has_click_item = true;
    state.click_item = {
      id: Number(_target.dataset.id),
      page: page,
      position: position,
      name: name,
      price: price,
      el: _target
    }
    return 
  }
  if(state.has_click_item) { // 유효 메뉴 클릭, active가 있음
    if(_target.dataset.id == state.click_item.id){ // 동일 메뉴 클릭 시
      state.has_click_item = false;
      state.click_item = null;
      _target.dataset.active = false;
      return;
    }
    // 위치 변경 api
    if(isHidden){ // 단일 위치 변경
      _target.dataset.id = state.click_item.id;
      _target.dataset.name = state.click_item.name;
      _target.dataset.price = state.click_item.price;
      
      _target.classList.remove('hidden');
      _target.innerHTML = `
        <div class="title">
          <h2 class="ellipsis">${state.click_item.name}</h2>
        </div>
        <span class="price">${state.click_item.price.toLocaleString()}원</span>
        <div class="active"><i class="ph ph-arrows-out-cardinal"></i></div>
      `
      state.click_item.el.classList.add('hidden');
      state.click_item.el.dataset.id='';
      state.click_item.el.dataset.name='';
      state.click_item.el.dataset.price='';
      state.click_item.el.dataset.active=false;
      state.click_item.el.innerHTML = ``;
      state.has_click_item=false;
      state.click_item=null;

    }else{ // 멀티 위치 변경
      console.log(state.click_item.el, _target)
      // 이전 클릭 요소 변경
      const _activeTarget = document.querySelector(`button.menu.item[data-id="${state.click_item.id}"]`)
      _activeTarget.dataset.id=_target.dataset.id;
      _activeTarget.dataset.name=_target.dataset.name;
      _activeTarget.dataset.price=_target.dataset.price;
      _activeTarget.dataset.active=false;
      _activeTarget.innerHTML = `
        <div class="title">
          <h2 class="ellipsis">${_target.dataset.name}</h2>
        </div>
        <span class="price">${_target.dataset.price.toLocaleString()}원</span>
        <div class="active"><i class="ph ph-arrows-out-cardinal"></i></div>
      `;
      // 최근 클릭 요소 변경
      _target.dataset.id = state.click_item.id;
      _target.dataset.name = state.click_item.name;
      _target.dataset.price = state.click_item.price;
      _target.dataset.active = false;
      _target.innerHTML = `
        <div class="title">
          <h2 class="ellipsis">${state.click_item.name}</h2>
        </div>
        <span class="price">${state.click_item.price.toLocaleString()}원</span>
        <div class="active"><i class="ph ph-arrows-out-cardinal"></i></div>
      `
      state.has_click_item=false;
      state.click_item=null;
    }
    return 
  }
  
}

// 페이지 변경
const clickChangeMenuPositionPage = (event, type) => {
  if(type == 'prev'){ // 이전 페이지
    curPage -= 1;
  }
  if(type == 'next') { // 다음 페이지
    curPage += 1;
  }
  createMenuHtml(menuData, curCategoryIndex, curPage);
}

// 카테고리 설정 클릭 시
const clickSetCategory = (event) => {
  // openModalFun(event);
  // const _modal = document.querySelector('.modal');
  // const _modalTitle = document.querySelector('.modal-content h1');
  // const _modalBody = document.querySelector('.modal-content .modal-body');
  // _modalTitle.innerHTML = '카테고리 설정'
  // const html = ``

  const modal = openDefaultModal();
  modal.top.innerHTML = modalTopHtml('카테고리 설정');
  modal.middle.innerHTML = ``;
  const btns = [
    {class: 'close',text: '취소', fun: ''},
    {class: 'close',text: '저장', fun: ''}
  ]
  modal.bottom.innerHTML = modalBottomHtml(btns);

}