let mainCategoryData;
let subCategoryData;
let menuData;
let allMenuData;

// 메인카테고리 데이터 가져오기
fetch(`/store/get_main_category`, {
  method: 'GET',
})
.then(response => response.json())
.then(data => {
  // 받은 데이터 처리
  console.log(data);
  mainCategoryData = data;
  // createHtml(data);
})
.catch(error => {
  console.error('Error:', error);
});


// 서브카테고리 데이터 가져오기
fetch(`/store/get_sub_category`, {
  method: 'GET',
})
.then(response => response.json())
.then(data => {
  // 받은 데이터 처리
  console.log(data);
  subCategoryData = data;
  // createHtml(data);
})
.catch(error => {
  console.error('Error:', error);
});


// 메뉴 데이터 가져오기
fetch(`/store/get_menu_list`, {
  method: 'GET',
})
.then(response => response.json())
.then(data => {
  // 받은 데이터 처리
  console.log(data);
  menuData = data;
  // createHtml(data);
})
.catch(error => {
  console.error('Error:', error);
});

// 메뉴 데이터 가져오기
fetch(`/store/all_menu_list`, {
  method: 'GET',
})
.then(response => response.json())
.then(data => {
  // 받은 데이터 처리
  console.log(data);
  allMenuData = data;
  // createHtml(data);
})
.catch(error => {
  console.error('Error:', error);
});


// 메뉴 영역 확장 버튼 클릭 시
const clickResponsiveBtn = (event) => {
  const _main = document.querySelector('main');
  _main.classList.toggle('open_aside')
}
