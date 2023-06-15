function randomizeInputs(formname) {
  const inputs = document.querySelectorAll(`${formname} input`);
  inputs.forEach(input => {
    // 랜덤 값을 생성하고 입력 요소에 할당
    const randomValue = Math.random().toString(36).substring(2);
    input.value = randomValue;
  });

  // textarea 요소도 랜덤 값으로 채우기
  const textareas = document.querySelectorAll(`${formname} textarea`);
  textareas.forEach(textarea => {
    const randomValue = Math.random().toString(36).substring(2);
    textarea.value = randomValue;
  });
}
const url = 'http://your-api-endpoint.com/user/create'; // API 엔드포인트 URL

function createObjectFromFormData(form) {
  const formData = {};
  for (const element of form.elements) {
    if (element.name) {
      formData[element.name] = element.value;
    }
  }
  return formData;
}

function handleFormSubmit(formId, processData) {
  const form = document.getElementById(formId);
  form.addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = createObjectFromFormData(form);
    processData(formData);
  });
}

handleFormSubmit('userForm', function(userData) {
  console.log(userData);
});

handleFormSubmit('storeForm', function(storeData) {
  console.log(storeData);
});

handleFormSubmit('menuForm', function(menuData) {
  console.log(menuData);
});

handleFormSubmit('menuOptionForm', function(menuOptionData) {
  console.log(menuOptionData);
});

handleFormSubmit('mainCategoryForm', function(mainCategoryData) {
  console.log(mainCategoryData);
});

handleFormSubmit('subCategoryForm', function(subCategoryData) {
  console.log(subCategoryData);
});



// fetch(url, {
//   method: 'POST',
//   headers: {
//     'Content-Type': 'application/json'
//   },
//   body: JSON.stringify(userData)
// })
// .then(response => {
//   if (response.ok) {
//     console.log('User created successfully');
//   } else {
//     console.log('Failed to create user');
//   }
// })
// .catch(error => {
//   console.error('Error:', error);
// });
