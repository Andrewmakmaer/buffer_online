window.addEventListener('DOMContentLoaded', ()=>{
    var phone_numbers = document.getElementById('phone_number');
    phone_numbers.innerHTML = '+7(901)906-98-26';

    const url = 'http://localhost:8000/app';
    var data;
    var some_id;
    var some_key = 1;
    

    document.querySelector('.push_text').onclick = Click_text;
    document.querySelector('.push_key').onclick = Click_key;
    var btn = document.getElementById("copyText");

    btn.onclick = function() {
      let copy_text = document.getElementById("out_text_form");
      document.getElementById("message").innerHTML = "Скопировано!"
      copy_text.select();
      document.execCommand("copy");
    }

    function make_json(some_id, data, some_key){
         return json_data = { id: some_id,
                              text: data, 
                              key: some_key };
    }

    function Click_text(){
        let push_text = document.getElementById('text_area').value;
        post_data = make_json("add_text", push_text, 0);
        var result = post_and_get(post_data)
        .then(res => {new_key = res})
        .then(() => alert('Сгенерирован новый ключ: ' + new_key))
    }

    function Click_key(){
        let push_key = document.getElementById('key_area').value;
        if (push_key) {
          post_data = make_json("get_text", 'NoN', push_key);
          var out_text_form = document.getElementById('out_text_form');
          var result = post_and_get(post_data)
          .then(res => {recived_text = res})
          .then(()=>out_text_form.innerHTML = recived_text.slice(1, -1))
        } else {
          alert('Пожалуйста, введите ключ')
        }
    }

     
    async function post_and_get(data) {
        try {
          const response = await fetch(url, {
            method: 'POST', // или 'PUT'
            body: JSON.stringify(data), // данные могут быть 'строкой' или {объектом}!
            headers: {
              'Content-Type': 'application/json'
            }
          });
          const response_json = await response.json();
          return JSON.stringify(response_json);
        } catch (error) {
          console.error('Ошибка:', error);
        }
    }
});