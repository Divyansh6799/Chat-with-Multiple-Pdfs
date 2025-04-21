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
<div class="chat-message bot" 
    <div class="avatar">
        <img src="https://i.ibb.co/cN0nmSj/Screenshot-2023-05-28-at-02-37-21.png">
    </div>
    <div style="flex-grow: 1; position: relative;">
        <div class="message" id="msg_{{ID}}" style="padding-right: 40px;">{{MSG}}</div>
        <button onclick="copyToClipboard('{{ID}}')"
                style="position: absolute; top: 0; right: 0; background: none; border: none; cursor: pointer;"
                title="Copy to clipboard">📋</button>
    </div>
</div>
<script>
function copyToClipboard(id) {
    const text = document.getElementById('msg_' + id).innerText;
    navigator.clipboard.writeText(text).then(function() {
        alert('Copied to clipboard!');
    }, function(err) {
        alert('Error copying text: ' + err);
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