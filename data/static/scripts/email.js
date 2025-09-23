// Show subject only if Email is selected
document.getElementById('message_type').addEventListener('change', function() {
    document.getElementById('email-subject').classList.toggle('hidden', this.value !== 'email');
});