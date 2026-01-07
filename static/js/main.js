//  const chatIcon = document.getElementById('chat-icon');
//  const chatbot = document.getElementById('chatbot-window');
//  const form = document.getElementById('chatbot-form');
//  const input = document.getElementById('chatbot-input');
//  const body = document.getElementById('chatbot-body');
//
//  chatIcon.addEventListener('click', () => {
//    chatbot.classList.toggle('hidden');
//  });
//
//  form.addEventListener('submit', (e) => {
//    e.preventDefault();
//    const userMsg = input.value.trim();
//    if (!userMsg) return;
//
//    const userBubble = document.createElement('div');
//    userBubble.className = 'chatbot-message user';
//    userBubble.textContent = userMsg;
//    body.appendChild(userBubble);
//
//    input.value = '';
//
//    // Simulated bot response
//    setTimeout(() => {
//      const botBubble = document.createElement('div');
//      botBubble.className = 'chatbot-message bot';
//      botBubble.textContent = "Thanks for your message! We'll get back to you shortly.";
//      body.appendChild(botBubble);
//      body.scrollTop = body.scrollHeight;
//    }, 600);
//  });
