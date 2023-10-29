let tableData;
let curCategoryIndex = 0;
let curPage = 0;

// 테이블 리스트 호출
const callTableList = () => {
  const onSuccess = (data) => {
    console.log(data);
  }
  fetchData(`/pos/get_table_page`, 'GET', {}, onSuccess)
}
callTableList();