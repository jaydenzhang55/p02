

document.addEventListener('DOMContentLoaded', function () {
//Messages JS
var focusPerson = "";

//Search
const searchInput = document.getElementById('search');

const peopleList = document.getElementById('searchResult');

const plist = peopleList.getElementsByTagName('li');

let filterPeople = function(){
    const searchTerm = searchInput.value.toLowerCase();

    Array.from(plist).forEach(person => {
        const personName = person.textContent.toLowerCase();
        
        if (personName.includes(searchTerm)) {
            person.style.display = '';
        } else {
            person.style.display = 'none';
        }
    });
}

searchInput.addEventListener('input', filterPeople);

const  addChatButton = document.getElementById('addChat');

let showContactList = function(){
    const list = document.getElementById('Contact');
    list.style.display='';
}

addChatButton.addEventListener('click', showContactList)

// adding chat

let addChat = function(other) {
    const check = document.getElementById(other);
    if(check === null){
        const chatlist = document.getElementById('chatList');
        const chat = document.createElement('li');
        chat.textContent = other;
        chat.setAttribute('id', other)
        focusPerson = other;
        chatlist.appendChild(chat);
        const contact = document.getElementById('Contact');
        contact.style.display='none';


    }
    else{
        focusPerson = other;
    }
}

Array.from(plist).forEach((person) => {
    person.addEventListener('click', function() {
        addChat(person.textContent);
    });
});
});