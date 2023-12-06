
// 메뉴판 페이지 우측 장바구니 상단 버튼 HTML
const posMenuListBasketTopBtnsHtml = () => {
  return `
    <button 
      onclick="minusBasketMenu(event)" 
      data-active="false" 
      class="minus">
      <i class="ph ph-minus"></i>
    </button>
    <button 
      onclick="plusBasketMenu(event)" 
      data-active="false" 
      class="plus">
      <i class="ph ph-plus"></i>
    </button>
    <button 
      onclick="deleteBasketMenu(event)" 
      class="delete" 
      data-active="false">
      <i class="ph ph-trash"></i>
    </button>
    <button 
      onclick="clickOrderHistoryBtn(event)" 
      class="order_history" 
      data-check="false" 
      data-active="true">
      주문내역
    </button>
  `
}


// 메뉴판 페이지 우측 주문내역 상단 버튼 HTML
const posMenuListOrderListTopBtnsHtml = () => {
  return `
    <button 
      onclick="minusOrderListMenu(event)" 
      data-active="false" 
      class="minus">
      <i class="ph ph-minus"></i>
    </button>
    <button 
      onclick="plusOrderListMenu(event)" 
      data-active="false" 
      class="plus">
      <i class="ph ph-plus"></i>
    </button>
    <button 
      onclick="deleteOrderListMenu(event)" 
      class="delete" 
      data-active="false">
      <i class="ph ph-trash"></i>
    </button>
    <button 
      onclick="clickBasketBtn(event)" 
      class="new_order" 
      data-active="true">
      장바구니
    </button>
  `
}