const lastPath = window.location.href.split('/').pop();

let menuData;
fetch(`/pos/get_menu_list/${lastPath}`, {
  method: 'GET',
})
.then(response => response.json())
.then(data => {
  // 받은 데이터 처리
  console.log(data);
  menuData = data;
  createHtml(data);
})
.catch(error => {
  console.error('Error:', error);
});

const createHtml = (menuPageData) => {
  const _menuCatgory = document.querySelector('main section nav ul');
  const _menu = document.querySelector('main section article .items');
  let nav_html = '';
  menuPageData.forEach((data, index)=>{
    nav_html += `
      <li data-id="${data.categoryId}" data-state="${index == 0 ? 'active': ''}">
        <button onclick="changeMenuCategory(event, ${index})">${data.category}</button>
      </li>
    `
    _menuCatgory.innerHTML =  nav_html;
    if(index != 0) return;

    const menus = data.menuList;
    const menus_html = changeMenuHtml(menus);
    _menu.innerHTML = menus_html;
  })
}

// 메뉴 카테고리 변경
const changeMenuCategory = (event, index) => {
  const prevBtn = document.querySelector('main section nav ul li[data-state="active"]');
  prevBtn.dataset.state = '';

  const _li = event.target.closest('li');
  const _menu = document.querySelector('main section article .items');

  _li.dataset.state = 'active'
  const menus_html = changeMenuHtml(menuData[index].menuList);
  _menu.innerHTML = menus_html;
}

// 메뉴 html 변경
const changeMenuHtml = (menus) => {
  let html = '';
  menus.forEach((menu, index)=>{
    html += `
      <button class="menu item" data-id="${menu.menuId}" onclick="clickMenu(event)">
        <div class="title">
          <h2 class="ellipsis">${menu.menu}</h2>
        </div>
        <span class="price">${menu.price}원</span>
      </button>
    `
  })
  return html;
}

// 메뉴 클릭 시
const clickMenu = (event) => {
  const categoryId = document.querySelector('main section nav ul li[data-state="active"]').dataset.id;
  const menuId = event.currentTarget.dataset.id;
  const menu = getMenuData(menuData, categoryId, menuId);
  const _optionHtml = document.querySelector('#container.order main section aside');
  const __menu = document.querySelectorAll('main section article .item');

  resetMenuBackground(__menu);

  let hasMenu = false;

  basket.forEach((data)=>{
    if(data.id == menu.menuId){
      data.count += 1;
      data.price += data.price;
      hasMenu = true;
    }
  })

  if(!hasMenu){
    let newMenu = {
      id: menu.menuId,
      name: menu.menu,
      price: menu.price,
      options: [],
      count: 1
    }
    basket.push(newMenu)
  }
  
  if(menu.optionList.length != 0){
    showMenuOptionHtml(menu.optionList)
    _optionHtml.classList.add('active');
    setMenuDisabled(__menu, event.currentTarget)
  }else {
    _optionHtml.classList.remove('active');

  }
  console.log(basket)
  changeBasketHtml(basket)
}

// 카테고리id, 메뉴id 로 메뉴 찾기
const getMenuData = (data, categoryId, menuId) => {
  const category = data.find(item => item.categoryId == categoryId)?.menuList;
  return category?.find(item => item.menuId == menuId) || null;
};

// 카테고리id, 메뉴id, 옵션id 로 옵션 찾기
const getMenuOptionData = (data, categoryId, menuId, optionId) => {
  const category = data.find(item => item.categoryId == categoryId)?.menuList;
  const menu = category?.find(item => item.menuId == menuId);
  const option = menu?.optionList.find(option => option.optionId == optionId);
  return option || null;
};



const showMenuOptionHtml = (optionDatas,) => {
  const _optionHtml = document.querySelector('main section aside .items');
  let html = ``;
  optionDatas.forEach((optionData)=>{
    html += `
    <button data-id="${optionData.optionId}" class="menu item" onclick="clickMenuOption(event)" >
      <div class="title">
        <h2>${optionData.option}</h2>
      </div>
      <span class="price">${optionData.price}원</span>
    </button>
    `
  })
  _optionHtml.innerHTML = html;
}

// 메뉴 백그라운드 활성화
const setMenuDisabled = (__menu, target) => {
  __menu.forEach((_menu, index)=>{
    _menu.classList.add('disabled');
  })
  target.classList.remove('disabled');
  target.classList.add('active');
}

// 메뉴 백그라운드 제거
const resetMenuBackground = (__menu) => {
  __menu.forEach((_menu, index)=>{
    _menu.classList.remove('disabled');
    _menu.classList.remove('active');
  })
}

// 메뉴 옵션 클릭 시
const clickMenuOption = (event) => {
  const categoryId = document.querySelector('main section nav ul li[data-state="active"]').dataset.id;
  const menuId = document.querySelector('main section article .item.active').dataset.id;
  const optionId = event.currentTarget.dataset.id;
  const option = getMenuOptionData(menuData, categoryId, menuId, optionId);
  basket.forEach((data)=>{
    if(data.id == menuId){
      let hasMenu = false;
      data.options.forEach((optionData)=>{
        if(optionData.id == option.optionId){
          optionData.count += 1;
          optionData.price += optionData.price;
          hasMenu = true;
        } 
      })
      if(!hasMenu) {
        const newOption = {
          id: option.optionId,
          name: option.option,
          price: option.price,
          count: 1
        };
        data.options.push(newOption)
      }
    }
  })
  changeBasketHtml(basket)
}

let basket = new Array;


const changeBasketHtml = (datas) => {
  const _basket = document.querySelector('main aside .basket');
  const _totalPrice = document.querySelector('main aside .total_price .price');
  html = ``;
  let totalPrice = 0;
  datas.forEach((data)=>{
    totalPrice += data.price
    html += `
      <li>
        <div class="menu" onclick="clickBasketMenu(event)">
          <h2>${data.name}</h2>
          <span>${data.count}</span>
          <span class="price">${data.price}원</span>
        </div>
        `
        data.options.forEach((option)=>{
          totalPrice += option.price
          html +=`
          <div class="menu_option" onclick="clickBasketMenu(event)">
            <h2>${option.name}</h2>
            <span>${option.count}</span>
            <span class="price">${option.price}원</span>
          </div>
          `

        })
      html +=
        `
      </li>
    `
  })
  _basket.innerHTML = html

  _totalPrice.innerHTML = totalPrice;
}

const clickBasketMenu = (event) => {
  const __basketMenu = document.querySelectorAll('.basket_container .basket li > div');
  const target = event.currentTarget;
  __basketMenu.forEach((_basketMenu)=>{
    _basketMenu.classList.remove('active');
  })
  target.classList.add('active');
}

const minusBasketMenu = () => {

}
const plusBasketMenu = () => {

}
const deleteBasketMenu = () => {

}