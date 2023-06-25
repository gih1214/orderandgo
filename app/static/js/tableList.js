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

    const tables = data.tableList;
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

  const tables_html = changeTableHtml(tableData[index].tableList);
  _table.innerHTML = tables_html;
}

const changeTableHtml = (tables) => {
  let html = '';
  tables.forEach((table, index)=>{
    html += `
      <button class="table item" data-state="${table.statusId}" 
        onclick="clickTable(${table.tableId})">
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

