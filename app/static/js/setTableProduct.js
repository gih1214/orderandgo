let tableData;
let curCategoryIndex = 0;
let curPage = 0;

// 테이블 리스트 호출
const callTableList = () => {
  const onSuccess = (data) => {
    console.log(data);
    createTableHtml(data, 0, 0);
  }
  fetchData(`/store/get_table`, 'GET', {}, onSuccess);
}
callTableList();

// 테이블 html 만들기
const createTableHtml = (data, categoryNum, pageNum) => {
  console.log(categoryNum, pageNum)
  const curData = data[categoryNum].pages[pageNum].tables
  const tableList = new Array(20).fill(false);
  curData.forEach(data=>tableList[data.position-1] = data);
  const html = tableList.map((table,index)=>`${table?`
    <button class="item" data-has="true" data-active="false">
      <h2>${table.name}</h2>
      <i class="ph ph-trash"></i>
      <div class="active"><i class="ph ph-arrows-out-cardinal"></i></div>
    </button>
  `:`
    <button class="item" data-has="false"><i class="ph ph-plus"></i></button>
  `}`).join('');
  const _items = document.querySelector('.set_table_product main section article .items');
  _items.innerHTML = html;

  const _article = document.querySelector('main section article');
  if(data[categoryNum].pages[pageNum-1]!=undefined){_article.classList.add('hasPrevPage')};
  if(data[categoryNum].pages[pageNum+1]!=undefined){_article.classList.add('hasNextPage')};
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