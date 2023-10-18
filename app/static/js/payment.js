let order_history = [];

// 테이블 주문 내역 가져오기
fetch(`/pos/get_table_order_list/${lastPath}`, {
  method: 'GET',
})
.then(response => response.json())
.then(data => {
  // 받은 데이터 처리
  console.log(data)
  order_history=data.map((order)=>({
    id: order.id,
    masterName : setMasterName(order),
    name: order.name,
    price: order.price,
    count: 1,
    options: order.options,
  }))
  changeBasketHtml(setBasketData(order_history))
})
.catch(error => {
  console.error('Error:', error);
});

// 할인 버튼 클릭 시
const clickDiscount = (event) => {
  openModalFun(event)
  const _modal = document.querySelector('.modal');
  const _modalTitle = document.querySelector('.modal-content h1');
  const _modalBody = document.querySelector('.modal-content .modal-body');
  _modalTitle.innerHTML = '할인'
  let html = `
  <div class="top ">
    <div class="content won" data-type="won">
      <div class="tab_btns">
        <button class="won_btn" onclick="">원</button>
        <button class="percent_btn" onclick="">%</button>
      </div>
      <div class="receive_amount">
        <h3>받을 금액</h3>
        <span>94,000원</span>
      </div>
      <div class="won_content">
        <div class="payment_amount">
          <h3>할인 금액</h3>
          <input type="text" oninput="updatePaymentAmount(event)"/>
        </div>
        <div class="percent_num_btns">
          <button>10%</button>
          <button>20%</button>
          <button>30%</button>
          <button>50%</button>
        </div>
      </div>
      <div class="split_payment_amount">
          <h3>할인 적용 금액</h3>
          <span>94,000원</span>
        </div>
    </div>
    <div class="number_pad" onclick="clickNumberPad(event)">
      <button data-value="1">1</button>
      <button data-value="2">2</button>
      <button data-value="3">3</button>
      <button data-value="4">4</button>
      <button data-value="5">5</button>
      <button data-value="6">6</button>
      <button data-value="7">7</button>
      <button data-value="8">8</button>
      <button data-value="9">9</button>
      <button data-value="C">C</button>
      <button data-value="0">0</button>
      <button data-value="←">←</button>
    </div>
  </div>
  <div class="bottom">
    <button>적용</button>
  </div>
  `
  _modalBody.innerHTML = html;
}

// 분할 결제 클릭 시
const clickSplitPayment = (event) => {
  openModalFun(event)
  const _modal = document.querySelector('.modal');
  const _modalTitle = document.querySelector('.modal-content h1');
  const _modalBody = document.querySelector('.modal-content .modal-body');
  _modalTitle.innerHTML = '분할 결제'
  let html = `
    <div class="top ">
      <div class="content direct" data-type="direct">
        <div class="tab_btns">
          <button class="direct_btn" onclick="clickDirectBtn(event)">직접 입력</button>
          <button class="dutch_btn" onclick="clickDutchBtn(event)">더치 페이</button>
        </div>
        <div class="receive_amount">
            <h3>받을 금액</h3>
            <span>94,000원</span>
          </div>
        <div class="dutch_content">
          <div class="count_btns">
            <button onclick="clickMinusCountBtn(event)"><i class="ph ph-minus"></i></button>
            <span>2</span>
            <button onclick="clickPlusCountBtn(event)"><i class="ph ph-plus"></i></button>
          </div>
        </div>
        <div class="direct_content">
          <div class="payment_amount">
            <h3>결제 금액</h3>
            <input type="text" oninput="updatePaymentAmount(event)"/>
          </div>
        </div>
        <div class="split_payment_amount">
            <h3>분할 결제 금액</h3>
            <span>94,000원</span>
          </div>
      </div>
      <div class="number_pad" onclick="clickNumberPad(event)">
        <button data-value="1">1</button>
        <button data-value="2">2</button>
        <button data-value="3">3</button>
        <button data-value="4">4</button>
        <button data-value="5">5</button>
        <button data-value="6">6</button>
        <button data-value="7">7</button>
        <button data-value="8">8</button>
        <button data-value="9">9</button>
        <button data-value="C">C</button>
        <button data-value="0">0</button>
        <button data-value="←">←</button>
      </div>
    </div>
    <div class="bottom">
      <button>적용</button>
    </div>
  `
  _modalBody.innerHTML = html;
}

// 직접 입력 버튼 클릭 시
const clickDirectBtn = (event) => {
  const _modalLeftEl = document.querySelector('.payment .modal-content .modal-body .top .content');
  _modalLeftEl.classList.remove('dutch')
  _modalLeftEl.classList.add('direct')
  _modalLeftEl.dataset.type='direct'
}

// 더치 페이 버튼 클릭 시
const clickDutchBtn = (event) => {
  const _modalLeftEl = document.querySelector('.payment .modal-content .modal-body .top .content');
  _modalLeftEl.classList.remove('direct')
  _modalLeftEl.classList.add('dutch')
  _modalLeftEl.dataset.type='dutch'
}

// 숫자 패드 클릭 시
const clickNumberPad = (event) => {
  const _modalLeftEl = document.querySelector('.payment .modal-content .modal-body .top .content');
  const curType = _modalLeftEl.dataset.type;

  const target = event.target;
  const targetValue = target.dataset.value;

  if(curType == 'direct'){ // 직접 입력 
    const _input = document.querySelector('.payment .modal-content .modal-body .top .content .payment_amount input');
    const value = _input.value;
    
    if(targetValue == undefined) return;
    _input.focus();
    if(targetValue == '←'){
      _input.value = setReplaceNumberPad(value.slice(0, -1));
    }
    if(targetValue == 'C'){
      _input.value = '';
    }
    if(targetValue != '←' && targetValue != 'C'){
      _input.value = setReplaceNumberPad(value + targetValue);
    }
  }
  if(curType == 'dutch'){ // 더치 페이
    const _input = document.querySelector('.payment .modal-content .modal-body .top .content .dutch_content .count_btns span');
    const value = _input.innerText;

    if(targetValue == undefined) return;
    _input.focus();
    if(targetValue == '←'){
      const newValue = setReplaceNumberPad(value.slice(0, -1));
      _input.innerText = newValue === "" ? "0" : newValue;
    }
    if(targetValue == 'C'){
      _input.innerText = '0';
    }
    if(targetValue != '←' && targetValue != 'C'){
      _input.innerText = setReplaceNumberPad(value + targetValue);
    }
  }

}

// 분할 결제 숫자 패드 클릭 시 입력 값 세팅
const setReplaceNumberPad = (str) => {
  return str.replace(/[^0-9]/g, '').replace(/^0+/, '').replace(/,(\s*)$/, '').toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
}

// 받을 금액에 입력 값이 변경 될 때
const updatePaymentAmount = (event) => {
  const curValue = event.target.value;
  event.target.value = curValue.replace(/[^0-9]/g, '').toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
}

// 더치 페이 - 클릭 시
const clickMinusCountBtn = (event) => {
  const _input = document.querySelector('.payment .modal-content .modal-body .top .content .dutch_content .count_btns span');
  const value = Number(_input.innerText);
  if(value == 0) return
  _input.innerText = String(value - 1);
}

// 더치 페이 + 클릭 시
const clickPlusCountBtn = (event) => {
  const _input = document.querySelector('.payment .modal-content .modal-body .top .content .dutch_content .count_btns span');
  const value = Number(_input.innerText);
  _input.innerText = String(value + 1);
}

// 현금 결제 클릭 시
const clickCashPayment = (event) => {
  openModalFun(event)
  const _modal = document.querySelector('.modal');
  const _modalTitle = document.querySelector('.modal-content h1');
  const _modalBody = document.querySelector('.modal-content .modal-body');
  _modalTitle.innerHTML = '현금 결제'
  let html = `
    <div class="top ">
      <div class="content direct" data-type="direct">
        <div class="receive_amount">
          <h3>받을 금액</h3>
          <span>94,000원</span>
        </div>
        <div class="direct_content">
          <div class="payment_amount">
            <h3>결제 금액</h3>
            <input type="text" oninput="updatePaymentAmount(event)"/>
          </div>
        </div>
        <div class="cash_amount ">
          <h3>현금 결제 금액</h3>
          <span>94,000원</span>
        </div>
        <div class="change_amount ">
          <h3>거스름 돈</h3>
          <span>94,000원</span>
        </div>
      </div>
      <div class="number_pad" onclick="clickNumberPad(event)">
        <button data-value="1">1</button>
        <button data-value="2">2</button>
        <button data-value="3">3</button>
        <button data-value="4">4</button>
        <button data-value="5">5</button>
        <button data-value="6">6</button>
        <button data-value="7">7</button>
        <button data-value="8">8</button>
        <button data-value="9">9</button>
        <button data-value="C">C</button>
        <button data-value="0">0</button>
        <button data-value="←">←</button>
      </div>
    </div>
    <div class="bottom">
      <button onclick="clickCashPaymentCompleted(event)">결제 완료</button>
    </div>
  `
  _modalBody.innerHTML = html;
}

// 현금 결제 완료 클릭 시
const clickCashPaymentCompleted = (event) => {
  // 결제 데이터 db 에 통신

  // 성공 모달 알림
  createCompletedPaymentModal(event, 'CASH');
}

// 결제 성공 모달
const createCompletedPaymentModal = (event, type) => {
  openModalFun(event)
  const _modal = document.querySelector('.modal');
  const _modalTitle = document.querySelector('.modal-content h1');
  const _modalBody = document.querySelector('.modal-content .modal-body');
  _modal.classList.add('success_payment')
  _modalTitle.innerHTML = ''
  let html = `
    <div class="top ">
      <i class="ph-fill ph-hands-clapping"></i>
      <h2>결제 완료</h2>
      <span>${type == 'CASH' ? `현금` : `카드`} 결제가 완료되었습니다.</span>
    </div>
    <div class="bottom">
      <button class="close" onclick="">확인</button>
    </div>
  `
  _modalBody.innerHTML = html;
  setPayment(type == 'CASH' ? 1 : 2)
}

const setOrderList = () => {
  const items = deepCopy(setBasketData(order_history));
  return order_list = items.map((item)=>{
    delete item.data.id;
    item.data.options.forEach((option)=>{
      delete option.id
    })
    return item.data
  })
}

const setPayment = (method) => {
  const tableId = lastPath;
  const order_list = setOrderList();
  const price = Number(document.querySelector('.payment main section article .top .total_price span').textContent);
  const payment = {
    'discount': 0,  
    'method': method,
    'price': price
  }
  console.log(tableId,order_list)
}