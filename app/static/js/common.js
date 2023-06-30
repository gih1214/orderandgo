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
