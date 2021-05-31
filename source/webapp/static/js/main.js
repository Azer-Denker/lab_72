const BASE_API_URL = '/api/v1/'
async function makeRequest(url, method='GET', data=undefined) {
    let opts = {method, headers: {}};

    if (!csrfSafeMethod(method))
        opts.headers['X-CSRFToken'] = getCookie('csrftoken');

    if (data) {
        opts.headers['Content-Type'] = 'application/json';
        opts.body = JSON.stringify(data);
    }
    console.log(opts);
    let response = await fetch(url, opts);
    console.log(response);

    if (response.ok) {
        console.log(response)
        return response;
    } else {
        let error = new Error(response.statusText);
        error.response = response;
        console.log(error.response)
        throw error;
    }
}
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

async function addQuote(event) {
    event.preventDefault();
    let response = await makeRequest('/api/v1/quote/', 'POST', {
        text: document.getElementById('text_quote').value,
        author: document.getElementById('author').value,
        email: document.getElementById('email').value
    });
    let data = await response.json();
    console.log(data);
    document.getElementById('text_quote').value = ""
    document.getElementById('author').value = ""
    email: document.getElementById('email').value = ""
}

async function like_quote(event) {
    event.preventDefault()
    let data = await makeRequest('/api/v1/quote/'+event.target.id + '/like', 'GET').then(response => response.json())
    console.log(data)
    quote = await  makeRequest('/api/v1/quote/'+event.target.id, 'GET').then(response => response.json())
    event.target.parentElement.getElementsByTagName('p')[1].innerText = 'Raiting' + ':' + quote['rating']
}

async function dislike_quote(event) {
    event.preventDefault()
    let data = await makeRequest('/api/v1/quote/'+event.target.id + '/dislike', 'GET').then(response => response.json())
    console.log(data)
    quote = await  makeRequest('/api/v1/quote/'+event.target.id, 'GET').then(response => response.json())
    event.target.parentElement.getElementsByTagName('p')[1].innerText = 'Raiting' + ':' + quote['rating']
}

function show_form(event){
    event.preventDefault()
    let form = document.getElementById('form')
    form.style.display = "block"
}

function show_one_quote(event){
    event.preventDefault()
    quotes = document.getElementsByClassName('quote')
    for (quote of quotes)
    {
        quote.classList.add("hidden")
    }
    event.target.parentElement.classList.remove('hidden')
}

async function get_quote(event){
    event.preventDefault()
    let data = await makeRequest('/api/v1/quote/', 'GET').then(response => response.json())
    console.log(data);
    for (quote of data) {
        let div = document.createElement('div');
            div.className = 'quote';
            let a = document.createElement('a')
            a.innerText = 'text' + ':' + quote['text']
            a.href = ''
            a.classList.add('like')
            a.addEventListener('click', show_one_quote )
            div.appendChild(a)
            let p1 = document.createElement('p')
            p1.innerText = 'created' + ':' + Date(quote['created_at'])
            p1.classList.add('ml-3')
            div.appendChild(p1)
            let p2 = document.createElement('p')
            p2.innerText = 'Raiting' + ':' + quote['rating']
            p2.classList.add('ml-3')
            div.appendChild(p2)

        let like = document.createElement("a")
            like.innerText = 'like'
            like.href = ''
            like.id = quote['id']
            like.classList.add('like')
            div.appendChild(like)
            like.addEventListener('click', like_quote)

        let dislike = document.createElement("a")
            dislike.innerText = 'dislike'
            dislike.href = ''
            dislike.id = quote['id']
            dislike.classList.add('like')
            div.appendChild(dislike)
            dislike.addEventListener('click', dislike_quote)

        container = document.getElementById('quotes')
        container.appendChild(div)
        container.classList.remove("hidden");
        form = document.getElementById('form')
        form.classList.add("hidden");
    }
}

window.addEventListener('load', function() {
    const send_button = document.getElementById('send');
    send_button.onclick = addQuote;
    const home_button = document.getElementById('home_menu')
    home_button.onclick = get_quote;
    const new_quote = document.getElementById('add_quote')
    console.log(new_quote)
    new_quote.onclick = show_form;
});