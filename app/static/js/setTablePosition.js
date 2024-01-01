let tableData;
let curCategoryIndex = 0;
let curPage = 0;
let state = {
  has_click_item : false,
  click_item : null,
}

// 테이블 리스트 호출
const callTableList = () => {
  const onSuccess = (data) => {
    console.log(data);
    tableData=data;
    createTableHtml(data, curCategoryIndex, curPage);
  }
  fetchData(`/store/get_table`, 'GET', {}, onSuccess);
}
callTableList();

// 테이블 html 만들기
const createTableHtml = (data, categoryNum, pageNum) => {
  const curData = data[categoryNum].pages[pageNum].tables;
  const categoryHtml = data.map((category,index)=> `
    <li data-id="${category.id}" data-state="${index == 0 ? 'active': ''}">
      <button onclick="changeTableCategory(event,${index})">${category.name}</button>
    </li>
  `).join('');
  document.querySelector('.set_table_position main section nav ul').innerHTML = categoryHtml;
  const tableList = new Array(20).fill(false);
  curData.forEach(data => tableList[data.position-1] = data);
  
  const html = tableList.map((table, index)=>`${table?`
    <button class="item" data-id="${table.id}" data-name="${table.name}" data-active="false" data-has="true" data-page="${pageNum}" data-position="${index+1}" onclick="clickTableArea(event)">
      <h2>${table.name}</h2>
      <div class="icons">
        <i class="ph ph-pencil"></i>
        <i class="ph ph-trash"></i>
      </div>
      <div class="active"><i class="ph ph-arrows-out-cardinal"></i></div>
    </button>
  `:`
    <button class="item" data-has="false" data-page="${pageNum}" data-position="${index+1}" onclick="clickTableArea(event)"><i class="ph ph-plus"></i></button>
  `}`).join('');
  const _items = document.querySelector('.set_table_position main section article .items');
  _items.innerHTML = html;

  const _article = document.querySelector('main section article');

  _article.classList.toggle('hasPrevPage', data[categoryNum].pages[pageNum - 1] !== undefined);
  _article.classList.toggle('hasNextPage', data[categoryNum].pages[pageNum + 1] !== undefined);
}

// 테이블 영역 클릭 시
const clickTableArea = async (event) => {
  const _target = findParentTarget(event.target, 'button.item');
  const isHas = JSON.parse(_target.dataset.has);
  const page = Number(_target.dataset.page);
  const position = Number(_target.dataset.position);
  const name = _target.dataset.name;
  if(isHas){ // 유효한 테이블 클릭
    const isTrash = findParentTarget(event.target, 'i.ph-trash') != undefined ? true : false;
    const isSetName = findParentTarget(event.target, 'i.ph-pencil') != undefined ? true : false;
    if(isSetName){ // 연필 클릭 시
      const tableName = _target.dataset.name;
      const id = Number(_target.dataset.id);
      openModalFun(event)
      const _modal = document.querySelector('.modal');
      const _modalTitle = document.querySelector('.modal-content h1');
      const _modalBody = document.querySelector('.modal-content .modal-body');
      _modalTitle.innerHTML = '테이블 명 변경'
      let html = `
        <div class="top">
          <input type="text" value="${tableName}"/>
        </div>
        <div class="bottom">
          <button onclick="callChangeTableName(event,${id})">적용</button> 
        </div>
      `
      _modalBody.innerHTML = html;
      return;
    }
    if(isTrash){ // 삭제 클릭 
      const id = Number(_target.dataset.id);
      const onSuccess = ()=>{
        _target.dataset.has = false; 
        _target.innerHTML = `<i class="ph ph-plus"></i>`
      }
      await callDeleteTable(id, onSuccess)
      return;
      
    }
    if(state.has_click_item){ // 테이블 위치 변경 api 요청
      const data = {
        table_id_fir : Number(_target.dataset.id),
        table_id_sec : state.click_item.id,
      }
      const onSuccess = () => {
        // 이전 클릭 테이블 변경
        const _preTarget = state.click_item.el;
        _preTarget.dataset.active = false;
        _preTarget.dataset.id = _target.dataset.id;
        _preTarget.dataset.name = _target.dataset.name;
        _preTarget.querySelector('h2').innerHTML = _target.dataset.name;
  
        // 현재 클릭 테이블 변경
        _target.dataset.active = false;
        _target.dataset.id = state.click_item.id;
        _target.dataset.name = state.click_item.name;
        _target.querySelector('h2').innerHTML = state.click_item.name;
        state.has_click_item=false;
        state.click_item = null;
      }
      
      await callChangeTablePostion(data, onSuccess);
      return;
    }
    _target.dataset.active = true;
    state.has_click_item = true;
    state.click_item = {
      id: Number(_target.dataset.id),
      page: page,
      position: position,
      name: name,
      el: _target
    }
    // 클릭 테이블 이동 준비;
  }else{ // 빈 테이블 클릭
    if(state.has_click_item){ // 테이블 위치 변경 api 요청
      const _preTarget = state.click_item.el;
      _preTarget.dataset.active = false;
      _preTarget.dataset.has = false;
      _preTarget.innerHTML = `<i class="ph ph-plus"></i>`;

      _target.dataset.active = false;
      _target.dataset.has = true;
      _target.dataset.id = state.click_item.id;
      _target.dataset.name = state.click_item.name;
      _target.innerHTML = `
        <h2>${state.click_item.name}</h2>
        <div class="icons">
          <i class="ph ph-pencil"></i>
          <i class="ph ph-trash"></i>
        </div>
        <div class="active"><i class="ph ph-arrows-out-cardinal"></i></div>
      `
      state.has_click_item=false;
      state.click_item = null;
      return ;
    }else{
      // 테이블 추가 api 요청;
      const data = {
        name :`${tableData[curCategoryIndex].name} ${position}`,
        seat_count : 4,
        table_category: tableData[curCategoryIndex].id,
        page : page+1,
        position : position,
      }
      const onSuccess = (data) => {
        if(data.code == 200){

        }
        _target.dataset.has = true;
        _target.dataset.name = `${tableData[curCategoryIndex].name} ${position}`;
        _target.dataset.id = data.id;
        _target.innerHTML = `
          <h2>${tableData[curCategoryIndex].name} ${position}</h2>
          <i class="ph ph-trash"></i>
          <div class="active"><i class="ph ph-arrows-out-cardinal"></i></div>
        `
      }
      await callCreateTable(data, onSuccess)
    }
  }
}


const callCreateTable = async (data, onSuccess) => { // 테이블 생성
  fetchData('/adm/create_table', 'POST', data, onSuccess)
}

const callChangeTablePostion = async (data, onSuccess) => { // 테이블 위치 변경
  console.log(data, onSuccess)
  fetchData('/adm/update_table_position', 'PATCH', data, onSuccess)
}

const callDeleteTable = async (id, onSuccess) => { // 테이블 삭제
  fetch(`/adm/table/${id}`, {
    method: 'DELETE',
  })
  .then(data => onSuccess(data))
  .catch(error => {
    console.error('Error:', error);
  });
}
const callChangeTableName = async (event, id) => {
  const _modal = document.querySelector('.modal');
  const text = _modal.querySelector('input[type="text"]').value;
  const data = {
    table_id : id,
    name : text,
  }
  const onSuccess = (data) => {
    const target = document.querySelector(`button.item[data-id="${id}"]`)
    target.querySelector('h2').innerHTML = text;
    _modal.click;
  }
  await fetchData('/adm/update_table_name', 'PATCH', data, onSuccess);
}

// 페이지 변경 클릭 시
const clickChangeTablePosition = (event, type) => {
  if(type == 'prev'){ // 이전 페이지
    curPage -= 1;
  }
  if(type == 'next') { // 다음 페이지
    curPage += 1;
  }
  createTableHtml(tableData, curCategoryIndex, curPage);
}