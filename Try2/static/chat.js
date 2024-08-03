const socket = io();
const chatList = document.getElementById('chat-list');
const messagesContainer = document.getElementById('messages');
const messageInput = document.getElementById('message-input');
const sendBtn = document.getElementById('send-btn');
const createGroupBtn = document.getElementById('create-group-btn');

let currentRoom = 'general';

// Join the general room by default
socket.emit('join_room', { room: currentRoom });

// Load messages for the current room
socket.emit('get_messages', { room: currentRoom });

// Handle incoming messages
socket.on('message', (data) => {
    const msgElement = document.createElement('div');
    msgElement.textContent = `${data.sender}: ${data.message}`;
    messagesContainer.appendChild(msgElement);
});

// Load messages when switching rooms
socket.on('load_messages', (messages) => {
    messagesContainer.innerHTML = '';
    messages.forEach((message) => {
        const msgElement = document.createElement('div');
        msgElement.textContent = `${message[0]}: ${message[1]}`;
        messagesContainer.appendChild(msgElement);
    });
});

// Handle room join/leave announcements
socket.on('join_room_announcement', (message) => {
    const msgElement = document.createElement('div');
    msgElement.textContent = message;
    messagesContainer.appendChild(msgElement);
});

socket.on('leave_room_announcement', (message) => {
    const msgElement = document.createElement('div');
    msgElement.textContent = message;
    messagesContainer.appendChild(msgElement);
});

// Send message
sendBtn.addEventListener('click', () => {
    const message = messageInput.value;
    if (message) {
        socket.emit('message', { room: currentRoom, message });
        messageInput.value = '';
    }
});

// Switch rooms
chatList.addEventListener('click', (event) => {
    if (event.target.tagName === 'LI') {
        const room = event.target.dataset