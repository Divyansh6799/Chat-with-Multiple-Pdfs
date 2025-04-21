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
'''

bot_template = '''
<div class="chat-message bot" style="
    display: flex;
    align-items: flex-start;
    background-color: #f9f9f9;
    border-radius: 12px;
    padding: 12px;
    margin-bottom: 16px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    color: #333;
    max-width: 80%;
    word-wrap: break-word;
">
    <div class="avatar" style="
        margin-right: 12px;
        flex-shrink: 0;
    ">
        <img src="https://i.ibb.co/cN0nmSj/Screenshot-2023-05-28-at-02-37-21.png"
             style="max-height: 48px; max-width: 48px; border-radius: 50%; object-fit: cover;">
    </div>
    
    <div style="flex-grow: 1; position: relative;">
        <div class="message" id="msg_{{ID}}" style="
            background-color: #ffffff;
            padding: 12px;
            border-radius: 8px;
            font-size: 16px;
            line-height: 1.5;
            max-width: 100%;
            white-space: pre-wrap;
            overflow-wrap: break-word;
            word-wrap: break-word;
        ">{{MSG}}</div>
        
        <button onclick="copyToClipboard('{{ID}}')" style="
            position: absolute;
            top: 8px;
            right: 8px;
            background: #f0f0f0;
            border: 1px solid #ddd;
            border-radius: 50%;
            padding: 8px;
            cursor: pointer;
            font-size: 18px;
            color: #333;
            transition: all 0.3s ease;
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