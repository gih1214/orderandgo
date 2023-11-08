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
    createTableHtml(data, 0, 0);
  }
  fetchData(`/store/get_table`, 'GET', {}, onSuccess);
}
callTableList();

// 테이블 html 만들기
const createTableHtml = (data, categoryNum, pageNum) => {
  const curData = data[categoryNum].pages[pageNum].tables
  const tableList = new Array(20).fill(false);
  curData.forEach(data=>tableList[data.position-1] = data);
  const html = tableList.map((table,index)=>`${table?`
    <button class="item" data-id="${table.id}" data-name="${table.name}" data-active="false" data-has="true" data-page="${pageNum}" data-position="${index+1}" onclick="clickTableArea(event)">
      <h2>${table.name}</h2>
      <i class="ph ph-trash"></i>
      <div class="active"><i class="ph ph-arrows-out-cardinal"></i></div>
    </button>
  `:`
    <button class="item" data-has="false" data-page="${pageNum}" data-position="${index+1}" onclick="clickTableArea(event)"><i class="ph ph-plus"></i></button>
  `}`).join('');
  const _items = document.querySelector('.set_table_product main section article .items');
  _items.innerHTML = html;

  const _article = document.querySelector('main section article');

  _article.classList.toggle('hasPrevPage', data[categoryNum].pages[pageNum - 1] !== undefined);
  _article.classList.toggle('hasNextPage', data[categoryNum].pages[pageNum + 1] !== undefined);
}

// 테이블 영역 클릭 시
const clickTableArea = (event) => {
  const _target = findParentTarget(event.target, 'button.item');
  const isHas = JSON.parse(_target.dataset.has);
  const page = Number(_target.dataset.page);
  const position = Number(_target.dataset.position);
  const name = _target.dataset.name;
  if(isHas){ // 유효한 테이블 클릭
    const isTrash = findParentTarget(event.target, 'i.ph-trash') != undefined ? true : false;
    if(isTrash){
      _target.dataset.has = false;
      _target.innerHTML = `<i class="ph ph-plus"></i>`
      return;
    }
    if(state.has_click_item){ // 테이블 위치 변경 api 요청
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
      return ;
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
        <i class="ph ph-trash"></i>
        <div class="active"><i class="ph ph-arrows-out-cardinal"></i></div>
      `
      state.has_click_item=false;
      state.click_item = null;
      return ;
    }else{
      // 테이블 추가 api 요청;
      _target.dataset.has = true;
      _target.dataset.name = `${tableData[curCategoryIndex].name} ${position}`;
      _target.innerHTML = `
        <h2>${tableData[curCategoryIndex].name} ${position}</h2>
        <i class="ph ph-trash"></i>
        <div class="active"><i class="ph ph-arrows-out-cardinal"></i></div>
      `
    }
  }
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