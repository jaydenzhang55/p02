document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('search');
    const profileList = document.getElementById('profileList');

async function fetchUsers(){
    const response = await fetch('/search', {method: 'POST'});
    const data = await response.json();
    return data.users;
}

let filterPeople = function(){
    const searchTerm = searchInput.value.toLowerCase();
    const filteredUsers = users.filter(user => user.name.toLowerCase().includes(searchTerm));
    showProfileList(filteredUsers);
}

searchInput.addEventListener('input', filterPeople); //runs search, finds person/pofile


let showProfileList = function(usersToShow){
    profileList.innerHTML =''; //clears current list
    usersToShow.forEach(user => {
        const li = document.getElementById('li');
        profileList.appendChild(li);
    });
}

let users = [];
fetchUsers().then(fetchedUsers => {
    users = fetchUsers;
    showProfileList(users);

});

findFriendsButton.addEventListener('click', () => {
    searchInput = '';
    renderProfiles(users);
});

});




