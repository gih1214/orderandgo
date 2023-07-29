const lastPath = window.location.href.split('/').pop();

// 모달 배경 및 닫기 클릭 시 모달 닫기
window.onclick = function (event) {
  if (event.target.id == 'modal' || event.target.closest('.close') != undefined) {
    const _modal = document.querySelector(".modal");
    _modal.classList.remove("show");
    _modal.remove();

  }
}

// 버튼을 클릭하면 모달 열기
const openModalFun = (event) => {
  event.preventDefault();
  document.querySelector('body').insertAdjacentHTML('beforeend','<div id="modal" class="modal"></div>')

  const _modal = document.getElementById('modal')
  _modal.innerHTML = common_modal_html
  _modal.classList.add("show");

}

// 모달 기본 틀 HTML
const common_modal_html = `
  <div class="modal-content">
      <div class="modal-top">
          <h1>모달 제목</h1>
          <i class="ph ph-x close"></i>
      </div>
      <div class="modal-body">
          <p>모달 body</p>
      </div>
  </div>
`

// 페이지 변경 버튼 html 만들기 
const createPageNationBtnHtml = (event) => {
  console.log('화살표 만듬')
  const _article = document.querySelector('main section article');
  let html = `
  <button class="change_page_btn prev_page_btn" onclick="clickChagePageBtn(event, 'prev')">
    <i class="ph ph-caret-left"></i>
  </button>
  <button class="change_page_btn next_page_btn" onclick="clickChagePageBtn(event, 'next')">
    <i class="ph ph-caret-right"></i>
  </button>
  `
  _article.insertAdjacentHTML('beforeend',html)
}

// 페이지 변경 버튼 클릭 시
const clickChagePageBtn = (event, type) => {
  const _article = document.querySelector('main section article')
  const _table = document.querySelector('main section article .items');
  const mainData = lastPath === 'tableList' ? tableData : menuData;
  const curPageIndex = Number(_table.dataset.page);
  const curCategoryId = document.querySelector('main section nav ul li[data-state="active"]').dataset.id;
  let pageLen;
  if(cachingData != null) {
    pageLen = cachingData.find((category)=>category.categoryId == Number(curCategoryId)).pageList.length;
  }else {
    pageLen = mainData.find((category)=>category.categoryId == Number(curCategoryId)).pageList.length;
  }

  
  let newPageIndex
  console.log(type, curPageIndex)
  if(type == 'prev' && curPageIndex > 0){
    newPageIndex = curPageIndex - 1;
  }
  if(type == 'next' && curPageIndex < pageLen-1){
    newPageIndex = curPageIndex + 1;
  }
  if(newPageIndex == undefined) return;
  let targetData;
  if(cachingData != null) {
    if(lastPath == 'tableList'){
      targetData = cachingData.find((category) =>
        category.categoryId == Number(curCategoryId)).pageList[newPageIndex].tableList
    }else {
      targetData = cachingData.find((category) =>
        category.categoryId == Number(curCategoryId)).pageList[newPageIndex].menuList
    }
  }else {
    if(lastPath == 'tableList'){
      targetData = mainData.find((category) =>
        category.categoryId == Number(curCategoryId)).pageList[newPageIndex].tableList
    }else{
      targetData = mainData.find((category) =>
        category.categoryId == Number(curCategoryId)).pageList[newPageIndex].menuList
    }
  }
  
  // const tables_html = changeTableHtml(targetData);
  const tables_html = lastPath === 'tableList' ? changeTableHtml(targetData) : changeMenuHtml(targetData);
  _table.innerHTML = tables_html; 
  _table.setAttribute('data-page', newPageIndex);
  
  _article.classList.remove('hasNextPage');
  _article.classList.remove('hasPrevPage');

  if(0 < newPageIndex){_article.classList.add('hasPrevPage')};
  if(newPageIndex < pageLen-1){_article.classList.add('hasNextPage')};
}