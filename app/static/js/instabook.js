import { initializeApp } from "https://www.gstatic.com/firebasejs/11.1.0/firebase-app.js";
import { getFirestore, collection, query, where, getDocs, onSnapshot, addDoc, serverTimestamp } from "https://www.gstatic.com/firebasejs/11.1.0/firebase-firestore.js";
import { getMessaging } from "https://www.gstatic.com/firebasejs/11.1.0/firebase-messaging.js";

const firebaseKey = 'AIzaSyBCUpBRlURDAupPoq7dXpee0MKfFxkh1Vk';

const firebaseConfig = {
    apiKey: firebaseKey,
    authDomain: "h1n1---instabook.firebaseapp.com",
    projectId: "h1n1---instabook",
    storageBucket: "h1n1---instabook.firebasestorage.app",
    messagingSenderId: "857268042390",
    appId: "1:857268042390:web:a2290dff1564eac80160b7",
    measurementId: "G-0793H5FCXT"
  };

  const app = initializeApp(firebaseConfig);
  const db = getFirestore(app);
  const messaging = getMessaging(app);

document.addEventListener('DOMContentLoaded', function () {

localStorage.setItem('firebase_debug', 'true');
//Messages JS
let focusPerson = "";

const thisUser = document.getElementById('user').getAttribute('data-user');
console.log(thisUser);

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

const addChatButton = document.getElementById('addChat');
const findProfileButton = document.getElementById('findProfile');


let showContactList = function(){
    const list = document.getElementById('Contact');
    list.style.display='';
}

let showProfileList = function(){
  const list = document.getElementById('Profile');
  list.style.display = '';
}

addChatButton.addEventListener('click', showContactList)
// adding chat
findProfileButton.addEventListener('click', showProfileList)
// adding profile to recently viewed

let addChat = function(other) {
    let fireChat = createNewChat(other);
    const chatlist = document.getElementById('chatList');
    const chat = document.createElement('li');
    chat.textContent = other;
    chat.setAttribute('id', fireChat.id)
    focusPerson = fireChat.id;
    chatlist.appendChild(chat);
    const  = document.getElementById('Contact');
    contact.style.display='none';
}

let findProfile = function(other){
  const profList = document.getElementById('profileList');
  const prof = document.createElement('li');
}

let createNewChat = async function(other){
    try {
        let participants = [other, thisUser];
        participants.sort();
        const newChat = await addDoc(collection(db, "chats"), {
            name: participants.join('_'),
            users: participants,
            createdAt: serverTimestamp(),
        });
        return newChat;
    }
    catch (error) {
        console.error("Error creating chat: ", error);
      }
}

let getPastChats = async function(user){
    try {
        const chatsRef = collection(db, "chats");

        const q = query(chatsRef, where("users", "array-contains", user));
        const chatSnapshot = await getDocs(q);
        const chatsList = chatSnapshot.docs.map(doc => ({
          id: doc.id,
          ...doc.data(),
        }));
        return chatsList;

      } catch (error) {
        console.error("Error fetching chats:", error);
      }
}

let displayPastChats = async function(){
    let chats = await getPastChats(thisUser);
    const chatlist = document.getElementById('chatList');
    Array.from(chats).forEach(chat => {
        const htmlChat = document.createElement('li');
        let participants = chat.users.filter(people => people !== thisUser);
        htmlChat.textContent = participants[0];
        htmlChat.setAttribute('id', chat.id);
        chatlist.appendChild(htmlChat);
        focusPerson = chat.id;
    })
}


displayPastChats();

Array.from(plist).forEach((person) => {
    person.addEventListener('click', function() {
        let chats = document.getElementById('chatList');
        if(chats !== null){
            let chat = chats.getElementsByTagName('li');
            if (chat !== null){
                if (!!Array.from(chat).find(element => element.textContent === person.textContent)){
                    focusPerson = Array.from(chat).find(element => element.textContent === person.textContent).getAttribute('id');
                    const contact = document.getElementById('Contact');
                    contact.style.display='none';
                }
                else{
                addChat(person.textContent);
                }
            }
        }
    });
});
});
