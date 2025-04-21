# This file contains the HTML templates used for rendering chat messages in a web application.
# The templates are designed to display messages from both the user and the bot in a visually appealing manner.
css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
:root {
    --chat-bg: #f5f5f5;
    --text-color: #222;
    --bubble-bg: #ffffff;
    --bubble-text: #000;
}

@media (prefers-color-scheme: dark) {
    :root {
        --chat-bg: #2e2e2e;
        --text-color: #f0f0f0;
        --bubble-bg: #3c3c3c;
        --bubble-text: #f0f0f0;
    }
}
'''

bot_template = '''
<div class="chat-message bot" style="
    display: flex;
    align-items: flex-start;
    background-color: var(--chat-bg, #f5f5f5);
    border-radius: 12px;
    padding: 14px;
    margin-bottom: 18px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
    max-width: 100%;
    position: relative;
    color: var(--text-color, #222);
    font-family: 'Segoe UI', sans-serif;
">
    <!-- Avatar -->
    <div class="avatar" style="
        margin-right: 12px;
        flex-shrink: 0;
    ">
        <img src="https://i.ibb.co/cN0nmSj/Screenshot-2023-05-28-at-02-37-21.png"
             style="height: 48px; width: 48px; border-radius: 50%; object-fit: cover;">
    </div>

    <!-- Message bubble + copy button wrapper -->
    <div style="flex-grow: 1; display: flex; flex-direction: column; position: relative;">

        <!-- Message text -->
        <div class="message" id="msg_{{ID}}" style="
            background-color: var(--bubble-bg, #ffffff);
            padding: 12px 16px;
            border-radius: 10px;
            font-size: 16px;
            line-height: 1.6;
            word-wrap: break-word;
            overflow-wrap: break-word;
            color: var(--bubble-text, #000);
        ">{{MSG}}</div>

        <!-- Copy button floating outside bubble -->
        <button onclick="copyToClipboard('{{ID}}')" style="
            position: absolute;
            top: 6px;
            right: -42px;
            background: #f0f0f0;
            border: 1px solid #ccc;
            border-radius: 50%;
            padding: 6px 8px;
            font-size: 16px;
            cursor: pointer;
            transition: background 0.2s ease;
        " title="Copy to clipboard">
            📋
        </button>
    </div>
</div>

<script>
function copyToClipboard(id) {
    const el = document.getElementById('msg_' + id);
    if (!el) {
        console.error('Could not find element with id:', 'msg_' + id);
        return;
    }
    const text = el.innerText;
    navigator.clipboard.writeText(text).then(function() {
        console.log('✅ Copied:', text);
    }, function(err) {
        alert('❌ Error copying text: ' + err);
    });
}
</script>
'''


user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://img.icons8.com/?size=100&id=108652&format=png&color=000000">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''