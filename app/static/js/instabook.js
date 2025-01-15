import { initializeApp } from "https://www.gstatic.com/firebasejs/11.1.0/firebase-app.js";
import { getFirestore, collection, query, where, getDocs, onSnapshot, addDoc, serverTimestamp, orderBy, doc } from "https://www.gstatic.com/firebasejs/11.1.0/firebase-firestore.js";
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
//


let showContactList = function(){
    const list = document.getElementById('Contact');
    list.style.display='';
}

/*
let showProfileList = function(){
  const list = document.getElementById('Profile');
  list.style.display = '';
}
*/

addChatButton.addEventListener('click', showContactList);
// adding chat


//findProfileButton.addEventListener('click', showProfileList);
// adding profile to recently viewed

let addChat = function(other) {
    let fireChat = createNewChat(other);
    const chatlist = document.getElementById('chatList');
    const chat = document.createElement('li');
    chat.textContent = other;
    chat.setAttribute('id', fireChat.id)
    chatlist.appendChild(chat);
    const contact  = document.getElementById('Contact');
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

        sendMessage(newChat.id, thisUser, "Hi " +  other + " this is the start of our legendary chats!");
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

let displayPastChatsList = async function(){
    let chats = await getPastChats(thisUser);
    const chatlist = document.getElementById('chatList');
    chatlist.textContent ='';
    Array.from(chats).forEach(chat => {
        const htmlChat = document.createElement('li');
        let participants = chat.users.filter(people => people !== thisUser);
        htmlChat.textContent = participants[0];
        htmlChat.setAttribute('id', chat.id);
        if (chat.id !== focusPerson){
            htmlChat.classList.add('w-5/6', 'border', 'border-gray-600', 'bg-gray-600', 'text-white', 'p-5', 'rounded-xl');
        }
        else{
            htmlChat.classList.add('w-5/6', 'border', 'border-sky-400', 'bg-sky-400', 'text-white', 'p-5', 'rounded-xl')
        }
        htmlChat.addEventListener('click', function() {
            focusPerson = chat.id;
        });
        chatlist.appendChild(htmlChat);
        if(focusPerson === ''){
            focusPerson = chat.id;
        }
    })
}

displayPastChatsList();
setInterval(displayPastChatsList, 1000);


let chatNow = async function(){
    let chat = document.getElementById(focusPerson);
    let user = chat.textContent;
    displayPastChat(user, focusPerson);
}

chatNow();
setInterval(chatNow, 900);

let displayPastChat = async function(userID, chatID){
    const chatContent = document.getElementById("chatContent");
    chatContent.innerHTML = "";
    const chatName = document.getElementById('chatName');
    chatName.textContent = userID;
    const chatDocRef = doc(db, "chats", chatID);
    const messagesRef = collection(chatDocRef, "messages");
    const q = query(messagesRef, orderBy("timestamp"));
    onSnapshot(q, (querySnapshot) => {
        querySnapshot.forEach((doc) => {
            const messageData = doc.data();
            const newMessage = document.createElement("li");
            newMessage.textContent = messageData.text;
            newMessage.classList.add('p-3', 'max-w-xs', 'text-wrap', 'border', 'rounded-xl');
            if (messageData.user === thisUser){
                newMessage.classList.add('bg-gray-400', 'text-black', 'ml-auto', 'border-gray-400');
                console.log("this");
            }
            else{
                newMessage.classList.add('bg-sky-400', 'text-white', 'border-sky-400');
            }
            chatContent.appendChild(newMessage);
        });
        scrollToBottom();
    }, (error) => {
        console.error("Error listening for new messages:", error);
    });
}

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

let sendMessage = async function(chatID, userID, message){
    try{
        const chatDocRef = doc(db, "chats", chatID);
        const messagesRef = collection(chatDocRef, "messages");
        const newMessage = {
            user: userID,
            text: message,
            timestamp: serverTimestamp(),
        }

        await addDoc(messagesRef, newMessage);
    }
    catch (error){
        console.error("Error sending message:", error);
    }
}

const send = document.getElementById('sendMessage');
const messageContent = document.getElementById('messageContent');

send.addEventListener('submit', function () {

    event.preventDefault();
    if(messageContent.value){
        sendMessage(focusPerson, thisUser, messageContent.value);
    }

    messageContent.value = '';
});

function scrollToBottom() {
    const chatContent = document.getElementById('chatContent');
    chatContent.scrollTop = chatContent.scrollHeight; 
}

});
