let menuData;
let cachingData = null;
let basket = new Array;
let currentMenu = null;
let menuAllData = [];
let order_history = [];
// 메뉴판 메뉴 리스트 가져오기
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

// 테이블 주문 내역 가져오기
fetch(`/pos/get_table_order_list/${lastPath}`, {
  method: 'GET',
})
.then(response => response.json())
.then(data => {
  // 받은 데이터 처리
  console.log(data)
  order_history=data.map((order)=>({
    id: order.id,
    masterName : setMasterName(order),
    name: order.name,
    price: order.price,
    count: 1,
    options: order.options,
  }))
})
.catch(error => {
  console.error('Error:', error);
});

// 이전 주문 버튼 클릭 시
const clickOrderHistoryBtn = (event) => {
  const _orderHistoryBtn = event.currentTarget;
  _orderHistoryBtn.dataset.check = true;
  changeBasketHtml(setBasketData(order_history))
}
// 장바구니 버튼 클릭 시
const clickBasketBtn = (event) => {
  changeBasketHtml(setBasketData(menuAllData))
  const _orderHistoryBtn = document.querySelector('.basket_container > .count_btns button.order_history')
  _orderHistoryBtn.dataset.check = false;
}

const createHtml = (menuPageData) => {
  const _menuCatgory = document.querySelector('main section nav ul');
  const _menu = document.querySelector('main section article .items');
  let nav_html = '';
  menuPageData.forEach(({categoryId, category, pageList}, index)=>{
    
    nav_html += `
      <li data-id="${categoryId}" data-state="${index == 0 ? 'active': ''}">
        <button onclick="changeMenuCategory(event, ${index})">${category}</button>
      </li>
    `
    _menuCatgory.innerHTML =  nav_html;
    if(index != 0) return;
    const PAGE_INDEX = 0;
    const menus = pageList[PAGE_INDEX].menuList;
    const menus_html = changeMenuHtml(menus);
    _menu.innerHTML = menus_html;
    _menu.setAttribute('data-page', PAGE_INDEX);
    createPageNationBtnHtml();
    const _article = document.querySelector('main section article');
    const curCategoryId = document.querySelector('main section nav ul li[data-state="active"]').dataset.id;
    const pageLen = menuData.find((category)=>category.categoryId == Number(curCategoryId)).pageList.length;
    if(0 < PAGE_INDEX){_article.classList.add('hasPrevPage')};
    if(PAGE_INDEX < pageLen-1){_article.classList.add('hasNextPage')};
  })
}

// 메뉴 카테고리 변경
const changeMenuCategory = (event, index) => {
  const prevBtn = document.querySelector('main section nav ul li[data-state="active"]');
  prevBtn.dataset.state = '';

  const _li = event.target.closest('li');
  const _menu = document.querySelector('main section article .items');

  _li.dataset.state = 'active'
  const PAGE_INDEX = 0;
  let menus_html
  if(cachingData != null) {
    menus_html = changeMenuHtml(cachingData[index].pageList[PAGE_INDEX].menuList);
  }else {
    menus_html = changeMenuHtml(menuData[index].pageList[PAGE_INDEX].menuList);  
  }
  _menu.innerHTML = menus_html;
  _menu.setAttribute('data-page', PAGE_INDEX);

  const _article = document.querySelector('main section article');
  _article.classList.remove('hasNextPage');
  _article.classList.remove('hasPrevPage');


  const curCategoryId = document.querySelector('main section nav ul li[data-state="active"]').dataset.id;
  const pageLen = menuData.find((category)=>category.categoryId == Number(curCategoryId)).pageList.length;
  if(PAGE_INDEX < pageLen-1){_article.classList.add('hasNextPage')};
}

// 메뉴 html 변경
const changeMenuHtml = (menus) => {
  console.log(menus)
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

// 메뉴 올 데이터를 이용해서 장바구니 데이터로 만들기
const setBasketData = (menus) => {
  const transformedData = [];
  const tempData = {};

  menus.forEach(item => {
    const { masterName, id, name, count, price, options } = item;
    if (tempData[masterName]) {
      tempData[masterName].length++;
    } else {
      tempData[masterName] = {
        masterName,
        length: 1,
        data: {
          id,
          name,
          count,
          price,
          options
        }
      };
    }
  });

  for (const key in tempData) {
    transformedData.push(tempData[key]);
  }

  return transformedData;
}

// 메뉴 클릭 시
const clickMenu = (event) => {
  const categoryId = document.querySelector('main section nav ul li[data-state="active"]').dataset.id;
  const page = document.querySelector('main section article .items').dataset.page;
  const menuId = event.currentTarget.dataset.id;
  const menu = getMenuData(menuData, categoryId, page, menuId);
  const _optionHtml = document.querySelector('#container.order main section aside');
  const __menu = document.querySelectorAll('main section article .item');

  resetMenuBackground(__menu);

  let hasMenu = false;

  currentMenu = {
    id: menu.menuId,
    name: menu.menu,
    price: menu.price,
    count: 1,
    options: [],
  }
  currentMenu.masterName = setMasterName(currentMenu);

  menuAllData.push(currentMenu);
  console.log('menuAllData,',menuAllData)
  changeBasketHtml(setBasketData(menuAllData))
  // 메뉴 옵션 HTML 토글
  if(menu.optionList.length != 0){
    showMenuOptionHtml(menu.optionList)
    _optionHtml.classList.add('active');
    setMenuDisabled(__menu, event.currentTarget)
  }else {
    _optionHtml.classList.remove('active');
  }

  // basket.forEach((data)=>{
  //   if(data.id == menu.menuId){
  //     data.count += 1;
  //     data.price += data.price;
  //     hasMenu = true;
  //   }
  // })

  // if(!hasMenu){
  //   let newMenu = {
  //     id: menu.menuId,
  //     name: menu.menu,
  //     price: menu.price,
  //     options: [],
  //     count: 1
  //   }
  //   basket.push(newMenu)
  // }
  
  // if(menu.optionList.length != 0){
  //   showMenuOptionHtml(menu.optionList)
  //   _optionHtml.classList.add('active');
  //   setMenuDisabled(__menu, event.currentTarget)
  // }else {
  //   _optionHtml.classList.remove('active');

  // }
  // changeBasketHtml(basket)
  // const menuIndex = basket.findIndex(menu => menu.id == menuId);
  // maintainActive(menuIndex, undefined);
}



// 카테고리id, 메뉴id 로 메뉴 찾기
const getMenuData = (data, categoryId, page, menuId) => {
  const category = data.find(item => Number(item.categoryId) == Number(categoryId)).pageList[page]?.menuList;
  return category?.find(item => Number(item.menuId) == Number(menuId)) || null;
};

// 카테고리id, 메뉴id, 옵션id 로 옵션 찾기
const getMenuOptionData = (data, categoryId, page, menuId, optionId) => {
  const category = data.find(item => item.categoryId == categoryId).pageList[page]?.menuList;
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

// 메뉴 마스터 네임 만들기
const setMasterName = (menu) => {
  let masterName = '';
  masterName = `${menu.id}_${menu.count}`;
  menu?.options.sort((a, b)=>{return b - a});
  menu?.options.forEach((option)=>{
    masterName += `_${option.id}_${option.count}`
  })
  return masterName
}

// 메뉴 옵션 클릭 시
const clickMenuOption = (event) => {
  const categoryId = document.querySelector('main section nav ul li[data-state="active"]').dataset.id;
  const page = document.querySelector('main section article .items').dataset.page;
  const menuId = document.querySelector('main section article .item.active').dataset.id;
  const optionId = event.currentTarget.dataset.id;
  const option = getMenuOptionData(menuData, categoryId, page, menuId, optionId);
  let optionIndex = undefined;
  const newOption = {
    id: option.optionId,
    name: option.option,
    price: option.price,
    count: 1,
  }
  let isHas = false;
  currentMenu = menuAllData[menuAllData.length-1]
  currentMenu.options.forEach((option)=>{
    if(option.id == newOption.id){
      console.log('이미 있는 옵션입니다.')
      option.count = option.count + 1; 
      isHas = true;
    }
  })
  if(!isHas || currentMenu.length == 0){
    currentMenu.options.push(newOption)
  }
  currentMenu.masterName = setMasterName(currentMenu);
  console.log('menuAllData,',menuAllData)
  changeBasketHtml(setBasketData(menuAllData))
  // basket.forEach((data)=>{
  //   if(data.id == menuId){
  //     let hasMenu = false;
  //     data.options.forEach((optionData, index)=>{
  //       if(optionData.id == option.optionId){
  //         optionData.count += 1;
  //         optionData.price += optionData.price;
  //         hasMenu = true;
  //         optionIndex = index;
  //       } 
  //     })
  //     const isOptionIndex = currentMenu.options.indexOf(option.optionId);
  //     if (isOptionIndex !== -1) {
  //       console.log('이미 안에 있음');
  //       currentMenu.options.splice(isOptionIndex, 1);
  //     }else {
  //       currentMenu.options.push(option.optionId);
  //       currentMenu.options.sort(function(a, b) { return a - b });
        
  //     }
  //     console.log('currentMenu, ',currentMenu)
  //     console.log('basket,',basket)
      
  //     if(!hasMenu) {
  //       const newOption = {
  //         id: option.optionId,
  //         name: option.option,
  //         price: option.price,
  //         count: 1
  //       };
  //       data.options.push(newOption)
  //       optionIndex = (data.options.length -1)
  //     }
  //   }
  // })
  // changeBasketHtml(basket)
  // const menuIndex = basket.findIndex(menu => menu.id == menuId);
  // maintainActive(menuIndex, optionIndex);
}



// 장바구니 html 변경
const changeBasketHtml = (datas) => {
  console.log(datas)
  const _basket = document.querySelector('main aside .basket');
  const _totalPrice = document.querySelector('main aside .total_price .price');
  html = ``;
  let totalPrice = 0;
  datas.forEach(({data, length})=>{
    totalPrice += data.price
    html += `
      <li>
        <div data-id="${data.id}" data-type="menu" class="menu" onclick="clickBasketMenu(event)">
          <h2>${data.name}</h2>
          <span>${data.count * length}</span>
          <span class="price">${data.price}원</span>
        </div>
        `
        data?.options?.forEach((option)=>{
          totalPrice += option.price
          html +=`
          <div data-id="${option.id}" data-type="menu_option" class="menu_option" onclick="clickBasketMenu(event)">
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

// 장바구니 아이템 클릭 시
const clickBasketMenu = (event) => {
  const __basketMenu = document.querySelectorAll('.basket_container .basket li > div');
  const target = event.currentTarget;
  __basketMenu.forEach((_basketMenu)=>{
    _basketMenu.classList.remove('active');
  })
  target.classList.add('active');
}

// 장바구니 - 클릭 시
const minusBasketMenu = () => {
  if(basket.length == 0) return;
  const target = document.querySelector('.basket .active');
  const targetType = target.dataset.type;
  const pargetEl = target.closest('li').querySelector('[data-type="menu"]')
  const menuId = targetType == "menu" ? target.dataset.id : pargetEl.dataset.id;
  const optionId = targetType == "menu_option" ? target.dataset.id : "";
  let optionIndex = undefined;

  const menuIndex = basket.findIndex(menu => menu.id == menuId);
  if (menuIndex != -1) {
    const menu = basket[menuIndex];
    
    if (optionId) {
      optionIndex = menu.options.findIndex(option => option.id == optionId);
      
      if (optionIndex != -1) {
        const option = menu.options[optionIndex];
        
        if (option.count > 0) {
          option.price = option.price - (option.price/option.count)
          option.count--;
          
          if (option.count == 0) {
            menu.options.splice(optionIndex, 1); // 옵션 제거
          }
        }
      }
    } else {
      if (menu.count > 0) {
        menu.price = menu.price - (menu.price/menu.count)
        menu.count--;
        if (menu.count == 0) {
          basket.splice(menuIndex, 1); // 메뉴 제거
        }
      }
    }
  }
  changeBasketHtml(basket)
  if (basket.length !== 0) {
    maintainActive(menuIndex, optionIndex);
  }
}

// 장바구니 + 클릭 시
const plusBasketMenu = () => {
  if(basket.length == 0) return;
  const target = document.querySelector('.basket .active');
  const targetType = target.dataset.type;
  const pargetEl = target.closest('li').querySelector('[data-type="menu"]')
  const menuId = targetType == "menu" ? target.dataset.id : pargetEl.dataset.id;
  const optionId = targetType == "menu_option" ? target.dataset.id : "";

  const menuIndex = basket.findIndex(menu => menu.id == menuId);
  let optionIndex = undefined;
  if (menuIndex != -1) {
    const menu = basket[menuIndex];
    
    if (optionId) {
      optionIndex = menu.options.findIndex(option => option.id == optionId);
      
      if (optionIndex != -1) {
        const option = menu.options[optionIndex];
        
        if (option.count > 0) {
          option.price = option.price + (option.price/option.count)
          option.count++;
        }
      }
    } else {
      if (menu.count > 0) {
        menu.price = menu.price + (menu.price/menu.count)
        menu.count++;
      }
    }
  }
  changeBasketHtml(basket)
  maintainActive(menuIndex, optionIndex);
}

// 장바구니 클릭 상태 유지
const maintainActive = (menuIndex, optionIndex) => {
  const basketItems = document.querySelectorAll('.basket li');
  const basketLength = basketItems.length;
  
  if (basketLength === 0) return;
  
  let menuElement = basketItems[Math.min(menuIndex, basketLength - 1)];
  const menuOptions = menuElement.querySelectorAll('[data-type="menu_option"]');
  const menuOptionLength = menuOptions.length;
  
  let targetElement = optionIndex !== undefined && optionIndex !== -1
    ? menuOptions[Math.min(optionIndex, menuOptionLength - 1)]
    : menuElement.querySelector('[data-type="menu"]');
  
  if (optionIndex === undefined || !menuOptions[optionIndex]) {
    targetElement = menuOptionLength === 0
      ? menuElement.querySelector('[data-type="menu"]')
      : menuOptions[Math.max(menuOptionLength - 1, 0)];
  }
  
      
  
  targetElement.classList.add('active');
}

// 장바구니 삭제 클릭 시
const deleteBasketMenu = () => {
  if(basket.length == 0) return;
  const target = document.querySelector('.basket .active');
  const targetType = target.dataset.type;
  const pargetEl = target.closest('li').querySelector('[data-type="menu"]')
  const menuId = targetType == "menu" ? target.dataset.id : pargetEl.dataset.id;
  const optionId = targetType == "menu_option" ? target.dataset.id : "";

  const menuIndex = basket.findIndex(menu => menu.id == menuId);
  if (menuIndex != -1) {
    const menu = basket[menuIndex];
    if (optionId) {
      const optionIndex = menu.options.findIndex(option => option.id == optionId);     
      if (optionIndex != -1) {
        const option = menu.options[optionIndex];
        menu.options.splice(optionIndex, 1); // 옵션 제거
      }
    } else {
      if (menu.count > 0) {
        basket.splice(menuIndex, 1); // 메뉴 제거
      }
    }
  }
  changeBasketHtml(basket)
  let optionIndex = undefined;

  maintainActive(menuIndex, optionIndex);

}

// // 주문하기 용 데이터 만들기
// function transformData(inputData) {
//   const transformedData = [];

//   inputData.forEach(item => {
//     const { id, options } = item;
//     const optionIds = options.map(option => option.id);
//     const optionCount = options.map(option => option.count);

//     const newOptions = [];
//     optionIds.forEach((optionId, index) => {
//       for (let i = 0; i < optionCount[index]; i++) {
//         newOptions.push(optionId);
//       }
//     });

//     transformedData.push({
//       menu_id: id,
//       option_list: newOptions
//     });
//   });

//   return transformedData;
// }

const clickOrder = (event) => {
  console.log('menuAllData,',menuAllData)
  const data = {
    table_id : lastPath,
    // order_list : transformData(deepCopy(menuAllData))
    order_list : deepCopy(menuAllData)
  }
  console.log('data,', data)
  fetch(`/order`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(data => {
    // 받은 데이터 처리
    console.log(data);
    // window.location.href = '/pos/tableList'
  })
  .catch(error => {
    console.error('Error:', error);
  });
  
}