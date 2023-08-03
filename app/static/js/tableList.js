let tableData;
let cachingData = null;
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

    const PAGE_INDEX = 0;
    const tables = data.pageList[PAGE_INDEX].tableList;
    const tables_html = changeTableHtml(tables);
    _table.innerHTML = tables_html;

    _table.setAttribute('data-page', PAGE_INDEX);
    createPageNationBtnHtml();
    const _article = document.querySelector('main section article');
    const curCategoryId = document.querySelector('main section nav ul li[data-state="active"]').dataset.id;
    const pageLen = tableData.find((category)=>category.categoryId == Number(curCategoryId)).pageList.length;
    if(0 < PAGE_INDEX){_article.classList.add('hasPrevPage')};
    if(PAGE_INDEX < pageLen-1){_article.classList.add('hasNextPage')};
  })
}

// 테이블 카테고리 변경
const changeTableCategory = (event, index) => {
  const prevBtn = document.querySelector('main section nav ul li[data-state="active"]')
  prevBtn.dataset.state = '';

  const _li = event.target.closest('li');
  const _table = document.querySelector('main section article .items');

  _li.dataset.state = 'active'
  const PAGE_INDEX = 0;
  let tables_html
  if(cachingData != null) {
    tables_html = changeTableHtml(cachingData[index].pageList[PAGE_INDEX].tableList);
  }else {
    tables_html = changeTableHtml(tableData[index].pageList[PAGE_INDEX].tableList);  
  }
  _table.innerHTML = tables_html;
  _table.setAttribute('data-page', PAGE_INDEX);

  const _article = document.querySelector('main section article');
  _article.classList.remove('hasNextPage');
  _article.classList.remove('hasPrevPage');


  const curCategoryId = document.querySelector('main section nav ul li[data-state="active"]').dataset.id;
  const pageLen = tableData.find((category)=>category.categoryId == Number(curCategoryId)).pageList.length;
  if(PAGE_INDEX < pageLen-1){_article.classList.add('hasNextPage')};

}

const changeTableHtml = (tables) => {
  console.log('changeTableHtml',tables)
  let html = '';
  tables.forEach((table, index)=>{
    html += `
      <button class="table item ${table.select ? 'select' : ''}" data-id="${table.tableId}" data-state="${table.statusId}" style="border:${table.groupId != 0 ? "1px solid " + table.groupColor : ""}"
        onclick="clickTable(${table.tableId})">
        `
      if(table.isGroup != 0) {
        html += `
          <div class="item_grop_num" data-id="${table.groupId}" style="background : ${table.groupColor}">${table.groupNum}</div>
        `

      }
      html +=` 
        <div class="transparent_group_box" onclick="clickTransparentGroupTable(event)">
          <i class="ph-fill ph-check-fat"></i>
        </div>
        <div class="transparent_move_box" onclick="clickTransparentMoveTable(event)">
          <i class="ph-fill ph-check-fat"></i>
        </div>
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

// // 페이지 변경 버튼 html 만들기 
// const createPageNationBtnHtml = (event) => {
//   console.log('화살표 만듬')
//   const _article = document.querySelector('main section article');
//   let html = `
//   <button class="change_page_btn prev_page_btn" onclick="clickChagePageBtn(event, 'prev')">
//     <i class="ph ph-caret-left"></i>
//   </button>
//   <button class="change_page_btn next_page_btn" onclick="clickChagePageBtn(event, 'next')">
//     <i class="ph ph-caret-right"></i>
//   </button>
//   `
//   _article.insertAdjacentHTML('beforeend',html)
// }



function clickTable(table_id){
  console.log('클릭함')
  window.location.href=`/pos/menuList/${table_id}`
}



// 테이블 그룹지정 버튼 클릭 시
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
      ${ groupColors.map(({num, color})=>`
        <li data-value="${num}" data-text="그룹 ${num}" class="" data-color="${color}" onclick="clickCurGroupNum(event)">
          <div style="background: ${color}">${num}</div>
          <span>그룹 ${num}</span>
          <button onclick="clickGroupDeleteBtn(event)">
            <i class="ph ph-trash"></i>
          </button>
        </li>
      `).join('')}
        <!-- 
        <button data-value="" data-text="그룹 추가" onclick="clickAddGroupList(event)">
          <i class="ph ph-plus"></i>
          <span>그룹 추가</span>
        </button>
        -->
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

  // 캐싱 데이터에서 선택 그룹 데이터 삭제
  cachingData.forEach((categoryData)=>{
    categoryData.pageList.forEach((pageData)=>{
      pageData.tableList.forEach((table)=>{
        if(Number(table.groupId) == Number(value)){
          table.groupColor = '';
          table.groupId = '';
          table.isGroup = 0;
        }
      })
    })
  })

  // 현재 화면에서 해당 그룹 스타일 변경
  __groupEls.forEach((item)=>{
    if(item.textContent == value){
      item.closest('.item').style.border = '';
      item.remove();
    }
  });
}

// 그룹 셀릭트 박스에서 현재 그룹 변경 클릭 시
const clickCurGroupNum = (event) => {
  const _target = event.currentTarget;
  const _dropDwonList = _target.closest('.dropdown-list');
  const groupNum = _target.dataset.value;
  const groupColor = _target.dataset.color;
  const _dropDownBtn = document.querySelector('.selete_box_group .btn-dropdown')
  _dropDownBtn.querySelector('div').innerHTML = groupNum;
  _dropDownBtn.querySelector('div').style.background = groupColor;
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
  const _table = document.querySelector('main section article .items');

  const curPage = Number(_table.dataset.page);
  const itemId = _target.dataset.id;

  const targetData = 
    cachingData
      .find((category)=>category.categoryId == Number(curCategoryId))
      .pageList[curPage]
      .tableList
      .find((table)=>table.tableId == Number(itemId))

  if (targetData.isGroup == 1 && targetData.groupId == Number(value)) {
    targetData.groupColor = undefined;
    targetData.groupId = undefined;
    targetData.groupNum = undefined;
    targetData.isGroup = 0;
  } else {
    targetData.groupColor = backgroundColor;
    targetData.groupId = Number(value);
    targetData.groupNum = Number(value);
    targetData.isGroup = 1;
  }
  const changeTableData = cachingData
    .find((category)=>category.categoryId == Number(curCategoryId))
    .pageList[curPage]
    .tableList
  
  const tables_html = changeTableHtml(changeTableData)
  _table.innerHTML = tables_html;

}

// 그룹 지정 취소 버튼 클릭 시
const clickSetGroupCancelBtn = (event) => {
  changeStyleOnSet();

  const curCategoryId = document.querySelector('main section nav ul li[data-state="active"]').dataset.id;
  const _table = document.querySelector('main section article .items');
  const curPage = Number(_table.dataset.page);
  const targetData = 
    tableData
    .find((category)=>category.categoryId == Number(curCategoryId))
    .pageList[curPage]
    .tableList

  const tables_html = changeTableHtml(targetData)
  _table.innerHTML = tables_html;
  cachingData = null
}


// 그룹 지정 저장 버튼 클릭 시
const clickSetGroupSaveBtn = (event) => {
  changeStyleOnSet()
  // 백으로 저장 api 호출하기
  const group_data = [];
  tableData = JSON.parse(JSON.stringify(cachingData));
  tableData.forEach((categoryData, index) => {
    categoryData.pageList.forEach((pageData, index)=>{
      pageData.tableList.forEach((table)=>{
        group_data.push({
          'table_id': table.tableId,
          'group_id': table.groupId == undefined ? null : table.groupId,
          'group_color':table.groupColor == undefined ? null : table.groupColor
        })
      })
    })
  })
  fetch('/pos/set_group', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(group_data)
  })
  .then(response => response.json())
  .then(data => {
    // 받은 데이터 처리
    console.log(data);
  })
  .catch(error => {
    console.error('Error:', error);
  });
  cachingData = null;
}

// 테이블 이동/합석 환경에서 테이블 클릭 시
const cachingSetTableData = []
const tableMoveList = [];
const clickTransparentMoveTable = (event) => {
  event.stopPropagation();
  const _target = event.currentTarget.closest('.item');
  const curCategoryId = document.querySelector('main section nav ul li[data-state="active"]').dataset.id;
  const _table = document.querySelector('main section article .items');
  const curPage = Number(_table.dataset.page);
  const itemId = _target.dataset.id;

  const targetData = 
    cachingData
      .find((category)=>category.categoryId == Number(curCategoryId))
      .pageList[curPage].tableList
      .find((table)=>table.tableId == Number(itemId))
  const targetStatusId = targetData.statusId;
  const curCachingDataLen = cachingSetTableData.length;
  if(targetStatusId != 0 && curCachingDataLen == 0) {
    // 첫번째 테이블 선택
    cachingSetTableData.push(targetData)
    targetData['select'] = true;
    const tables_html = changeTableHtml(cachingData
      .find((category)=>category.categoryId == Number(curCategoryId))
      .pageList[curPage].tableList
    )
    const _table = document.querySelector('main section article .items');
    _table.innerHTML = tables_html;
  }else if(targetStatusId != 0 && curCachingDataLen != 0){
    if (targetData.tableId == cachingSetTableData[0].tableId) return
    // 테이블 합석
    console.log(cachingSetTableData[0],targetData)
    tableMoveList.push({
      start_table_id : cachingSetTableData[0].tableId,
      end_table_id : targetData.tableId,
    })
    console.log(`${cachingSetTableData[0].table}에서 ${targetData.table}(으)로 합석합니다.`)
    delete cachingSetTableData[0].select;

    targetData.orderList = mergeOrderLists(cachingSetTableData[0], targetData).orderList;
    
    cachingSetTableData[0] = createEmptyTable(cachingSetTableData[0]);

    const tables_html = changeTableHtml(cachingData
      .find((category)=>category.categoryId == Number(curCategoryId))
      .pageList[curPage].tableList
    )
    const _table = document.querySelector('main section article .items');
    _table.innerHTML = tables_html;

    // 초기화
    cachingSetTableData.length = 0
  }else if(targetStatusId == 0 && curCachingDataLen != 0){
    console.log(cachingSetTableData[0],targetData)
    tableMoveList.push({
      start_table_id : cachingSetTableData[0].tableId,
      end_table_id : targetData.tableId,
    })
    // 테이블 이동
    console.log(`${cachingSetTableData[0].table}에서 ${targetData.table}(으)로 이동합니다.`)
    delete cachingSetTableData[0].select;

    for( key in targetData) {
      if(key != 'table' && key != 'tableId'){
        targetData[key] = JSON.parse(JSON.stringify(cachingSetTableData[0][key]));   
      }
    }
    cachingSetTableData[0] = createEmptyTable(cachingSetTableData[0]);

    const tables_html = changeTableHtml(cachingData
      .find((category)=>category.categoryId == Number(curCategoryId))
      .pageList[curPage].tableList
    )
    const _table = document.querySelector('main section article .items');
    _table.innerHTML = tables_html;

    // 초기화
    cachingSetTableData.length = 0
  }

}

// orderList 병합 하기
function mergeOrderLists(existingData, newData) {
  const existingOrders = existingData.orderList;
  const newOrders = newData.orderList;

  newOrders.forEach(newOrder => {
    const existingOrder = existingOrders.find(order => order.menuId === newOrder.menuId);

    if (existingOrder) {
      existingOrder.count += newOrder.count;

      newOrder.optionList.forEach(newOption => {
        const existingOption = existingOrder.optionList.find(option => option.optionId === newOption.optionId);

        if (existingOption) {
          existingOption.count += newOption.count;
        } else {
          existingOrder.optionList.push(newOption);
        }
      });
    } else {
      existingOrders.push(newOrder);
    }
  });

  return existingData;
}

// 이동/합석 취소 버튼 클릭 시
const clickCombineMoveCancelBtn = (event) => {
  changeStyleOnSet();
  tableMoveList.length=0;
  const curCategoryId = document.querySelector('main section nav ul li[data-state="active"]').dataset.id;
  const _table = document.querySelector('main section article .items');
  const curPage = _table.dataset.page;
  const targetData = 
    tableData
    .find((category)=>category.categoryId == Number(curCategoryId))
    .pageList[curPage].tableList

  const tables_html = changeTableHtml(targetData)
  _table.innerHTML = tables_html;
  cachingData = null
}

// 이동/합석 저장 버튼 클릭 시
const clickCombineMoveSaveBtn = (event) => {
  changeStyleOnSet();
  // 백으로 저장 api 호출하기
  const data = setMoveTableList(tableMoveList)
  tableData = JSON.parse(JSON.stringify(data));
  console.log(tableData)
  fetch(`/pos/set_table`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(tableData)
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
  cachingData = null;
  // 테이블 이동/합석 내역 초기화
  tableMoveList.length=0;
}

// 테이블 이동/합석 내역 데이터 정리
const setMoveTableList = (inputList) => {
  let resultList = [];
  for (let inputIndex = 0; inputIndex < inputList.length; inputIndex++) {
    const current = inputList[inputIndex];
    let curStartList = [current.start_table_id];
  
    for (let resultIndex = 0; resultIndex < resultList.length; resultIndex++) {
      const previous = resultList[resultIndex];
      if (current.start_table_id === previous.end_table_id || previous.end_table_id === current.end_table_id) {
        const previousStartList = previous.start_table_id;
        curStartList = [...curStartList, ...previousStartList];
        delete resultList[resultIndex].end_table_id
      }
    }
  
    const dataObject = { start_table_id: curStartList, end_table_id: current.end_table_id }
    if (dataObject.start_table_id.includes(dataObject.end_table_id)) {
      dataObject.start_table_id = dataObject.start_table_id.filter((value) => value !== dataObject.end_table_id);
    }
    
    resultList.push(dataObject);
  }
  return resultList = resultList.filter(item => item.hasOwnProperty('end_table_id'));
  
}

// 빈 테이블 만들기
const createEmptyTable = (tableData) => {
  tableData['groupColor'] = ''
  tableData['groupId'] = ''
  tableData['groupNum'] = ''
  tableData['isGroup'] = 0
  tableData['orderList'] = []
  tableData['status'] = '빈 테이블'
  tableData['statusId'] = 0
  return tableData
}

// 테이블 설정 시 배경 화면 설정
const changeStyleOnSet = () => {
  const _mainEl = document.querySelector('main section article');
  const _aside = document.querySelector('main section > aside');
  _mainEl.classList.remove('group')
  _mainEl.classList.remove('move')
  _mainEl.classList.remove('disabled')
  _aside.classList.remove('active');
}