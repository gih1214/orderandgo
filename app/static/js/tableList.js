let tableData;
fetch('/pos/get_table_page', {
  method: 'GET',
})
.then(response => response.json())
.then(data => {
  // 받은 데이터 처리
  console.log(data);
  tableData = data;
  createHtml(data);
})
.catch(error => {
  console.error('Error:', error);
});

const createHtml = (tablePageData) => {
  const _tableCategory = document.querySelector('main section nav ul');
  const _table = document.querySelector('main section article .items');
  
  let nav_html = '';
  tablePageData.forEach((data, index)=>{
    nav_html += `
      <li data-id="${data.categoryId}" data-state="${index == 0 ? 'active': ''}">
        <button onclick="changeTableCategory(event,${index})">${data.category}</button>
      </li>`;
    _tableCategory.innerHTML =  nav_html;
    if(index != 0) return;

    const tables = data.pageList[0].tableList;
    const tables_html = changeTableHtml(tables);
    _table.innerHTML = tables_html;
  })
}

// 테이블 카테고리 변경
const changeTableCategory = (event, index) => {
  const prevBtn = document.querySelector('main section nav ul li[data-state="active"]')
  prevBtn.dataset.state = '';

  const _li = event.target.closest('li');
  const _table = document.querySelector('main section article .items');

  _li.dataset.state = 'active'

  let tables_html
  if(cachingData != null) {
    tables_html = changeTableHtml(cachingData[index].pageList[0].tableList);
  }else {
    tables_html = changeTableHtml(tableData[index].pageList[0].tableList);  
  }
  _table.innerHTML = tables_html;
}

const changeTableHtml = (tables) => {
  let html = '';
  tables.forEach((table, index)=>{
    html += `
      <button class="table item" data-id="${table.tableId}" data-state="${table.statusId}" style="border:${table.groupId != 0 ? "1px solid " + table.groupColor : ""}"
        onclick="clickTable(${table.tableId})">
        `
      if(table.isGroup != 0) {
        html += `
          <div class="item_grop_num" data-id="${table.groupId}" style="background : ${table.groupColor}">${table.groupNum}</div>
        `

      }
      html +=` 
        <div class="transparent_group_box" onclick="clickTransparentGroupTable(event)"></div>
        <div class="transparent_move_box" onclick="clickTransparentMoveTable(event)"></div>
        <div class="title">
          <h2>${table.table} <i class="ph-fill ph-bell-ringing"></i></h2>
          <div class="table_state">${table.statusId != 0 ? table.status : ''}</div>
        </div>
        <div class="body">
          <i class="ph-bold ph-plus"></i>
          <ul>
          `
          if(table.orderList.length != 0){
            const orderList = table.orderList;
            orderList.forEach((order, orderIndex)=>{
              if(orderIndex <= 2){
                html +=`
                <li data-id="${order.menuId}">
                  <span>${order.menu}</span>
                  <span>${order.count}</span>
                </li>
                `
              } 
              if(orderIndex == 2){
                html += `
                  <li class="order_more">
                    <span>외 ${orderList.length - 3}</span>
                  </li>` 
              }
            })
          }

        html +=`
          </ul>
        </div>
      </button>`
  })
  return html;
}

function clickTable(table_id){
  console.log('클릭함')
  window.location.href=`/pos/menuList/${table_id}`
}

// 테이블 그룹지정 버튼 클릭 시
let cachingData = null;
const clickGroupBtn = (event) => {
  const asideHtml = 
    `
    <div class="left selete_box_group">
      <button data-value="1" data-text="그룹 1" class="btn-dropdown" onclick="clickDropDownBtn(event)">
        <div>1</div>
        <span>그룹 1</span>
        <i class="ph ph-caret-up"></i>
      </button>

      <ul class="dropdown-list">
        <li data-value="1" data-text="그룹 1" class="" onclick="clickCurGroupNum(event)">
          <div>1</div>
          <span>그룹 1</span>
          <button onclick="clickGroupDeleteBtn(event)">
            <i class="ph ph-trash"></i>
          </button>
        </li>
        <button data-value="" data-text="그룹 추가" onclick="clickAddGroupList(event)">
          <i class="ph ph-plus"></i>
          <span>그룹 추가</span>
        </button>
      </ul>
    </div>
    <div class="right custom_btns">
      <button onclick="clickSetGroupCancelBtn(event)">취소</button>
      <button onclick="clickSetGroupSaveBtn(event)" class="active">저장</button>
    </div>
    `

  const _modal = document.querySelector('.modal');
  _modal.click();
  const _groupEl = document.querySelector('main section aside');
  _groupEl.innerHTML = asideHtml;
  _groupEl.classList.add('active');
  const _mainEl = document.querySelector('main section article')
  _mainEl.classList.add('group')
  _mainEl.classList.remove('move')
  _mainEl.classList.add('disabled')
  cachingData = JSON.parse(JSON.stringify(tableData));
}

// 테이블 합석/이동 버튼 클릭 시
const clickMoveAndjoinBtn = (event) => {
  const asideHtml = 
  `
    <div class="left">
    </div>
    <div class="right custom_btns">
      <button onclick="clickCombineMoveCancelBtn(event)">취소</button>
      <button onclick="clickCombineMoveSaveBtn(event)" class="active">저장</button>
    </div>
    `
  const _modal = document.querySelector('.modal');
  _modal.click();
  const _groupEl = document.querySelector('main section aside');
  _groupEl.classList.add('active');
  _groupEl.innerHTML = asideHtml;
  const _mainEl = document.querySelector('main section article')
  _mainEl.classList.add('move')
  _mainEl.classList.remove('group')
  _mainEl.classList.add('disabled')
  cachingData = JSON.parse(JSON.stringify(tableData));


}

const clickSetBtn = (event) => {
  openModalFun(event)
  const _modal = document.querySelector('.modal');
  const _modalTitle = document.querySelector('.modal-content h1');
  const _modalBody = document.querySelector('.modal-content .modal-body');
  _modalTitle.innerHTML = '설정'
  let html = `
    <div class="top">
      <div class="grid">
        <button class="" onclick="clickMoveAndjoinBtn(event)">
          <i class="ph ph-swap"></i>
          <span>이동/합석</span>
        </button>
        <button class="" onclick="clickGroupBtn(event)">
          <i class="ph ph-users-three"></i>
          <span>그룹</span>
        </button>
        <button class="" onclick="clickZoningBtn(event)">
          <i class="ph ph-squares-four"></i>
          <span>구역 설정</span>
        </button>
        <button class="" onclick="clickSetTableBtn(event)">
          <i class="ph ph-subtract-square"></i>
          <span>테이블 설정</span>
        </button>
      </div>
    </div>
    <div class="bottom"></div>
  `
  _modalBody.innerHTML = html;
}

// 그룹 셀렉트 드롭박스 클릭 시
const clickDropDownBtn = (event) => {
  const _dropDownBtn = event.currentTarget;
  const _dropDownList = _dropDownBtn.nextElementSibling;
  _dropDownList.classList.toggle('active');
}
// 그룹 셀렉트 박스에서 그룹 추가 클릭 시
let groupNum = 1;
const clickAddGroupList = (event) => {
  const _target = event.currentTarget;
  groupNum += 1;
  let html = `
    <li data-value="${groupNum}" data-text="그룹 ${groupNum}" class="" onclick="clickCurGroupNum(event)">
      <div>${groupNum}</div>
      <span>그룹 ${groupNum}</span>
      <button onclick="clickGroupDeleteBtn(event)">
        <i class="ph ph-trash"></i>
      </button>
    </li>
  `;
  _target.insertAdjacentHTML('beforebegin', html)
}

//그룹 셀렉트 박스에서 특정 그룹 삭제 버튼 클릭 시
const clickGroupDeleteBtn = (event) =>{
  event.stopPropagation();
  const _target = event.currentTarget;
  const _targetGroup = _target.closest('li');
  const value = _targetGroup.dataset.value;
  const __groupEls = document.querySelectorAll('.item_grop_num');
  __groupEls.forEach((item)=>{
    if(item.textContent == value){
      item.closest('.item').style.border = '';
      item.remove();
    }
  });
  _targetGroup.remove();
}

// 그룹 셀릭트 박스에서 현재 그룹 변경 클릭 시
const clickCurGroupNum = (event) => {
  const _target = event.currentTarget;
  const _dropDwonList = _target.closest('.dropdown-list');
  const groupNum = _target.dataset.value;
  const _dropDownBtn = document.querySelector('.selete_box_group .btn-dropdown')
  _dropDownBtn.querySelector('div').innerHTML = groupNum;
  _dropDownBtn.querySelector('span').innerHTML = '그룹 ' + groupNum;

  _dropDownBtn.dataset.value = groupNum;
  _dropDownBtn.dataset.text = '그룹 ' + groupNum;
  _dropDwonList.classList.remove('active');

}

// 그룹 지정 환경에서 테이블 클릭 시
const clickTransparentGroupTable = (event) => {
  event.stopPropagation();
  const _target = event.currentTarget.closest('.item');
  const curGroup = document.querySelector('.selete_box_group .btn-dropdown');
  const value = curGroup.dataset.value;
  const curNumEl = curGroup.querySelector('div');
  const computedStyle = window.getComputedStyle(curNumEl);
  const backgroundColor = computedStyle.backgroundColor;
  
  const curCategoryId = document.querySelector('main section nav ul li[data-state="active"]').dataset.id;
  const curPage = 1
  const itemId = _target.dataset.id;

  const targetData = 
    cachingData
      .find((category)=>category.categoryId == Number(curCategoryId))
      .pageList
      .find((pageData)=>pageData.page == curPage)
      .tableList
      .find((table)=>table.tableId == Number(itemId))

  if (targetData.isGroup == 1 && targetData.groupId == Number(value)) {
    targetData.groupColor = '';
    targetData.groupId = '';
    targetData.groupNum = '';
    targetData.isGroup = 0;
  } else {
    targetData.groupColor = backgroundColor;
    targetData.groupId = Number(value);
    targetData.groupNum = Number(value);
    targetData.isGroup = 1;
  }
  const changeTableData = cachingData
    .find((category)=>category.categoryId == Number(curCategoryId))
    .pageList
    .find((pageData)=>pageData.page == curPage)
    .tableList
  
  const tables_html = changeTableHtml(changeTableData)
  const _table = document.querySelector('main section article .items');
  _table.innerHTML = tables_html;

}

// 그룹 지정 취소 버튼 클릭 시
const clickSetGroupCancelBtn = (event) => {
  const _mainEl = document.querySelector('main section article');
  const _aside = document.querySelector('main section > aside');
  _mainEl.classList.remove('disabled');
  _aside.classList.remove('active');

  const curCategoryId = document.querySelector('main section nav ul li[data-state="active"]').dataset.id;
  const curPage = 1
  const targetData = 
    tableData
    .find((category)=>category.categoryId == Number(curCategoryId))
    .pageList
    .find((pageData)=>pageData.page == curPage)
    .tableList

  const tables_html = changeTableHtml(targetData)
  const _table = document.querySelector('main section article .items');
  _table.innerHTML = tables_html;
  cachingData = null
}


// 그룹 지정 저장 버튼 클릭 시
const clickSetGroupSaveBtn = (event) => {
  const _mainEl = document.querySelector('main section article')
  const _aside = document.querySelector('main section > aside');

  _mainEl.classList.remove('disabled')
  _aside.classList.remove('active');
  // 백으로 저장 api 호출하기
  tableData = JSON.parse(JSON.stringify(cachingData));
  cachingData = null;
}

// 테이블 이동/합석 환경에서 테이블 클릭 시
const cachingSetTableData = []
const clickTransparentMoveTable = (event) => {
  event.stopPropagation();
  const _target = event.currentTarget.closest('.item');
  const curCategoryId = document.querySelector('main section nav ul li[data-state="active"]').dataset.id;
  const curPage = 1
  const itemId = _target.dataset.id;

  const targetData = 
    cachingData
      .find((category)=>category.categoryId == Number(curCategoryId))
      .pageList
      .find((pageData)=>pageData.page == curPage)
      .tableList
      .find((table)=>table.tableId == Number(itemId))
  
  const targetStatusId = targetData.statusId;
  const curCachingDataLen = cachingSetTableData.length;
  if(targetStatusId != 0 && curCachingDataLen == 0) {
    // 첫번째 테이블 선택
    cachingSetTableData.push(targetData)
  }else if(targetStatusId != 0 && curCachingDataLen != 0){
    // 테이블 합석
    console.log(`${cachingSetTableData[0].table}에서 ${targetData.table}(으)로 합석합니다.`)
    
    // cachingSetTableData[0].tableId 
    // targetData.tableId


    // 초기화
    cachingSetTableData.length = 0
  }else if(targetStatusId == 0 && curCachingDataLen != 0){
    // 테이블 이동
    console.log(`${cachingSetTableData[0].table}에서 ${targetData.table}(으)로 이동합니다.`)
    for( key in targetData) {
      if(targetData[key] != 'table' || targetData[key] != 'tableId'){
        console.log(key, targetData[key])
      }
    }
    console.log(targetData)
    
    // cachingSetTableData[0].tableId 
    // targetData.tableId


    // 초기화
    cachingSetTableData.length = 0
  }
  // if (targetData.isGroup == 1 && targetData.groupId == Number(value)) {
  //   targetData.groupColor = '';
  //   targetData.groupId = '';
  //   targetData.groupNum = '';
  //   targetData.isGroup = 0;
  // } else {
  //   targetData.groupColor = backgroundColor;
  //   targetData.groupId = Number(value);
  //   targetData.groupNum = Number(value);
  //   targetData.isGroup = 1;
  // }
  // const changeTableData = cachingData
  //   .find((category)=>category.categoryId == Number(curCategoryId))
  //   .pageList
  //   .find((pageData)=>pageData.page == curPage)
  //   .tableList
  
  // const tables_html = changeTableHtml(changeTableData)
  // const _table = document.querySelector('main section article .items');
  // _table.innerHTML = tables_html;


}